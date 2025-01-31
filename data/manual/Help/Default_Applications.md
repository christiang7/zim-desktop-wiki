====== Default Applications ======

Zim opens files and attachments with other applications. Usually clicking on a link will start the appropriate application for your system. And the "//Open With...//" menu in the context menu (click the right mouse button on the link) gives alternative applications.

If you want to change the default application, or you want to add additional applications to the "//Open With...//" menu, there is a menu item "//Customize...//" at the bottom of the popup. This item brings up a dialog that allows changing the default application and adding new applications.

===== Configure Applications Dialog =====
The //Configure Applications //dialog has a drop-down menu to choose a default application. Applications zim knows about are shown in this drop-down. Also, there is a special menu item "**System Default**" which means to use whatever application is the default used by the operating system.

Note that there may be applications installed that zim does not know about. Setting the default to "**System Default**" may result in the correct application being used, even if it is not shown in the list.

To add applications to the list (and to the "//Open With...//" menu) click the button "**Add Application**", this will bring up the //Add New Application// dialog.

===== Add Application Dialog =====
The //Add Application// dialog allows adding a new application for a specific file type.

The **Name** is the application name and **Command** is the command to execute. Usually, this is just the name of an executable or a script to execute. The command can also use the following special codes:

* **%f** a single file path to be opened
* **%F** a list of file paths to be opened
* **%u** a single URL to be opened
* **%U** a list of URLs to be opened
* **%c** the application name

If "**Make default application**" is enabled the new application will become the new default. This implies that it does not show up in the menu itself. If this is not set the new application will just be added to the menu.

The quoting of the command should follow the "XDG Desktop Entry" specification. In short:
* Arguments can be quoted in full with double quotes
* Arguments containing reserved characters must be quoted - these are: '"', "'", "`", "`" "\", " ", "\t", "\n", ">", "<", "~", "|", "&", ";", "$", "*", "?", "#", "(" and ")"
* Within quoted arguments quotes and other reserved characters should be escaped with a backslash e.g. '\"'
* Within quoted arguments a literal backslash is written as a double backslash ''\\'

Zim is tolerant for reserved characters in arguments that are not quoted, and does not process escape sequences in arguments that are not quoted. However for interoperability with other applications the above rules should be followed.

The special codes that do expand to a single argument can also appear inside (quoted) arguments. This behavior is unspecified in the specification. Be aware that no whitespace escaping and other escaping is done with this replacement.


===== Technical Details =====
Zim uses the XDG Desktop Entry spec to store and retrieve application information. The default application per mimetype is stored in a file in the ''XDG_CONFIG_HOME'' folder, typically ''~/.config/mimeapps.list'' according to the "mime-apps-spec". In the same file, you can also
add or remove (blacklist) applications to be shown in the "Open With" menu for a given
mimetype.

To populate the "//Open With...//" menu first the ''mimeapps.list'' is read. In addtion zim searches the ''XDG_DATA_HOME/share/applications/'' and ''XDG_DATA_DIRS/share/applications/'' folders for a "''mimeinfo.cache''" file which lists applications per mimetype. Applications are configured via ''.desktop'' files that should reside in the same folder as the cache file.

When the user adds a new application zim creates a new ''.desktop'' file in the XDG_DATA_HOME folder and updates the cache. Next time it lists applications for a specific type, this entry will show up. For a new default application we also update ''defaults.list'', but the desktop entry has a "''NoDisplay''" set, so it is hidden from the menu.

Zim uses the XDG MimeInfo spec or the ''mimetypes'' module to determine file types. As an extension for URL and URI schemes the "''x-scheme-handler/''" mimetype is used. So "''x-scheme-handler/http''" is used to configure the webbrowser, "''x-scheme-handler/mailto''" for the email client, etc.

If no default application is found, zim uses operating system-specific fallbacks. For files and email this mean calling "''os.startfile()''" on Windows, the "''open''" command on OSX, and the "''xdg-open''" and "''xdg-email''" commands on Linux and unix other systems. For URLs the "''webbrowser''" module is used as generic fallback. The "''webbrowser''" module is also used for files and email when e.g. the "''xdg-open''" or "''xdg-email''" commands are not found. (The ''webbrowser'' module does not only check specific browsers but also tries system APIs that handle files as well.)

So on Windows, zim uses the XDG system to store application preferences, even though this is not the native system on windows. The fallback is an API (''os.startfile()'') that uses applications known to the Windows registry. As a result zim will just use the default installed applications on Windows, but this can be overruled by installing Desktop Entry files.

If you want to clean up custom application entries, have a look at the folder ''~/.local/share/applications'' (or the equivalent ''XDG_DATA_HOME'' folder)

See [[Config Files]] for an overview of the various XDG file paths.

The XDG Desktop Entry spec and the XDG MimeInfo spec can be found here: https://www.freedesktop.org/wiki/Specifications
