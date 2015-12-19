import vim
import os
import hashlib
from os import path
from win32gui import GetActiveWindow, LoadImage, SendMessage, IMAGE_ICON, LR_LOADFROMFILE
from PIL import Image

ICON = 'project.ico'

WM_SETICON = 128
ICON_SMALL = 0
ICON_BIG = 1

OVERLAY = path.join(path.dirname(__file__), 'overlay.ico')
VIMICON = path.join(path.dirname(__file__), 'vim.ico')

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

def with_cache(op, icon):
    with open(icon, 'rb') as f:
        hash = hashlib.md5(op.__name__.encode('ascii') + f.read()).hexdigest()
    cache = path.join(os.environ['TEMP'], hash + '.ico')
    if not path.isfile(cache):
        op(icon, cache)
    return cache

def overlay_vim_to_icon(icon, cache):
    bg = Image.open(icon)
    fg = Image.open(OVERLAY)
    Image.alpha_composite(bg, fg).save(cache)

def overlay_icon_to_vim(icon, cache):
    bg = Image.open(VIMICON)
    overlay_size = 10
    overlay = Image.open(icon).resize((overlay_size, overlay_size), Image.ANTIALIAS)
    fg = Image.new('RGBA', (16, 16))
    fg.paste(overlay, (16 - overlay_size, 16 - overlay_size, 16, 16))
    Image.alpha_composite(bg, fg).save(cache)

def seticon():
    global iconhandle
    if iconhandle is not None:
        return
    icon = findicon()
    if icon:
        icon = with_cache(overlay_icon_to_vim, icon)
        iconhandle = LoadImage(0, icon, IMAGE_ICON, 16, 16, LR_LOADFROMFILE)
        if iconhandle:
            SendMessage(GetActiveWindow(), WM_SETICON, ICON_SMALL, iconhandle)
