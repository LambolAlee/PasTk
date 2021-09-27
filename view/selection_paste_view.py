import PySimpleGUI as sg
from queue import Queue
from pyperclip import copy
from .abstract_window import Window
from .helper import copier, FONT, auto_paste_servive


class SelectionWindow(Window):
    over = False
    shorten_list = []
    queue = Queue(3)
    service_thread = None
    layout = [
        [sg.Listbox(copier, select_mode="LISTBOX_SELECT_MODE_SINGLE", size=(28, 10), no_scrollbar=True, font=('', 16), k='-S_LIST-', enable_events=True)],
        [sg.B('不贴了，退出', size=(30, 1), k='-S_QUIT-', enable_events=True, font=FONT)]
    ]

    @classmethod
    def init(cls):
        cls.window = sg.Window('选择粘贴模式', layout=cls.layout, keep_on_top=True, finalize=True)
        cls.service_thread = auto_paste_servive(cls.window, cls.queue)
        cls.service_thread.start()

    @classmethod
    def _update_list(cls, value):
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
                cls.queue.put('q')
                cls.service_thread.join()
                break

            elif e == '-S_LIST-':
                value = v[e][0]
                if cls.over: 
                    cls.window['-S_QUIT-'].click()
                    continue
                copy(value)
                window.hide()
                cls.queue.put('execute')
                cls._update_list(value)

            elif e == '*EXECUTED*':
                window.un_hide()
