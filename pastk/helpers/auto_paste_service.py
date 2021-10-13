import pyautogui as auto
import PySimpleGUI as sg

from time import sleep
from queue import Queue
from functools import wraps
from threading import Thread
from ..config.system_manager import platform


def auto_paste_service(func):
    @wraps(func)
    def wrapper():
        apm = AutoPasteManager().start()
        try:
            func()
        finally:
            apm.stop()
    return wrapper


class AutoPasteManager:
    thread = None
    paste_order = Queue(3)
    paste_done = Queue(3)

    @staticmethod
    def paste():
        if platform.sys_name == 'Darwin':
            platform.app.hide()
        sleep(1)
        auto.hotkey(*platform.paste_keys)

    @classmethod
    def order(cls, window: sg.Window=None):
        order = window if window is not None else 'go ahead'
        cls.paste_order.put(order)

    @classmethod
    def wait(cls):
        return cls.paste_done.get()

    def start(self):
        def service():
            self.report('start listening...')
            while True:
                sig = self.paste_order.get()

                if sig == 'quit':
                    self.report('apm quitting...')
                    return

                self.report('pasting...')
                self.paste()

                if isinstance(sig, sg.Window):
                    sleep(.2)
                    sig.write_event_value('*EXECUTED*', True)
                else:
                    sleep(.2)
                    self.paste_done.put('executed')

        self.thread = Thread(target=service, name='AutoPaste_Service')
        self.thread.start()
        return self

    def stop(self):
        if not self.thread is None and self.thread.is_alive():
            self.paste_order.put('quit')
            self.thread.join()
            self.thread = None

    def report(self, log):
        print(f"*[{self.__class__.__name__}]* {log}")
