# Fork of Zim - A Desktop Wiki Editor

![zim banner](./website/files/images/globe.png)

Zim is a graphical text editor used to maintain a collection of wiki pages. Each
page can contain links to other pages, simple formatting, and images. Pages are
stored in a folder structure, like in an outliner, and can have attachments.
Creating a new page is as easy as linking to a nonexistent page. All data is
stored in plain text files with wiki formatting. Various plugins provide
additional functionality, like a task list manager, an equation editor, a tray
icon, and support for version control.

![Screenshot](./website/files/screenshots/zim-normal.png)

Zim can be used to:

* Keep an archive of notes
* Keep a daily or weekly journal
* Take notes during meetings or lectures
* Organize task lists
* Draft blog entries and emails
* Do brainstorming

- [X] Zim Wiki Markdown Fork
    - [X] Doing Interput (2)
    - [X] Doing (2)
    - [X] Next (2)
    - [X] Planning (2)
        - [ ] Using markdown markup instead of zim wiki markup
            - [ ] instant refresh
            - [ ] linking
            - [ ] anchors
    - [X] Backlog

## Changes in this fork

* Zim uses Markdown files
* Markdown files does not need the headers in the files
* Help files are Markdown files
* searchdialog without loading screens

## Installing from a Package

Most Linux distributions include zim in their package repository. On Debian and
Ubuntu, the package is simply called "zim".

Debian/Ubuntu packages, a Windows installer and an app for macOS can be found on the [website](https://zim-wiki.org/downloads.html).

## Installing from Source

**NOTE:** You don't need to install zim in order to test it. You should be able to run it
directly from the source directory by calling `./zim.py`. (To run a translated
version from the source, run `./setup.py build_trans`.)

First, you should verify you have the dependencies zim needs. To list all dependencies check `./setup.py --requires`.

You will at least need the following:

* Gtk+ >= 3.18
* python3 >= 3.6
* python3-gi (also known as pygobject, but make sure to have the "gi" based version)
* python3-xdg (optional, but recommended)
* xdg-utils (optional, but recommended on linux)
* python3-pillow (optional, to support more image formats like ".webp")

To verify that zim is working properly on your system, you can run the test suite using `./test.py`. Failures do not have to be critical, but in principle, all tests should pass.

Zim can be installed from source using:

    ./setup.py install

If you are installing Zim from source in a Python virtual environment,
you need to tell Zim where to load necessary data files by
`export XDG_DATA_DIRS=<where-your-virtual-environment-root-folder-is>/share:$XDG_DATA_DIRS`.
Please refer to the `Install Paths` section for more details about the XDG paths.

Most plugins have additional requirements. These are listed in the plugin descriptions.

### Ubuntu

On Ubuntu or other Debian derived systems, the following packages should be installed:

* python3
* gir1.2-gtk-3.0
* python3-gi
* python3-xdg
* python3-pillow

### Windows

Download, install and update [MSYS2](https://www.msys2.org/) 64-bit by following the instructions on their website.

Open "MSYS2 MSYS" terminal from the Start Menu and install GTK3, Python3 and Python bindings for GTK:

`pacman -S mingw-w64-x86_64-gtk3 mingw-w64-x86_64-python3 mingw-w64-x86_64-python3-gobject`

The Windows drive is mounted on `/c`, browse your Windows user folder using:

`cd "/c/Users/$USERNAME"`

You can now run Zim from the MSYS terminal using:

`/mingw64/bin/python3 zim.py`

Or from any Windows terminal using:

`C:\msys64\mingw64\bin\python3.exe zim.py`

For more details see [GTK installation instructions for Windows](https://www.gtk.org/docs/installations/windows/) and [PyGObject Getting Started](https://pygobject.readthedocs.io/en/latest/getting_started.html).

*Note:* installation of the "msys" environment offers a "32" and a "64" bit
shell. When you installed the "64" packages for Gtk, they will only run from
the "64" shell.

### macOS

You can use a package manager like [Homebrew](https://brew.sh) (instructions [here](https://formulae.brew.sh/formula/zim)) or [MacPorts](https://www.macports.org) (instructions [here](https://ports.macports.org/port/zim/)) to install Zim and its dependencies. Please note that we do not have the resources to offer any support for this.

### Install Paths

If you install zim in a non-default location, you may need to set the PYTHONPATH environment variable in order for zim to find its python modules. For example, if you installed the modules below "/home/user/lib/zim" you need to set:

    PYTHONPATH=/home/user/lib

Also, zim uses the XDG paths to locate data and config files. If you get an error that zim can not find its data files, for example, if you installed the zim data files to "/home/user/share/zim", you will need to set the data path like this:

    XDG_DATA_DIRS=/home/user/share:/usr/local/share:/usr/share

## Contributing

See [CONTRIBUTING](./CONTRIBUTING.md) and [PLUGIN_WRITING](./PLUGIN_WRITING.md)
for information on contributing to the zim source code, translations and
documentation.

## Copyright and License

Zim is an open-source program. This means it can be used and distributed freely
under the conditions of the [license](./LICENSE).

All files in this package, except for those mentioned below, are
copyrighted by Jaap Karssenberg <jaap.karssenberg@gmail.com>

Translations are copyrighted by their respective translators. All translations
that are entered through the launchpad or weblate websites are distributed
under the BSD license. See the translation files for detailed translator credits.

The following files were included from other sources:

* `zim/inc/xdot.py` - Copyright 2008 Jose Fonseca
* `zim/inc/arithmetic.py` - Copyright 2010, 2011 Patricio Paez
* From the default Gnome icon theme:
  * `pixmaps/task-list.png` (was: `stock_todo.png`)
  * `pixmaps/attachment.png` (was: `mail-attachment.png`)
* From Gtk+ 2.8
  * `pixmaps/link.png` (was: `stock_connect_24.png`)
* `pixmaps/calendar.png` (was: `stock_calendar-view-month.png`)
  Copyright 2007 by Jakub Steiner, released under GPL
  modifications copyright 2009 by Gabriel Hurley
