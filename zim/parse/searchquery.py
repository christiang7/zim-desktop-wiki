# Copyright 2009-2025 Jaap Karssenberg <jaap.karssenberg@gmail.com>

'''This module contains logic to parse search queries

The main entry point is the function L{parse_search_query()} which takes a string
and definition of supported keywords and returns a L{SearchQuery} object.

Search queries consist of keywords like `content: foo` to search content for `foo`
or `name: foo` to search names matching `foo`.

Search terms without a keyword are mapped to a default keyword.

Search terms can be combined using operators.

Supported operators:
	- "NOT", "not" and "-"
	- "AND", "and", and "+"
	- "OR" or "or"

Order of precedence: AND, OR, NOT
so "foo AND NOT bar OR baz" means AND(foo, OR(NOT(bar), baz))

Explicit groups can be made by "(" and ")"

This module does not implement the search itself, see C{zim.search} for page search.
For other cases, the helper function L{compile_search_query_check_function()} can be used.
'''


import re
import logging

from functools import partial
from collections.abc import Callable

from .encode import unescape_string


logger = logging.getLogger('zim.parsing.searchquery')


OPERATOR_OR = 'OR'
OPERATOR_AND = 'AND'
OPERATOR_NOT = 'NOT'
OPERATOR_GROUP_START = '('
OPERATOR_GROUP_END = ')'


_operator_tokens = (OPERATOR_OR, OPERATOR_AND, OPERATOR_NOT, OPERATOR_GROUP_START, OPERATOR_GROUP_END)

operators = {
	'or': OPERATOR_OR,
	'and': OPERATOR_AND,
	'+': OPERATOR_AND,
	'-': OPERATOR_NOT,
	'not': OPERATOR_NOT,
	'(': OPERATOR_GROUP_START,
	')': OPERATOR_GROUP_END,
}
_operators_allowed_in_keyword_group = ('+', '-')
_operators_not_allowed_in_keyword_group = ('(', ')')
# 'and' 'or' 'not' will be interpreted as string in keyword group context

_word_re = re.compile(r'''
	(	'(\\'|[^'])*' |  # single quoted word
		"(\\"|[^"])*" |  # double quoted word
		[^\s'"]+         # word without spaces or quotes
	)''', re.X)


def split_quoted_strings(string: str) -> list[str]:
	'''Split a word list respecting quotes, does not remove the quotes

	Allow both double and single quotes

	This function always expect full words to be quoted, even if quotes
	appear in the middle of a word, they are considered word
	boundries.
	'''
	string = string.strip()
	words = []
	m = _word_re.match(string)
	while m:
		words.append(m.group(0))
		i = m.end()
		string = string[i:].lstrip()
		m = _word_re.match(string)

	if string:
		words += string.split() # unmatched quote ?

	return [w for w in words if w]


def unescape_quoted_string(string: str) -> str:
	'''Removes quotes from a string and unescapes embedded quotes'''
	if not string:
		return string
	elif string[0] in ('"', "'") and string[-1] == string[0]:
		string = string[1:-1]
	return unescape_string(string)


def _indent(string):
	return ''.join("\t"+l for l in string.splitlines(True))


class SearchQuery:
	'''Object to represent a search query'''

	def __init__(self, operator=OPERATOR_AND, terms: 'Iterable|None'=None, negate: bool=False):
		self.operator = operator
		self.terms = list(terms) if terms else []
		assert all(isinstance(t, (SearchQuery, SearchQueryTerm)) for t in self.terms), self.terms
		self.negate = negate

	def __eq__(self, other):
		return isinstance(other, self.__class__) and \
			(self.operator, self.negate, self.terms) == (other.operator, other.negate, other.terms)

	def __repr__(self):
		return "<%s op=%r negate=%r [\n%s\n]>" % (
			self.__class__.__name__, self.operator, self.negate,
			'\n'.join(_indent(repr(t)) for t in self.terms)
		)

	def __len__(self):
		return len(self.terms)

	def __iter__(self):
		return iter(self.terms)

	def __getitem__(self, i):
		return self.terms[i]

	def add(self, term):
		self.terms.append(term)

	def remove(self, term):
		i = self.terms.index(term)
		self.terms.pop(i)

	def copy(self):
		'''Shallow copy'''
		return self.__class__(self.operator, list(self.terms), self.negate)


