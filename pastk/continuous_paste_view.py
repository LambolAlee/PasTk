import PySimpleGUI as sg
from pyperclip import copy
from .config.configure import tr
from .helpers.helper import copier
from .abstract_window import Window
from .config.system_manager import platform
from .helpers.auto_paste_service import AutoPasteManager as apm


class ContinueWindow(Window):
    over = False

    @classmethod
    def init(cls):
        cls.window = sg.Window(tr('连续粘贴模式'), layout=cls.build(), keep_on_top=True, finalize=True)
        cls.window['-C_PASTE-'].update(text=cls.wrap(copier[0]))

    @classmethod
    def build(cls):
        cls.layout = [
            [sg.Frame('', [
                [sg.B('Hello World', font=platform.get_font('setting_text'), size=(20, 2), enable_events=True, k='-C_PASTE-')],
                [sg.B(tr('不贴了，退出'), size=(26, 1), enable_events=True, k='-C_QUIT-')]
            ], element_justification='center')]
        ]
        return cls.layout

    @staticmethod
    def wrap(text):
        if len(text) > 27:
            text = text.strip().replace('\n', '  ')
            text = text[:27] + '...'
        return text

    @classmethod
    def update_button_text(cls):
        if len(copier) == 0:
            text = tr('已全部贴完！')
            cls.over = True
        else:
            text = cls.wrap(copier[0])
        cls.window['-C_PASTE-'].update(text=text)

    @classmethod
    def loop(cls, parent=None):
        cls.over = False
        window = cls.window

        while True:
            e, _ = window.read()

            if e in (sg.WINDOW_CLOSED, '-C_QUIT-'):
                break

            elif e == '-C_PASTE-':
                if cls.over: break
                window.hide()
                copy(copier.pop(0))
                cls.update_button_text()
                apm.order(window)

            elif e == '*EXECUTED*':
                window.un_hide()
