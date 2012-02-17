# -*- coding: utf-8 -*-

# Copyright 2009 Jaap Karssenberg <pardus@cpan.org>

from __future__ import with_statement

import os
import logging

from zim.fs import FS
from zim.applications import Application
from zim.async import AsyncOperation
from zim.plugins.versioncontrol import NoChangesError
from zim.plugins.versioncontrol.generic import VersionControlSystemBackend

logger = logging.getLogger('zim.vcs.bzr')
# TODO check if bzrlib also uses logging for output


# Disabled using bzrlib for now as this seems to conflict with threading - see lp: 555257
#~ try:
#~     import bzrlib.commands as bzrlib
#~ except ImportError:
#~ 	logger.warn('Could not load bzrlib - falling back to calling bzr as external program')
bzrlib = None


class BzrlibApplication(Application):
	'''This class is a wrapper around the bzrlib library which supports the same
	API as an Application object for an external application. It gives command
	arguments directly to the library to handle instead of actually spawning a
	process to call the executable.

	Falling back to using "Application(('bzr',))" instead should give the exact
	same results.
	'''

	def __init__(self):
		Application.__init__(self, ('bzr',))

	def run(self, args, cwd=None):
		if bzrlib:
			cwd = unicode(cwd).encode('utf-8')
			self._bzrlib(args, cwd)
		else:
			Application.run(self, cwd=cwd)

	# TODO find out how to implement pipe() using bzrlib

	def _bzrlib(self, args, cwd):
		ourcwd = os.getcwdu()
		os.chdir(cwd)
		try:
			args = [unicode(a).encode('utf-8') for a in args]
			args.insert(1, '-q') # --quiet
			logger.info('Running through bzrlib: %s', args)
			#~ bzrlib.run_bzr(args)
			bzrlib.main([None] + args)
		except:
			logger.exception('Error thrown by bzrlib')
		os.chdir(ourcwd)


if bzrlib:
	_bzr = BzrlibApplication()
else:
	_bzr = Application(('bzr',))