class SearchQueryTerm:
	'''Object to represent a single keyword term in a search query'''

	def __init__(self, keyword: str, value: str, negate: bool=False):
		self.keyword = keyword.lower()
		self.value = value
		self.negate = negate

	def __eq__(self, other):
		# Compare resulting term, not original string information
		return isinstance(other, self.__class__) and \
			(self.keyword, self.negate, self.value) == (other.keyword, other.negate, other.value)

	def __repr__(self):
		return "<%s %r %r negate=%r>" % (self.__class__.__name__, self.keyword, self.value, self.negate)

	def copy(self):
		'''Shallow copy'''
		return self.__class__(self.keyword, self.value, self.negate)


def parse_search_query(string: str, keywords: dict, default_keyword: str='any') -> SearchQuery:
	'''Parse a search query string into a L{SearchQuery} object

	Parsing behavior is controlled by the `keywords` dict and the `default_keyword`.
	The `keywords` dict should specify valid keywords as keys, the value should be a dict.
	The following keys are supported:

	  - `implicit_match` defines a regex object to be used to match this keyword implicit,
	     e.g. `search_tag_re` for the `tags` keyword

	For malformed queries warnings are logged while skipping over the errors.

	@param string: the string to be parsed
	@param keywords: dict with supported keywords
	@param default_keyword: keyword for strings without keyword specified
	'''
	tokens = _tokenize_search_query(string, keywords, default_keyword)
	tokens = _collect_explicit_groups(tokens)
	query = _process_operators(tokens)
	return query


def _tokenize_search_query(string: str, keywords: dict, default_keyword: str='any') -> list:
	# Split string in words, each word is either a search term or an operator
	# terms without a keyword get the default keyword

	# Bootstrap regexes
	keyword_re = re.compile('(' + '|'.join(keywords) + '):(.*)', re.I|re.U)
	implicit_keywords = {}
	if isinstance(keywords, dict): # should always be a dict, but in testing we use sets
		for k in keywords:
			if 'implicit_match' in keywords[k]:
				r = keywords[k]['implicit_match']
				implicit_keywords[k] = re.compile(r, re.U) if isinstance(r, str) else r

	def match_implicit_keyword(string):
		for k, r in implicit_keywords.items():
			if r.match(string):
				return k
		else:
			return default_keyword


	# First do a raw tokenizer
	words = split_quoted_strings(string)
	tokens = []
	while words:
		w = words.pop(0)

		if w[0] in ('(', ')', '+', '-') and len(w) > 1:
			words.insert(0, w[1:])
			w = w[0]

		while w[-1] in ('(', ')') and len(w) > 1:
			words.insert(0, w[-1])
			w = w[:-1]

		m_key = keyword_re.match(w)
		if w.lower() in operators:
			tokens.append(operators[w.lower()])
		elif m_key:
			keyword = m_key.group(1).lower()
			if m_key.group(2) or ( words and not words[0][0] == '(' ):
				string = m_key.group(2) or words.pop(0)
				term = unescape_quoted_string(string)
				tokens.append(SearchQueryTerm(keyword, term))
			elif words and words[0][0] == '(':
				# special case to support "keyword: (value value value)" as "(keyword:value keyword:value keyword:value)"
				if words[0] == '(':
					words.pop(0)
				else:
					words[0] = words[0][1:]
				tokens.append(OPERATOR_GROUP_START)
				tokens.extend(_tokenize_group_for_term(keyword, words))
			else:
				# no more words - edge case - something ending in ":" but nothing following
				term = m_key.group(1)+":"
				keyword = match_implicit_keyword(term)
				tokens.append(SearchQueryTerm(keyword, term))
		else:
			keyword = match_implicit_keyword(w)
			term = unescape_quoted_string(w)
			tokens.append(SearchQueryTerm(keyword, term))
	return tokens


