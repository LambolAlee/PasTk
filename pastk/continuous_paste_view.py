import PySimpleGUI as sg
from pyperclip import copy
from .helpers.helper import copier
from .abstract_window import Window
from .helpers.auto_paste_service import AutoPasteManager as apm


class ContinueWindow(Window):
    over = False

    @classmethod
    def init(cls):
        cls.window = sg.Window('连续粘贴模式', layout=cls.build(), keep_on_top=True, finalize=True)
        cls.update_button_text()
        cls.window.TKroot.bind("<FocusOut>", cls.on_focus_in)

    @classmethod
    def on_focus_in(cls, event):
        cls.window.TKroot.focus_set()

    @classmethod
    def build(cls):
        cls.layout = [
            [sg.Frame('', [
                [sg.B('Hello World', font=('PingFang', 16), size=(20, 2), enable_events=True, k='-C_PASTE-')],
                [sg.B('不贴了，退出', size=(26, 1), enable_events=True, k='-C_QUIT-')]
            ], element_justification='center')]
        ]
        return cls.layout

    @classmethod
    def update_button_text(cls):
        text = copier[0]
        if len(copier) == 1:
            text = '已全部贴完！'
            cls.over = True
        else:
            if len(text) > 27:
                text = text.strip().replace('\n', '  ')
                text = text[:27] + '...'
        cls.window['-C_PASTE-'].update(text=text)

    @classmethod
    def loop(cls):
        cls.over = False
        window = cls.window

        while True:
            e, _ = window.read()

            if e in (sg.WINDOW_CLOSED, '-C_QUIT-'):
                break

            elif e == '-C_PASTE-':
                if cls.over:
                    break
                window.hide()
                cls.update_button_text()
                copy(copier.pop(0))
                apm.order(window)

            elif e == '*EXECUTED*':
                window.un_hide()

