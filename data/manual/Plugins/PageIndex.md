====== PageIndex ======
This plugin provides the page index side pane for the main window.

**Dependencies:** This plugin has no additional dependencies.

===== Options =====
The option **Position in the window** determines in which side pane the browser is shown.

The option **Use drag&drop to move pages in the notebook** determines whether
you can use drag&drop on the page index to re-arrange pages in the notebook.

The option **Automatically expand sections on open page** determines whether
the section for the current page is automatically expanded.

The option **Automatically collapse sections on close page** determines whether
sections that are automatically expanded are also collapsed again on moving
away from the page. It does not affect sections that were expanded manually
by clicking on the expand arrow.

The option **Use horizontal scrollbar (may need restart)** sets the preference whether to use
horizontal scrolling or not. Without horizontal scrollbar long page names get
shortened by ellipsis ("..."). When you change this option, you may need to
restart Zim to see the correct rendering.

The option **Use tooltips** allows toggling whether or not tooltips are shown
for pages in the index.

===== Style =====

This plugin uses a widget name to allow CSS styling for the floating widget:

* zim-pageindex: for the main treeview

See [[Help:Config Files]] for info on CSS styling
