
# Copyright 2008-2015 Jaap Karssenberg <jaap.karssenberg@gmail.com>


'''The ExportLinker object translates links in zim pages to URLS
for the export content
'''

import logging

logger = logging.getLogger('zim.exporter')

#~ import base64

from .layouts import ExportLayout

from zim.parse.encode import url_decode, url_encode
from zim.formats import BaseLinker
from zim.newfs import SEP, LocalFile, LocalFolder
from zim.notebook import interwiki_link, encode_filename, HRef, PageNotFoundError
from zim.parse.links import link_type
from zim.formats import BaseLinker


class ExportLinker(BaseLinker):
	'''This object translate links in zim pages to (relative) URLs.
	This is used when exporting data to resolve links.
	Relative URLs start with "./" or "../" and should be interpreted
	in the same way as in HTML. Both URLs and relative URLs are
	already URL encoded

	@todo: info on formats to know how to set "usebase"
	'''

	def __init__(self, notebook, layout, source=None, output=None,
						usebase=False, document_root_url=None
	):
		'''Contructor
		@param notebook: the source L{Notebook} for resolving links
		@param layout: the L{ExportLayout} for resolving target files
		@param source: is the L{Path} of the source page being exported
		@param output: is a L{File} object for the destination file
		@param usebase: if C{True} the format allows returning relative paths
		@param document_root_url: optional URL for the document root
		'''
		self.notebook = notebook
		self.layout = layout
		self.source = source
		self.output = output

		if output:
			self.base = output.parent()
		else:
			self.base = None

		self.usebase = usebase

		self.document_root_url = document_root_url

		#~ self._icons = {} # memorize them because the occur often in one page


	## Methods used while exporting to resolve links etc. ##

	def link(self, link):
		'''Returns an url for a link in a zim page
		This method is used to translate links of any type.

		@param link: link to be translated
		@returns: url, uri, or relative path
		context of this linker
		'''
		# Determines the link type and dispatches any of the "link_*" methods
		assert isinstance(link, str)
		type = link_type(link)
		methodname = '_link_' + type
		if hasattr(self, methodname):
			href = getattr(self, methodname)(link)
		else:
			href = link
		# print("Linker:", link, '-->', href, '(%s)' % type)
		return href

	def img(self, src):
		'''Returns an url for image file 'src' '''
		return self._link_file(src)

	#~ def icon(self, name):
		#~ '''Returns an url for an icon'''
		#~ if not name in self._icons:
			#~ path = 'icons/%s.png' % name
			#~ self._icons[name] = self.resource(path)
		#~ return self._icons[name]

	def resource(self, path):
		'''Return an url for template resources'''
		dir = self.layout.resources_dir()
		file = dir.file(path)
		return self.file_object(file)

	def resolve_source_file(self, link):
		'''Find the source file for an attachment
		Used e.g. by the latex format to find files for equations to
		be inlined. Do not use this method to resolve links, the file
		given here might be temporary and is not guaranteed to be
		available after the export.
		@returns: a L{File} object or C{None} if no file was found
		'''
		return self.notebook.resolve_file(link, self.source)

	def resolve_dest_file(self, link):
		'''Find the destination file for an attachment
		@returns: a L{File} object
		'''
		return self._resolve_file(link)

	def page_object(self, path):
		'''Turn a L{Path} object in a relative link or URI'''
		try:
			file = self.layout.page_file(path)
		except ValueError:
			return '' # Link outside of current export ?
		else:
			if file == self.output:
				return '#' + path.name # single page layout ?
			else:
				return self.file_object(file)

	def file_object(self, file):
		'''Turn a L{File} object in a relative link or URI'''
		if self.base and self.usebase \
		and file.ischild(self.layout.relative_root):
			relpath = file.relpath(self.base, allowupward=True).replace(SEP, '/')
			if not relpath.startswith('.'):
				relpath = './' + relpath
			return relpath
		elif self.notebook.document_root \
		and self.document_root_url \
		and file.ischild(self.notebook.document_root):
			relpath = file.relpath(self.notebook.document_root).replace(SEP, '/')
			return self.document_root_url + relpath
		else:
			return file.uri





	## Methods below are internal, not used by format or template ##

	def _link_page(self, link):
		href = HRef.new_from_wiki_link(link)
		if not href.names:
			return '#' + href.anchor if href.anchor else ''

		try:
			if self.source:
				path = self.notebook.pages.resolve_link(self.source, href)
			else:
				path = self.notebook.pages.lookup_from_user_input(link)
		except ValueError:
			return ''
		else:
			url = self.page_object(path)
			return url + '#' + href.anchor if href.anchor else url

	def _link_file(self, link):
		try:
			file = self._resolve_file(link)
		except:
			logger.info("Could not resolve file: %s", link)
			return link # E.g. non-local file:/ URI etc.
		else:
			return self.file_object(file)

	def _resolve_file(self, link):
		file = self.notebook._resolve_abs_file(link)
		if file is None:
			if self.source:
				folder = self.layout.attachments_dir(self.source)
			else:
				folder = self.layout.relative_root

			file = LocalFile(folder.get_abspath(link))

		myfolder = LocalFolder(file)
		if link[-1] in ('/', '\\') or myfolder.exists():
			return myfolder
		else:
			return file

	def _link_mailto(self, link):
		if link.startswith('mailto:'):
			return link
		else:
			return 'mailto:' + link

	def _link_interwiki(self, link):
		href = interwiki_link(link)
		if href and href != link:
			return self.link(href) # recurs
		else:
			logger.warning('No URL found for interwiki link "%s"', link)
			return None

	def _link_notebook(self, link):
		if link.startswith('zim+'):
			link = link[4:]

		if '?' in link:
			link, path = link.split('?')
			# FIXME: code below is not robust because we don't know the
			# storage mode of linked notebook...
			path = url_decode(path) # was already encoded by interwiki_link()
			path = encode_filename(path).replace(' ', '_')
			return link + '/' + url_encode(path) + '.md'
		else:
			return link
