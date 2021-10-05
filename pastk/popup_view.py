import PySimpleGUI as sg

from pyperclip import copy
from .abstract_window import Window
from .helpers.helper import copier
from .helpers.auto_paste_service import AutoPasteManager as apm


def subsection():
    copy('\n'.join(copier))
    apm.order()
    apm.wait()


class PopupMergeWindow(Window):

    @classmethod
    def init(cls):
        cls.window = sg.Window('合并粘贴模式', layout=cls.build(), keep_on_top=True, finalize=True)

    @classmethod
    def build(cls):
        cls.layout = [
            [sg.T('请输入连接符')], [sg.Input(size=(20, 1))], 
            [sg.Ok(font=('', 12)), sg.Cancel(font=('', 12))]
        ]
        return cls.layout

    @classmethod
    def run_loop(cls):
        super().run_loop()

        while True:
            e, v = cls.window.read()

            if e in (sg.WINDOW_CLOSED, 'Cancel') or e == '*EXECUTED*':
                break
            else:
                cls.window.hide()
                copy(v[0].join(copier))
                apm.order(cls.window)


class SetInputPos(Window):

    @classmethod
    def init(cls):
        cls.window = sg.Window("连续复制", layout=cls.build(), keep_on_top=True, finalize=True)

    @classmethod
    def build(cls):
        cls.layout = [
            [sg.T('请点击需要粘贴的地方')], 
            [sg.B('选好了', font=('', 12)), sg.T('自动粘贴失败仍可手动粘贴', text_color='#E6E6FA')]
        ]
        return cls.layout

    @classmethod
    def run_loop(cls):
        super().run_loop()
        cls.window.read()
