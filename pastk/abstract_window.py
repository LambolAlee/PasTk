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
    def build(cls):
        return cls.layout

    @classmethod
    def report(cls, log):
        print(f"[{cls.__name__}]> {log}")

    @classmethod
    def run_loop(cls, parent: sg.Window=None):
        def run():
            if cls.window is None:
                cls.init()
            else:
                cls.window.un_hide()
            return cls.loop()

        if parent is not None:
            parent.hide()
            ret = run()
            parent.un_hide()
        else:
            ret = run()
        return ret

    @classmethod
    def loop(cls):
        pass

    @classmethod
    def close(cls):
        try:
            cls.window.close()
        except AttributeError:
            pass
        cls.layout = None
        cls.window = None
        gc.collect()
        cls.report('closed')
