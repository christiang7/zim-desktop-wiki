====== Checkboxes ======

Zim supports lists with checkboxes instead of bullets. These look like:

[*] item 1
[ ] item 2
	[*] item 2a
	[x] item 2b
[*] item3
[>] item4
[<] item 5

As you can see in this example checkboxes can have 5 states: [ ] open, [*] checked as completed, [x] checked as not completed,  [>] checked as moved and [<] checked as moved back. States can be toggle by clicking the checkbox with either the left mouse button or using the keyboard with ''<F12>'' and ''<shift><F12>'' respectively.

To start a checkbox list type on an empty line '''[]<space>''' or '''()<space>''', this will automatically insert an open checkbox. Similarly you can type checked checkboxes using '''[*]''' or '''(*)''' and '''[x]''' or '''(x)''' respectively, followed by '''<space>''' or '''<tab>'''. Lines that start with a checkbox behave like bullet list items, so you can indent by typing ''<tab>'' after the checkbox and when you press ''<enter>'' the new line will start with an empty checkbox automatically.

There is an option in the [[Preferences]]  to have checkbox lists behave recursively. This means that the state of items with a sublist reflects the state of all child items. Checking the parent will check all child items, and checking the last child item will check the parent item automatically.

The [[manual:Plugins:Task List|Task List plugin]] regards checkboxes as TODO items and can give an overview of all open checkboxes in a notebook.
