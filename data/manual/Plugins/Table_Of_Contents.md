====== Table Of Contents ======

This plugin adds a widget with a Table Of Contents for the current page. It can be either in the side pane or "floating" on top of the page. The Table Of Contents gives an outline of all headings in the page and allows modifying this outline (try the context menu).

**Dependencies:** This plugin has no additional dependencies.

===== Options =====
The option **Position in the window** determines in which side pane the table is shown.

Alternatively, if the option **Show ToC as floating widget instead of in sidepane** is enabled the table is shown on top of the page view. If the table of contents is shown as a floating widget, it will only be visible when the current page has one or more headings. When the table of contents is empty, the floating widget is hidden.

By default, the page title is not shown in the table of contents (unless there are multiple title headings in the page). If the option **Show the page title heading in the ToC** is enabled the page title will always be shown in the table of contents.

The table of contents also shows horizontal lines as these are considered breaks between sections.
The option **Include horizontal lines in the ToC** can be used to change this behavior.

The option **Set ToC fontsize** allows setting the fontsize of the floating ToC. Set it to 0 to leave this unset. In this case, the size of the ToC follows the global font-size. (You may need to disable and re-enable the plugin to see the effect.)


===== Style =====

This plugin uses two widget names to allow CSS styling for the floating widget:

* zim-toc-widget: for the whole floating widget; the default is to render a small border line
* zim-toc-head: for the top bar of the widget; the default is to render a small border line at the bottom

See [[Help:Config Files]] for info on CSS styling
