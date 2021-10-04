import PySimpleGUI as sg
from pyperclip import copy
from .helpers.helper import auto_paste, copier


def merge():
    e, v = sg.Window('合并粘贴模式', layout=[[sg.T('请输入连接符')], [sg.Input(size=(20, 1))], [sg.Ok(font=('', 12)), sg.Cancel(font=('', 12))]], keep_on_top=True, finalize=True).read(close=True)
    if not (e is None or e == 'Cancel'):
        copy(v[0].join(copier))
        auto_paste()


def subsection():
    copy('\n'.join(copier))
    auto_paste()
