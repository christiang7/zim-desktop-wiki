====== Key Bindings ======

See also [[Menu Items]].

==== General ====

'''
F9		Toggle visibility of sidepane(s)
<Ctrl>F9	Show all sidepanes
<Ctrl><Space>	Toggle focus between index and buffer
			opens side pane if index is invisible
		(optional see preferences)
<Ctrl><Tab>	Focus next inteface element (gtk default)
<Ctrl><Shift><Tab> Focus previous interface element (gtk default)
Esc		Close sidepane (when focus is on a side pane)
'''


'''
<Alt><Home>	Go to the home page
<Alt><Left>	Go one page back in history
<Alt><Right>	Go one page forward in history
<Alt><Up>	Go one level up in the page hierarchy
<Alt><Down>	Go one page down in the page hierarchy
		(The actual page is chosen by the history)
<Alt><PgUp>	Go to the previous page in the index
<Alt><PgDown>	Go to the next page in the index
<Alt>D		Go to today's page
'''


'''
<Ctrl>Q		Quit the application
<Ctrl>w		Close window
'''


'''
<Ctrl>F		Find in the current page
<Ctrl>G		Find next
<Shift><Ctrl>G	Find previous
<Shift><Ctrl>F  Search in all pages
<Ctrl>H		Find and Replace
'''


'''
<Ctrl>S		Save page        (forced)
<Shift><Ctrl>S	Save version...
<Ctrl>R		Reload page      (saves first)
<Ctrl>J		Jump to page...  (either an existing or a new page)
'''


'''
<Ctrl>L		Link selected text
		Follow selected text as a link when read-only
<Shift><Ctrl>L	Copy a link to the current page to the clipboard
		In the side pane copies a link to the selected page
		(Paste this link in a page with <Ctrl>V)
<Ctrl>E		Show the "edit link" dialog
<Ctrl>D		Inserts timestamp
'''


'''
<Ctrl>1..<Ctrl>5 Make selected text a heading
<Ctrl>9		Make selected text normal
<Ctrl>B		Make selected text strong
<Ctrl>I		Make selected text italic
<Ctrl>U		Make selected text underline     (renders highlighted)
<Ctrl>K		Make selected text strike-trough
<Ctrl>T		Make selected text verbatim text (monospace font)
'''


'''
<Ctrl>Z		Undo
<Shift><Ctrl>Z	Redo
<Ctrl>Y		Redo
'''


'''
<Shift><Ctrl>D	Show the calendar dialog
'''


'''
F1		Show the manual
F2		Rename current page
F3		Find next	(same as <Ctrl>G)
<Shift>F3	Find previous	(same as <Ctrl>G)
F5		Reload page	(same as <Ctrl>R)
F12		Toggle checkbox item to 'OK'
<Shift>F12	Toggle checkbox item to 'NOK'
'''

, all the usual keybindings apply for the gtk text edit widget, thus bindings like
''<Ctrl>C'', ''<Ctrl>X'', ''<Ctrl>V'', ''<Ctrl>A'' etc. work as expected.

==== Customize Key Bindings ====
Go to "Preference" and then "Key bindings". Supported since 0.72.0.

==== Side pane tree ====
The following key bindings works when the tree in the side pane is focussed:

'''
<Ctrl>L		Insert a link to the selected page
<Shift><Ctrl>L	Copy the selected page to clipboard
<Ctrl>C		Copy the selected page to clipboard
<Ctrl>F		Search in the page list as shown
*		Expand all
\		Collapse all
'''


=== Keyboard navigation of the index ===
When you click a page in the index with the mouse, this page is opened. However, when you navigate the index with keyboard cursor keys, the page that is focused is not actually opened until you press ''<Space>'' or ''<Enter>''. This means that there will be two pages highlighted, the page that has the focus and the page that is open. The page that is open is highlighted with **bold** text, while the focus is typically highlighted in the color of your desktop theme.

==== Text selections ====
For selected text the following keybindings are added:

'''
*		Toggle bullets for selected text
>		Toggle email-style quoting for selected text
<Tab>		Indent selected text
<Shift><Tab>	Un-indents selected text
<Backspace>	Un-indents selected text
'''


