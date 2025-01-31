====== Templates ======

Zim uses templates when exporting pages. This way you can for example write your website in zim and export it to HTML using the layout and style definition of your choice.

Templates are also used to initialize new pages.

If you are looking for information for file templates for attachments, see [[Attachments]]

===== Template Editor Dialog =====

The Template Editor Dialog can be accessed with the menu item "//Edit//" -> "//Templates//". It will show a list of templates that are available, and allows you to view and edit them.

Templates can either be system defaults, or custom templates in your home folder. When you edit them, a copy is made of the default to your home folder, and this copy is then edited. The remove function again deletes this custom version but does not touch the default template.

**Note:** if you try to edit, for example, an HTML template, and it opens in the web browser instead of in your default text editor, the cause is most likely that you did not explicitly configure a text editor in the preferences. Go to the [[Preferences|Preferences Dialog]] and specify your text editor.

===== Templates =====
Templates are located in ''/usr/share/zim/templates/'' and ''~/.local/share/zim/templates'' by default. You can add templates you use more often there. To modify a template copy it to the ''~/.local/...'' directory and edit it.

==== Export templates ====

For a list of templates for exporting see [[Export]] and subpages.

==== Page templates ====

**wiki/Default.txt**
This template is used to initialize new pages. The default contains a header with the page name and the date at which the page was created.

**wiki/Journal.txt**
This template is used to initialize new pages in the Journal section.

===== Template syntax =====
The template is a combination of the normal document output that you want to produce (e.g. HTML or Latex) combined with template instructions. The normal text is passed on to the output unmodified, while the instructions get replaced by the output of the template processing.

Template instructions can have two forms:

'''
[% some expression %]
'''

''and''

'''
<!--[% some expression %]-->
'''

The first is typically used but the second form can look better in HTML or XML templates as it is parsed as an XML comment by other tools.

==== Expressions ====
Expressions used in template instructions can be:

'''
True, False, None		# literal true, false and none
"string", 'string', 5, 5.0	# text or number
[.., .., ..]			# list
variable			# variable name
variable.name,			# variable name with named attributes
mylist.0			# variable containing a list with index
function(.., ..)		# function call
'''


The following operators can be used:

'''
and
or
not
== 		# Equals
!= 		# Not equals
> 		# Greater than
>=		# Greater or equal than
< 		# Less than
<=		# Less or equal than
'''


Valid variable names can contain letters (a - z) and numbers (0 - 9) and underscores ( _ ). The first character of the variable name must be a letter.

==== Instructions ====
An instruction can be one of the following:

'''
GET
SET
IF expr EL(S)IF expr .. ELSE .. END
FOR var IN expr .. END
FOREACH var = expr ... END
BLOCK name .. END
INCLUDE name or expr -- block or file
'''


The instruction is always in upper case letters. The expressions within can be either upper or lower case names.

=== Get & Set ===

'''
[% expr %]			 # implicit GET

[% GET expr %]
'''

With GET you evaluate an expression and the result is put into the output. Typically the expression will just be a variable name.

'''
[% SET var = expr %]
'''

With SET you assign a variable. It does not output in the result and the instruction will be removed.

=== Conditionals ===

'''
[% IF expr %] ... [% END %]	# conditionals
'''

'''
[% IF expr %]
...
[% ELSIF expr %]
...
[% ELSE %]
...
[% END %]
'''

In any of these constructs the expression is evaluated and depending on the result one of the blocks is added to the output. Used to include optional output in the template

=== Loops ===

'''
[% FOR var IN expr %]		# loop
...
[% END %]
'''

'''
[% FOREACH var = expr ]
...
[% END %]
'''

In these instructions the result of an expression — typically an input variable — is iterated and for each iteration the block is evaluated.

Within the loop the variable "''var''" is available and set to result of the iteration.

In addition there is a special variable "''loop''" that can be used to access the loop state. It is defined with following attributes:

'''
loop.first		True / False
loop.last		True / False
loop.parity		"even" or "odd"
loop.even		True / False
loop.odd		True / False
loop.size		n
loop.max		n-1
loop.index		0 .. n-1
loop.count		1 .. n
loop.outer		outer "loop" or None
loop.prev		previous item or None
loop.next		next item or None
'''


=== Blocks ===

'''
[% BLOCK name %]
...
[% END %]

[%  INCLUDE name %]
'''


A BLOCK can be defined anywhere in the template and then included in other places using the INCLUDE statement. This is useful e.g. for template parts that repeat multiple times in the document. Note that a BLOCK is always defined in the top-level scope, so you can not put them e.g. in an IF clause to define alternative versions. A BLOCK may be defined after the location where they are used.

