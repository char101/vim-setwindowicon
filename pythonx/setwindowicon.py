import vim
from os import path
from win32gui import GetActiveWindow, LoadImage, SendMessage, IMAGE_ICON, LR_LOADFROMFILE

ICON = 'gvim.ico'

WM_SETICON = 128
ICON_SMALL = 0
ICON_BIG = 1

iconhandle = None

def seticon():
    global iconhandle
    icon = findicon()
    if icon:
        iconhandle = LoadImage(0, icon, IMAGE_ICON, 16, 16, LR_LOADFROMFILE)
        if iconhandle:
            SendMessage(GetActiveWindow(), WM_SETICON, ICON_SMALL, iconhandle)

def findicon():
    dir = vim.eval("fnamemodify(getcwd(), ':p:h')")
    while True:
        iconpath = path.join(dir, ICON)
        if path.isfile(iconpath):
            return iconpath
        parent = path.dirname(dir)
        if parent == dir:
            break
        dir = parent