# TODO document API - use base class
class BazaarVCS(VersionControlSystemBackend):

	def __init__(self, dir):
		super(BazaarVCS, self).__init__(dir)


	@classmethod
	def _vcs_specific_check_dependencies(klass):
		"""@see VersionControlSystemBackend.check_dependencies"""
		return _bzr.tryexec()

	def _vcs_specific_ignored(self, path):
		"""Return True if we should ignore this path
		TODO add bzrignore patterns here

		@see VersionControlSystemBackend._vcs_specific_ignored
		     and VersionControlSystemBackend._ignored
		"""
		return False

	def _vcs_specific_init(self):
		"""Init a repository, here are operations specific to the VCS
		@see VersionControlSystemBackend._vcs_specific_init()
		"""
		_bzr.run(['init'], cwd=self.root)
		_bzr.run(['whoami', 'zim'], cwd=self.root) #FIXME - bzr need a user to be setup
		_bzr.run(['ignore', '**/.zim/'], cwd=self.root) # ignore cache
		_bzr.run(['add', '.'], cwd=self.root) # add all existing files

	def _vcs_specific_on_path_created(self, fs, path):
		"""@see VersionControlSystemBackend.on_path_created"""
		if path.ischild(self.root) and not self._ignored(path):
				def wrapper():
					_bzr.run(['add', path], cwd=self.root)
				AsyncOperation(wrapper, lock=self.lock).start()

	def _vcs_specific_on_path_moved(self, fs, oldpath, newpath):
		"""@see VersionControlSystemBackend.on_path_moved"""
		if newpath.ischild(self.root) and not self._ignored(newpath):
			def wrapper():
				if oldpath.ischild(self.root):
					# Parent of newpath needs to be versioned in order to make mv succeed
					_bzr.run(['add', '--no-recurse', newpath.dir], cwd=self.root)
					_bzr.run(['mv', oldpath, newpath], cwd=self.root)
				else:
					_bzr.run(['add', newpath], cwd=self.root)
			AsyncOperation(wrapper, lock=self.lock).start()
		elif oldpath.ischild(self.root) and not self._ignored(oldpath):
			self.on_path_deleted(self, fs, oldpath)

	def _vcs_specific_on_path_deleted(self, path):
		"""@see VersionControlSystemBackend.on_path_deleted"""
		def wrapper():
			_bzr.run(['rm', path], cwd=self.root)
		AsyncOperation(wrapper, lock=self.lock).start()

	def _vcs_specific_get_status(self):
		"""Returns last operation status as a list of text lines
		@see VersionControlSystemBackend._vcs_specific_get_status()
		     and VersionControlSystemBackend.get_status()
		"""
		return _bzr.pipe(['status'], cwd=self.root)


	def _vcs_specific_get_diff(self, versions=None, file=None):
		"""FIXME Document this
		Returns the diff operation result of a repo or file
		@param versions: couple of version numbers (integer)
		@param file: L{UnixFile} object of the file to check, or None
		@returns the diff result
		"""
		diff = None
		rev = self._revision_arg(versions)
		nc = ['=== No Changes\n']
		if file is None:
			diff = _bzr.pipe(['diff'] + rev, cwd=self.root) or nc
		else:
			diff = _bzr.pipe(['diff', file] + rev, cwd=self.root) or nc
		return diff

	def _vcs_specific_get_annotated(self, file, version=None):
		"""FIXME Document"""
		rev = self._revision_arg(version)
		annotated = _bzr.pipe(['annotate', file] + rev, cwd=self.root)
		return annotated

	def _vcs_specific_commit(self, msg):
		stat = ''.join( _bzr.pipe(['st'], cwd=self.root) ).strip()
		if not stat:
			raise NoChangesError(self.root)
		else:
			_bzr.run(['add'], cwd=self.root)
			_bzr.run(['commit', '-m', msg], cwd=self.root)

	def _vcs_specific_revert(self, version=None, file=None):
		"""FIXME Document this"""
		rev = self._revision_arg(version)
		if file is None:
			_bzr.run(['revert'] + rev, cwd=self.root)
		else:
			_bzr.run(['revert', file] + rev, cwd=self.root)
	

	def _vcs_specific_list_versions(self, file=None):
		"""FIXME Document"""
		# TODO see if we can get this directly from bzrlib as well
		if file is None:
			lines = _bzr.pipe(['log', '--forward'], cwd=self.root)
		else:
			lines = _bzr.pipe(['log', '--forward', file], cwd=self.root)

		versions = []
		(rev, date, user, msg) = (None, None, None, None)
		seenmsg = False
		for line in lines:
			if line.startswith('----'):
				if not rev is None:
					versions.append((rev, date, user, msg))
				(rev, date, user, msg) = (None, None, None, None)
			elif line.startswith('revno: '):
				value = line[7:].strip()
				if ' ' in value:
					# e.g. "revno: 48 [merge]\n"
					i = value.index(' ')
					value = value[:i]
				rev = int(value)
			elif line.startswith('committer: '):
				user = line[11:].strip()
			elif line.startswith('timestamp: '):
				date = line[11:].strip()
			elif line.startswith('message:'):
				seenmsg = True
				msg = u''
			elif seenmsg and line.startswith('  '):
				msg += line[2:]

		if not rev is None:
			versions.append((rev, date, user, msg))

		return versions

	def _vcs_specifc_get_version(self, file, version):
		rev = self._revision_arg(version)
		version = _bzr.pipe(['cat', file] + rev, cwd=self.root)
		return version

	def _revision_arg(self, versions):
		# Accepts: None, int, string, (int,), (int, int)
		# Always returns a list

		if isinstance(versions, (tuple, list)):
			assert 1 <= len(versions) <= 2
			if len(versions) == 2:
				versions = map(int, versions)
				versions.sort()
				return ['-r', '%i..%i' % tuple(versions)]
			else:
				versions = versions[0]

		if not versions is None:
			version = int(versions)
			return ['-r', '%i' % version]
		else:
			return []
