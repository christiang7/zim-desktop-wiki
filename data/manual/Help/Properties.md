Content-Type: text/x-zim-wiki
Wiki-Format: zim 0.4

====== Properties ======

The dialog with notebook properties can be accessed with the menu item "//File//" -> "//Properties//". The following notebook properties can be configured:

The notebook **Name** is used in the "[[Notebooks|Open Notebook]]" dialog and e.g. in the menu for the [[Plugins:Tray Icon|Tray Icon]]. This name is also used for the window title.

The notebook **Interwiki Keyword** can be used to link to this notebook for other notebooks. See "Interwiki" in [[Links]] for more info.

The **Home Page** is the first page to open in a notebook if you have no history yet. It can be accessed with the icon button for the home page and the <Alt><Home> key binding. Typically the home page should be an index page linking to other pages.

The notebook **Icon** is an image that is used together with the name to identify the notebook.

The **Document Root** is a special folder containing documents that can be linked to from the notebook. To link files in this folder start the links with a "/" (see [[Links]] for more details). This folder is typically used for notebooks to be published as a webpage. When [[Export|exporting]] the notebook to HTML, the document root can be mapped as a special URL.

The property **Prefer short names for page links** controls the behavior e.g. when pasting a page link. When enabled a link like "''CustomerA:ProjectB''" will be inserted with "''ProjectB''" as link text.

When the property **Do not use system trash for this notebook** is enabled, the "//Delete page//" menu action will perform a permanent delete instead of a moving files to trash.
