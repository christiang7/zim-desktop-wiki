====== Superior Table Operations ======

===== Markup in a cell =====
The main toolbar buttons for formatting are disabled. You have to know the special syntax and insert it directly within the textbox.
While editing:		{{./cell_editing_with_text_formatting.png}}
After formatting: 	{{./cell_after_text_formatting.png}}

==== Common formats ====
**bold**, //italic//, __highlight__, ~~strike through and~~ and ''verbatim''

'''
**bold**, //italic//, __highlight__, ~~strike through~~ and ''verbatim''
'''


==== Special characters ====
\\n		Newline
\|		| Character

==== Links in a  cell ====
'''
[[http://www.python.org]]
[[http://www.python.org\|Python homepage]]
[[foo@bar.org]]
[[foo]]		Internal Link
'''

Note: Only **one link per cell** can be opened. The first one is taken.
A link can be accessed with:
* ''RIGHT MOUSE-BUTTON-CLICK'' on cell with the link  and selection of the menu item //Open cell in content link//
* ''CTRL + LEFT MOUSE-BUTTON-CLICK'' on a cell

See also:	[[manual:Help:Links|Syntax for Links]]

===== Exporting: =====
Exporting filters for Plain, HTML, Markdown, reStructuredText, Latex has been also adjusted for the table plugin.

===== Limits of widget's integration =====
* search / replacing:
	* no highlighting
	* only the first location is found and after that the next one within the main text
* Undo / Redo not supported at all
* There can not be any element right or left to the table. The table must stand alone.
