import vim
import os
import hashlib
from os import path
from win32gui import GetActiveWindow, LoadImage, SendMessage, IMAGE_ICON, LR_LOADFROMFILE
from PIL import Image

ICON = 'gvim.ico'

WM_SETICON = 128
ICON_SMALL = 0
ICON_BIG = 1

OVERLAY = path.join(path.dirname(__file__), 'overlay.ico')

iconhandle = None

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

def overlay(icon):
    with open(icon, 'rb') as f:
        hash = hashlib.md5(f.read()).hexdigest()
    cache = path.join(os.environ['TEMP'], hash + '.ico')
    if not path.isfile(cache):
        bg = Image.open(icon)
        fg = Image.open(OVERLAY)
        Image.alpha_composite(bg, fg).save(cache)
    return cache

def seticon():
    global iconhandle
    if iconhandle is not None:
        return
    icon = findicon()
    if icon:
        icon = overlay(icon)
        iconhandle = LoadImage(0, icon, IMAGE_ICON, 16, 16, LR_LOADFROMFILE)
        if iconhandle:
            SendMessage(GetActiveWindow(), WM_SETICON, ICON_SMALL, iconhandle)