def _tokenize_group_for_term(keyword, words):
	# Collect all words untill ")" as keyword terms for "keyword"
	tokens = []
	while words and words[0][0] != ')':
		w = words.pop(0)

		if w[0] in ('(', ')', '+', '-') and len(w) > 1:
			words.insert(0, w[1:])
			w = w[0]

		while w[-1] in ('(', ')') and len(w) > 1:
			words.insert(0, w[-1])
			w = w[:-1]

		if w in _operators_allowed_in_keyword_group:
			tokens.append(operators[w])
		elif w == '(':
			logger.warning("Out of place '(' operator in keyword group of search query")
			# skip over this token
		else:
			term = unescape_quoted_string(w)
			tokens.append(SearchQueryTerm(keyword, term))

	return tokens


def _collect_explicit_groups(tokens: list) -> list:
	# Group matched "(" and ")" and raise on unmatched occurences
	stack = [[]]
	for i, t in enumerate(tokens):
		if t == OPERATOR_GROUP_START:
			subgroup = []
			stack[-1].append(subgroup)
			stack.append(subgroup)
		elif t == OPERATOR_GROUP_END:
			if len(stack) > 1:
				stack.pop()
			else:
				logger.warning("Unmatched ')' in search query")
				# skip over this token
		else:
			stack[-1].append(t)

	if len(stack) > 1:
		logger.warning("Unmatched '(' in search query")

	return stack[0]


def _process_operators(tokens: list) -> SearchQuery:
	# Validate out of place operators at start and end
	if not tokens or all(t in _operator_tokens for t in tokens):
		logger.warning('Empty search query')
		return SearchQuery()

	# Turn sub groups into queries - depth first
	for i in range(0, len(tokens)):
		if isinstance(tokens[i], list):
			tokens[i] = _process_operators(tokens[i]) # recurs

	# Process NOT operators and remove out of place AND / OR operators
	if tokens[0] == OPERATOR_AND:
		# Allow for one stray AND operator, to get over "+foo +bar"
		tokens.pop(0)

	while tokens[0] in (OPERATOR_AND, OPERATOR_OR):
		logger.warning("Out of place operator at start of query: %s" % tokens[0])
		tokens.pop(0)

	while tokens[-1] in (OPERATOR_AND, OPERATOR_OR, OPERATOR_NOT):
		logger.warning("Out of place operator at end of query: %s" % tokens[-1])
		tokens.pop()

	for i in range(0, len(tokens)-1):
		if tokens[i] == OPERATOR_NOT:
			tokens[i] = None
			if isinstance(tokens[i+1], (SearchQuery, SearchQueryTerm)):
				tokens[i+1].negate = True
			else:
				logger.warning("Out of place NOT operator in search query")
		elif tokens[i] in (OPERATOR_OR, OPERATOR_AND):
			if tokens[i+1] in (OPERATOR_OR, OPERATOR_AND):
				logger.warning("Out of place operator in query: %s" % tokens[i])
				tokens[i] = None
			elif tokens[i] == OPERATOR_AND:
				# implicit deafult, so remove already
				tokens[i] = None
			else:
				pass
		elif tokens[i] in (OPERATOR_GROUP_START, OPERATOR_GROUP_END):
			logger.warning('Bug: all operators should be removed at this point, found %s' % tokens[i])
			tokens[i] = None
		
	tokens = [t for t in tokens if t is not None]

	# Check for implicit sub-groups, and return top level group as query
	while OPERATOR_OR in tokens:
		i = tokens.index(OPERATOR_OR) # position first OR
		j = i # position last OR
		while j < len(tokens) and tokens[j] == OPERATOR_OR:
			j += 2

		group = [t for t in tokens[i-1:j] if t != OPERATOR_OR]
		if i == 1 and j == len(tokens):
			# We consumed the whole token list
			return SearchQuery(OPERATOR_OR, group)
		else:
			# Splice subgroup in list
			tokens = tokens[:i-1] + [SearchQuery(OPERATOR_OR, group)] + tokens[j:]
	else:
		# Final group is implicit AND group
		if len(tokens) == 1 and isinstance(tokens[0], SearchQuery):
			return tokens[0]
		else:
			return SearchQuery(OPERATOR_AND, tokens)


