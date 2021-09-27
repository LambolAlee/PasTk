import PySimpleGUI as sg
from pyperclip import copy
from queue import Queue
from .helper import copier, FONT, auto_paste_servive
from .abstract_window import Window


class ContinueWindow(Window):
    over = False
    queue = Queue(3)
    service_thread = None
    layout = [
        [sg.Frame('', [
            [sg.B('Hello World', font=('', 16), size=(20, 2), enable_events=True, k='-C_PASTE-')],
            [sg.B('不贴了，退出', font=FONT, size=(26, 1), enable_events=True, k='-C_QUIT-')]
        ], element_justification='center')]
    ]

    @classmethod
    def init(cls):
        cls.window = sg.Window('连续粘贴模式', layout=cls.layout, keep_on_top=True, finalize=True)
        cls.update_button_text()
        cls.service_thread = auto_paste_servive(cls.window, cls.queue)
        cls.service_thread.start()

    @classmethod
    def update_button_text(cls):
        try:
            text = copier[0]
        except IndexError:
            text = '已全部贴完！'
            cls.over = True
        else:
            if len(text) > 27:
                text = text.strip().replace('\n', '  ')
                text = text[:27] + '...'
        cls.window['-C_PASTE-'].update(text=text)

    @classmethod
    def run_loop(cls):
        super().run_loop()
        window = cls.window

        while True:
            e, _ = window.read()

            if e in (sg.WINDOW_CLOSED, '-C_QUIT-'):
                cls.queue.put('q')
                cls.service_thread.join()
                break

            elif e == '-C_PASTE-':
                if cls.over:
                    cls.window['-C_QUIT-'].click()
                    continue
                copy(copier.pop(0))
                window.hide()
                cls.queue.put('execute')
                cls.update_button_text()

            elif e == '*EXECUTED*':
                window.un_hide()
