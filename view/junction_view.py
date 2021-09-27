import PySimpleGUI as sg
from pyperclip import copy
from .helper import copier, FONT, auto_paste, notify


def merge():
    e, v = sg.Window('合并粘贴模式', layout=[[sg.T('请输入连接符', font=FONT)], [sg.Input(font=FONT, size=(20, 1))], [sg.Ok(font=('', 12)), sg.Cancel(font=('', 12))]], finalize=True).read(close=True)
    if not (e is None or e == 'Cancel'):
        copy(v[0].join(copier))
        auto_paste()
        notify('合并粘贴模式')

def subsection():
    copy('\n'.join(copier))
    auto_paste()
    notify('分段粘贴模式')
