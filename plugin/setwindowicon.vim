if exists('g:loaded_setwindowicon')
	finish
endif
let g:loaded_setwindowicon = 1

au VimEnter * py3 import setwindowicon; setwindowicon.seticon()
