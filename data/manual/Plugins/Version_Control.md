====== Version Control ======

Zim's default installation ships with a Version Control Plugin. To enable it, go to ''Edit -> Preferences -> Plugins'' and check the box next to Version Control. Zim supports [[http://bazaar.canonical.com/|Bazaar]],  [[https://git-scm.com/|Git]], [[http://mercurial.selenic.com/|Mercurial]], and [[https://www.fossil-scm.org/|Fossil]]  as backends.

**Dependencies:** This plugin requires one of the supported version control systems to be installed. Currently, Bazaar, Git, Mercurial and Fossil are supported, so one of these applications is required. In specific the "''bzr''", "''git''", "''hg''" or "''fossil''" command should be available in the system path.

===== Options =====
If the option **Autosave version when the notebook is closed** is enabled zim will save (or "commit") a new version every time you close zim or when opening zim if new changes are detected.

When the option **Autosave version on regular intervals** is enabled zim will save (or "commit") a new version after a set time interval. The **Autosave interval in minutes** gives the time interval.
Saving at regular intervals also includes at the exit and at the start of the application.

===== Usage =====
If you want to keep track of your changes or if you want to collaborate on a Zim notebook as a team, version control is the best way to go. Zim integrates very well with existing version control software because all relevant data is stored in plain text files.

To save the current state of the Notebook, choose ''File -> Save Version...'' from the Main Menu and confirm that you want to enable Version Control. In the next window add a comment describing the changes (probably something like "yeah, first version" at this point) and confirm by clicking Save.

You can browse the complete history of saved versions by selecting ''File -> Versions...'' from the Main Menu. You can view and restore previous versions of your Notebook and view all your changes between two versions in the window that opens.

==== The "Versions" dialog ====
TODO: document details all buttons

The "**Restore Version**" button allows restoring a single page to a selected revision. All changes since the last saved version will be lost.

The "**Side by Side**" button is used to show two versions of the page side by side with an external program like [[http://meldmerge.org/|meld]]. It only works when you select a revision for a single page. If the button remains insensitive, probably no suitable application is found.

You can configure applications to use for side by side comparison by installing a ''.desktop'' file in the [[Help:Config Files|zim data folder]] under ''helpers/compare_files/''. The application should accept two file names as arguments.

===== Sharing =====
TODO here should be documented how to share the newly created repository with your collaborators... (Depends on the backend chosen)

See the [[http://bazaar.canonical.com/|Bazaar]] user manual for various scenarios of collaboration (follow the "documentation" link on their website).

===== Technical Details =====
Technically speaking a local repository is created when enabling Version Control, depending on the backend you choose, this repository is managed by  [[http://bazaar.canonical.com/|Bazaar]],  [[https://git-scm.com/|Git]], [[http://mercurial.selenic.com/|Mercurial]] or [[https://www.fossil-scm.org/|Fossil]]. Every time you save a version, another revision is checked in. Zim just uses standard version control systems as a backend, so you can always view and export your history using standard tools.

On startup, zim tries to detect the version control system used for a specific notebook, and use it if supported. So you can manually the initialize repository (e.g. by branching) and then open them with zim. No need to tell Zim that the notebook is managed explicitly.

==== Known issues ====

Global user settings might not get picked up on Windows, possibly due to Zim running in an MSYS2 environment. In practice, this means you'll need a local configuration for backends that require initial setup. In the case of Git, you can solve this issue by executing ''git config user.name "Your Name"'' and ''git config user.email "your.email@example.com"'' in the repository folder, ie. set up a local configuration by omitting the ''--global'' flag from the usual commands.

===== Manual Version Control =====
This is for advanced users that have to use another Version Control System or have other reasons not to use the included plugin.

To manually manage revisions of your notebook, the following files should be added to your repository:
* The "''notebook.zim''" file in the notebook folder
* All your pages (*.txt files in the notebook folder and subfolders)
* All files linked/embedded from/into your pages ([[Help:Attachments|attachments]], etc.)

All files created by Zim are in plain text format and only change when you explicitly change them so you should get readable, reasonable diffs and merges in case of conflicts.

You can and should ignore the following items, however:
* The complete "''.zim''" folder - this is a local cache that will be regenerated
* Anything you manually put into or below the root folder you do not want to be in your repository

The files in the "''.zim''" folder are caches of the index and some client configuration (window sizes, scroll position, etc.) and some of it is in binary format, so you do not need or want it in your repository.

If you want for some reason stop using version control and throw away all history, you can do the following:
* Disable the version control plugin
* Quit zim
* Remove from your notebook folder:
	* the .bzr folder and .bzrignore file in case of Bazaar,
	* the .hg folder and the .hgignore file in case of Mercurial,
	* the .git folder and the .gitignore file in case of Git.
	* the .fslckout or _FOSSIL_ file in case of Fossil.
