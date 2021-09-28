import gc
import PySimpleGUI as sg


class Window:
    sg.theme('DarkBlue8')
    layout = []
    window = None
    @classmethod
    def init(cls):
        pass

    @classmethod
    def report(cls, log):
        print(f"[{cls.__name__}]> {log}")

    @classmethod
    def run_loop(cls):
        if cls.window is None:
            cls.init()

    @classmethod
    def close(cls):
        try:
            cls.window.close()
        except AttributeError:
            pass
        cls.layout = None
        cls.window = None
        gc.collect()
