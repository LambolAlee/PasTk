import PySimpleGUI as sg
from queue import Queue
from pyperclip import copy
from .abstract_window import Window
from .helpers.helper import copier
from .helpers.auto_paste_service import AutoPasteManager as apm


class SelectionWindow(Window):
    over = False

    @classmethod
    def init(cls):
        cls.window = sg.Window('选择粘贴模式', layout=cls.build(), keep_on_top=True, finalize=True)

    @classmethod
    def build(cls):
        cls.layout = [
            [sg.Listbox(copier, select_mode="LISTBOX_SELECT_MODE_SINGLE", size=(28, 10), no_scrollbar=True, font=('', 16), k='-S_LIST-', enable_events=True)],
            [sg.B('不贴了，退出', size=(30, 1), k='-S_QUIT-', enable_events=True)]
        ]
        return cls.layout

    @classmethod
    def update_list(cls, value):
        copier.remove(value)
        if copier == []:
            cls.over = True
            copier.append('已全部贴完！')
        cls.window['-S_LIST-'].update(values=copier)

    @classmethod
    def run_loop(cls):
        super().run_loop()
        window = cls.window

        while True:
            e, v = window.read()

            if e in (sg.WINDOW_CLOSED, '-S_QUIT-'):
                break

            elif e == '-S_LIST-':
                if cls.over: break
                window.hide()
                value = v[e][0]
                cls.update_list(value)
                copy(value)
                apm.order(window)

            elif e == '*EXECUTED*':
                window.un_hide()