def search_query_term_to_regex(value: str) -> re.Pattern:
	'''Returns a regex object for a simple string match of a L{SearchQueryTerm}

	The following rules are applied:
	  - a "*" optionally matches any non-whitespace character
	  - a space " " matches any combination of whitespace, or begin or end of the string
	  - by default matches begin at a word boundary, unless they start with "*" or a chinese character
	  - a space " " at the start does nothing but the default behavior, unless the first character is chinese
	  - by default matches can end anywhere in a word, unless they end with a space " "
	  - a "*" at the end does nothing but the default behavior

	@param value: the L{term.value} attribute of a L{SearchQueryTerm}
	@param returns: a C{re.Pattern} object
	'''
	# NOTE: changes in above rules also need to be updated in the manual
	case = False # TODO: how to switch this from the query?

	# Globs to regex
	parts = []
	for p in value.strip().strip('*').split('*'):
		sub_parts = re.split('\\s+', p) # use regex split to have empty match at start and end of piece
		parts.append(r'\s+'.join(map(re.escape, sub_parts)))
	regex = r'\S*'.join(parts)

	# Add word delimiters according to the rules explained above, but avoid adding them next
	# to non-word characters or next to chinese charaters.
	# Chinese is treated special because it does not always use whitespace as word delimiter.
	if re.match(r'^\s+\w', value, re.U) \
		or (re.match(r'^\w', value, re.U) and not '\u4e00' <= value[0] <= '\u9fff'):
			regex = r'\b' + regex

	if re.search(r'\w\s+$', value, re.U):
		regex = regex + r'\b'

	if case:
		return re.compile(regex, re.U)
	else:
		return re.compile(regex, re.U | re.I)


def search_query_pagename_term_to_regex(value: str) -> re.Pattern:
	'''Returns a regex object for a page name match of a L{SearchQueryTerm}

	The following rules are applied:
	  - a "*" optionally matches any character
	  - a space " " matches any combination of whitespace
	  - by default matches anywhere in the name, without word boundries, since page names can be CamelCase
	  - a "*" at the start or the end does nothing but the default behavior
	  - a ":" matches the start or end of a name segment
	  - a "::" at the start matches start at the top-level of the notebook
	  - a "::" at the end excludes sub-pages
	  - a ":+" at the end gives sub-pages put excludes the parent page

	@param value: the L{term.value} attribute of a L{SearchQueryTerm}
	@param returns: a C{re.Pattern} object
	'''
	# NOTE: changes in above rules also need to be updated in the manual
	case = False # TODO: how to switch this from the query?

	# Globs to regex
	parts = []
	for p in value.strip().strip('*').split('*'):
		sub_parts = re.split('\\s+', p) # use regex split to have empty match at start and end of piece
		parts.append(r'\s+'.join(map(re.escape, sub_parts)))
	regex = r'.*'.join(parts)

	if value.startswith(' '):
		regex = r'\s+' + regex
	elif regex.startswith('::'):
		regex = '^:?' + regex[2:]
	elif regex.startswith(':'):
		regex = '(^:?|:)' + regex[1:]

	if value.endswith(' '):
		regex = regex + r'\s+'
	elif regex.endswith('::'):
		regex = regex[:-2] + ':?$'
	elif value.endswith(':+'):
		regex = regex[:-3] + ':.+'
	elif regex.endswith(':'):
		regex = regex[:-1] + '(:|:?$)'

	if case:
		return re.compile(regex, re.U)
	else:
		return re.compile(regex, re.U | re.I)


search_tag_re = re.compile(r'^@[\w*]+@?$', re.U) #: Inteded to be used for implicit keyword parsing


def search_query_tags_term_to_regex(value: str) -> re.Pattern:
	'''Return a regex object for a tag name

	The following rules are applied:

	  - a "*" optionally matches any character
	  - a "*" at the start or the end does nothing but the default behavior
	  - if the term starts with a "@" it will only match from the start of the name
	  - if the term ends with a "@" it will only match from the end of the name

	@param value: the L{term.value} attribute of a L{SearchQueryTerm}
	@param returns: a C{re.Pattern} object
	'''
	startword = value.startswith('@')
	endsword = value.endswith('@')
	parts = value.strip('*').strip('@').split('*')
	regex = r'.*'.join(map(re.escape, parts))
	if startword:
		regex = '\\b' + regex
	if endsword:
		regex = regex + '\\b'
	return re.compile(regex, re.U | re.I)


