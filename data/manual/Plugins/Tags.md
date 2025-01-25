====== Tags ======

This plugin adds a tag cloud and a page index organized by tags in the side pane.

The tag cloud allows toggling the selection of tags that are shown in the page index. The page index can be switched between a flat view, showing all pages that match the filtering criteria, and an ordered view that shows known tags as the top-level nodes with pages beneath them.

**Dependencies:** This plugin has no additional dependencies.

**See also: **[[Help:Tags]]

===== Options =====

The option **Position in the window** determines in which side pane the tag list is shown.

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

===== Usage =====
The tag index has 3 views:

1. The normal index listing all pages by hierarchy
2. Index organized by tag with tags as the top level of the hierarchy
3. The index filtered by a given set of tags, showing all matching top-level pages

When no tags are selected, you can switch between 1. and 2. via an option in the context menu ('Right click menu') called **Sort pages by tags**.
Both views switch to 3. when you select tags in the tagcloud for filtering.


===== Style =====

This plugin uses widget names to allow CSS styling for the floating widget:

* zim-pageindex: for the main treeview
* zim-tags-tagcloud: for the textview that renders the tag cloud

See [[Help:Config Files]] for info on CSS styling