######changed return link + '/' + url_encode(path) + '.txt' to return link + '/' + url_encode(path) + '.md'

class StubLayout(ExportLayout):
	'''Stub implementation of L{ExportLayout} that is used by
	L{StaticExportLinker}
	'''

	def __init__(self, notebook, resources_dir):
		self.notebook = notebook
		self.resources_dir = resources_dir

	def page_file(self, page):
		try:
			page = self.notebook.get_page(page)
			return page.source_file
		except PageNotFoundError:
			return None

	def attachments_dir(self, page):
		return self.notebook.get_attachments_dir(page)

	def resources_dir(self):
		return self.resources_dir


#~ def data_uri(file):
	#~ if file.basename.endswith('.png'):
		#~ mime = 'image/png'
	#~ else:
		#~ mime = file.mimetype()
	#~ data64 = u''.join(base64.encodestring(file.read_binary()).splitlines())
	#~ return u'data:%s;base64,%s' % (mime, data64)


class StaticExportLinker(ExportLinker):
	'''This linker can be used when exporting a page to e.g. html
	without a file to write the html to. All links are resolved
	statically to the source files.
	'''

	def __init__(self, notebook, resources_dir=None, source=None):
		layout = StubLayout(notebook, resources_dir)
		ExportLinker.__init__(self, notebook, layout, source=source)

	#~ def icon(self, name):
		#~ if not name in self._icons:
			#~ path = 'icons/%s.png' % name
			#~ if self.layout.resources_dir:
				#~ file = self.layout.resources_dir.file(path)
				#~ if file.exists():
					#~ self._icons[name] = data_uri(file)

			#~ if not name in self._icons:
				#~ file = data_file('pixmaps/%s.png' % name)
				#~ if file.exists():
					#~ self._icons[name] = data_uri(file)
				#~ else:
					#~ self._icons[name] = file.uri

		#~ return self._icons[name]