If no block with name "name" is defined, "name" will be evaluated as a parameter. If the value of the parameter is a block name, that block will be included. If the value of the parameter is a file path a file include will be done.

=== File INCLUDE ===

'''
[% INCLUDE "path/to/file.txt" %]
'''

Will include the content of "file.txt" in the template and parse it as template content as well.

Only files included in the template resources (see below) can be included this way.


==== Objects and functions ====

Most variables behave partially as objects, which means that it is possible to call object methods on them. The following standard (python) object methods are commonly supported:

Strings: '''capitalize''', '''center''', '''count''', '''endswith''', '''expandtabs''', '''ljust''', '''lower''', '''lstrip''', '''replace''', '''rjust''', '''rsplit''', '''rstrip''', '''split''', '''splitlines''', '''startswith''', '''title''', '''upper'''

Lists: '''get''', '''len''', '''reversed''', '''sorted'''

Dictionary: '''get''', '''keys''', '''values''', '''items''', '''len''', '''reversed''', '''sorted'''

The following standard (python) functions are supported: ''len(list)'', ''sorted(list)'', ''reversed(list)'', ''range(start, end)''.


Other functions defined for all templates:

	''html_encode(text)''
		Format text in HTML encoding

	''url_encode(text)''
		Format text in URL encoding

	''strftime(template, date)''
		Format a date, see standard library for codes

	''strfcal(template, date)''
		Format a week number, accepts:

			%w for day of week according to locale
			%W for weeknumber according to locale
			%Y for the year to which the week belongs


===== Template variables and functions =====

==== Page templates ====
Only a single variable is defined for new pages:

'''
page
	.name
	.section
	.basename
'''

See also the [[Plugins:Journal|Journal Plugin]] for some properties available for journal pages

==== Export templates ====
When using templates when [[Export|exporting]] the following set of variables and functions is available in the export template:

'''
generator
	.name		Zim version number "Zim x.xx"
	.user		The current user name

title			Page title

navigation		links to other export pages (if not included in the same output file)
	.home
	.up					(not implemented yet)
	.prev
	.next

links			Sorted dictionary with links to other export pages (index, plugins, etc.)

	link
		.name
		.basename

pages			Iterator over all content to be exported (special + content)
	.special	Sorted dictionary with special pages to be included (index, plugins, etc.)
 	.content	Iterator with pages being exported to this file (1 or more)

	page
		.title		Either the first heading, or the page name
		.name		The page name
		.meta		Dict with meta properties, if any
		.section	The name of the parent page, if any
		.basename	The page name without the section name
		.heading	First heading of the page
		.body		Full body minus first heading
		.content	Heading + body
		.headings(max_level)	Split the page content by headings

 			headingsection
				.level		Heading level
 				.heading	Heading text
 				.body		Content below this heading
 				.content	Content including the heading

		.links
		.backlinks
		.attachments

			file
				.basename
				.mtime
				.size

options			Dictionary with template options that can be set to control the output format
'''

Functions:

	''uri(link|file)''
		Turns a zim link or file object into an URL

	''anchor(page)''
		Turns an output page into an achor that can be linked

	''resource(filename)''
		Returns an URL for a template resource (see below)

	''index(section, collapse, ignore_empty)''
		Creates a page index of the set of pages being exported.

		''section'': the starting page of the index - defaults to the top level (":")
		''collapse'': if ''True'' only branches related to the current page are visible, if ''False'' all branches are visible - defaults to ''True''
		''ignore_empty'': if ''True'' empty pages are ignored — defaults to ''True''.


===== Template Options =====
For export templates, a parameter named "''options''" allows setting options for the export format. You can set an option in a template using e.g.:
'''

[% options.line_breaks = 'remove' %]

'''
The following options are supported:

**HTML**
* ''options.line_breaks'': value should be either "''default''" or "''remove''", controls line breaks (''<br>'' elements) in paragraphs
* ''options.empty_lines'': value should be either "''default''" or "''remove''", controls whether empty lines in the source should be inserted as ''<br>'' elements in the HTML output between top level elements like paragraphs, headings etc.

**Latex**
* ''options.document_type'': one of "''report''", "''article''" or "''book''". Controls the heading type used.

===== Template Resources =====
To add additional files to the template, create a folder of the same name as the template. Any files in the folder (like style sheets, images, javascript files, etc.) will be copied along when this template is used to export data in zim. There is a function "''resource(filename)''" to refer to these files in the template. For example:

'''
<link rel="stylesheet" href="[% resource('style.css') %]">
'''

Zim always includes some images when exporting for the checkboxes used in checkbox lists. To customize these there should be template resources named "''checked-box.png''", "''unchecked-box.png''" and "''xchecked-box.png''" in this folder.

For the web interface, the resources can also contain a "''favicon.ico''" to serve as the favicon of the website.
