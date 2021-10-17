import PySimpleGUI as sg

from pyperclip import copy
from .config.configure import tr
from .helpers.helper import copier
from .abstract_window import Window
from .config.system_manager import platform
from .helpers.auto_paste_service import AutoPasteManager as apm


class SelectionWindow(Window):

    @classmethod
    def init(cls):
        cls.window = sg.Window(tr('选择粘贴模式'), layout=cls.build(), keep_on_top=True, finalize=True)

    @classmethod
    def build(cls):
        cls.layout = [
            [sg.Listbox(copier, select_mode="LISTBOX_SELECT_MODE_SINGLE", size=(28, 10), no_scrollbar=True, font=platform.get_font('setting_text'), k='-S_LIST-', enable_events=True)],
            [sg.B(tr('不贴了，退出'), size=(30, 1), k='-S_QUIT-', enable_events=True)]
        ]
        return cls.layout

    @classmethod
    def loop(cls, parent=None):
        cls.over = False
        window = cls.window

        while True:
            e, v = window.read()

            if e in (sg.WINDOW_CLOSED, '-S_QUIT-'):
                break

            elif e == '-S_LIST-':
                window.hide()
                value = v[e][0]
                copy(value)
                apm.order(window)

            elif e == '*EXECUTED*':
                window.un_hide()
