import PySimpleGUI as sg

from pyperclip import copy
from .config.configure import tr
from .helpers.helper import copier
from .abstract_window import Window
from .config.system_manager import platform
from .helpers.auto_paste_service import AutoPasteManager as apm


class PopupMergeWindow(Window):

    @classmethod
    def init(cls):
        cls.window = sg.Window(tr('合并粘贴模式'), layout=cls.build(), keep_on_top=True, finalize=True)

    @classmethod
    def build(cls):
        cls.layout = [
            [sg.T(tr('请输入连接符'))], [sg.Input(size=(20, 1))], 
            [sg.Ok(button_text=tr("确定"), font=platform.get_font('button')), sg.Cancel(button_text=tr("取消"), font=platform.get_font('button'), k='Cancel')]
        ]
        return cls.layout

    @classmethod
    def loop(cls, parent=None):

        while True:
            e, v = cls.window.read()

            if e in (sg.WINDOW_CLOSED, 'Cancel') or e == '*EXECUTED*':
                break
            else:
                cls.window.hide()
                copy(v[0].join(copier))
                apm.order(cls.window)


class PopupSubsectionWindow(Window):
    
    @classmethod
    def init(cls):
        cls.window = sg.Window(tr('分段粘贴模式'), layout=cls.build(), keep_on_top=True, finalize=True)

    @classmethod
    def build(cls):
        cls.layout = [
            [sg.T(tr('请选择分段符: ')), sg.Radio(tr('Enter换行符'), 'sep', default=True), sg.Radio(tr('Tab制表符'), 'sep')],
            [sg.Ok(button_text=tr("确定"), font=platform.get_font('button')), sg.Cancel(button_text=tr("取消"), font=platform.get_font('button'), k='Cancel')]
        ]
        return cls.layout

    @classmethod
    def loop(cls, parent=None):

        while True:
            e, v = cls.window.read()

            if e in (sg.WINDOW_CLOSED, 'Cancel') or e == '*EXECUTED*':
                break
            else:
                # v[int] in PySimpleGUI means anonymous widget's value, here point to the value of radio button 'Tab制表符'
                sep = '\t' if v[1] else '\n'
                cls.window.hide()
                copy(sep.join(copier))
                apm.order(cls.window)


class SetInputPos(Window):

    @classmethod
    def init(cls):
        cls.window = sg.Window(tr("连续复制"), layout=cls.build(), keep_on_top=True, enable_close_attempted_event=True, finalize=True)

    @classmethod
    def build(cls):
        cls.layout = [
            [sg.T(tr('请点击需要粘贴的地方'))], 
            [sg.B(tr('选好了'), font=platform.get_font('button')), sg.T(tr('自动粘贴失败仍可手动粘贴'), text_color='#E6E6FA')]
        ]
        return cls.layout

    @classmethod
    def loop(cls, parent=None):
        cls.window.read()
        cls.window.hide()