def check_func_constructor(term: SearchQueryTerm, keywords: dict) -> Callable[[object], bool]:
	'''To be used as a constructor with L{compile_search_query_check_function}
	The resulting check function does by default a string match based on C{search_query_term_to_regex}
	on the value of the given key in the object.
	Requires the C{key} to be specified in the keywords dict.
	If a c{regex_constructor} function is given in the keyword dict, this is used instead
	of C{search_query_term_to_regex}
	'''
	if 'regex_constructor' in keywords[term.keyword]:
		regex_constructor = keywords[term.keyword]['regex_constructor']
	else:
		regex_constructor = search_query_term_to_regex

	pattern = regex_constructor(term.value)
	key = keywords[term.keyword]['key']

	def mychecker(record):
		return bool(pattern.search(record[key]))

	return mychecker


def check_func_constructor_any_keyword(term: SearchQueryTerm, keywords: dict) -> Callable[[object], bool]:
	'''To be used as a constructor with L{compile_search_query_check_function}
	Intended for the default keyword. It effectively constructs an "or" function over multiple fields
	in the record. The C{'include'} value in the keywords dict should provide a list
	of keywords to include.
	'''

	check_functions = []
	for keyword in keywords[term.keyword]['include']:
		constructor = keywords[keyword].get('check_func_constructor', check_func_constructor)
		myterm = SearchQueryTerm(keyword, term.value)
		checker = constructor(myterm, keywords)
		check_functions.append(checker)

	def mychecker(record):
		for checker in check_functions:
			if checker(record):
				return True
		else:
			return False

	return mychecker


def _negate_checker(checker, *a):
	return not checker(*a)


def _and_checker(checkers, record):
	return all(c(record) for c in checkers)


def _or_checker(checkers, record):
	return any(c(record) for c in checkers)


def compile_search_query_check_function(query: SearchQuery, keywords: dict) -> Callable[[object], bool]:
	'''Compile a query to a function that checks whather a given object matches the query

	This function compiles a function that matches the rules of the given C{query} such that it
	returns boolean when called with an "record" to be checked. This "record" is an object which
	has an C{__getitem__} method and be iterable. Typical usage is checking tuples or dicts
	as records.

	The C{keywords} dict should contain definitions of the keywords supported in the query.
	It is intended to be the same dict as provided to C{parse_search_query()}.

	By default each term is interpretad as a string match against a given field in the "record".
	The C{keywords} dict should have a key C{'key'} which gives the mapping into the record.

	To change the default behavior, a key C{'check_func_constructor'} can be given in the keywords
	dict. This should have a functions as value that constructs the final check function. 
	The constructors should have the signature:

			constructor(term: SearchQueryTerm, keywords: dict) -> Callable[[object], bool]

	And result in a check function

			check(record: Sequence|Mapping) -> bool

	These check functions only need to check for a positive match, the wrapper takes care of
	operators and negation.

	Check function constructors included here are L{check_func_constructor_pagename} and 
	L{check_func_constructor_any_keyword} which implement a different regex for pagenames and 
	a check any field behavior.

	@param keywords: dict with keywords as keys and a dict with attributes (e.g. the type) as values
	@returns: a check function for the whole query C{check(record: Mapping) -> bool}
	'''
	members = []
	for term in query.terms:
		if isinstance(term, SearchQuery):
			members.append(compile_search_query_check_function(term, keywords)) # recurs
		else:
			constructor = keywords[term.keyword].get('check_func_constructor', check_func_constructor)
			checker = constructor(term, keywords)
			if term.negate:
				members.append(partial(_negate_checker, checker))
			else:
				members.append(checker)

	if len(members) == 1:
		# optimize for simple case by loosing group wrapper
		if query.negate:
			return partial(_negate_checker, members[0])
		else:
			return members[0]
	else:
		op_func = _or_checker if query.operator == OPERATOR_OR else _and_checker
		if query.negate:
			return partial(_negate_checker, op_func, members)
		else:
			return partial(op_func, members)

