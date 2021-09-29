import PySimpleGUI as sg

from .abstract_window import Window
from .helpers.configure import configure
from .helpers.helper import FONT, music_dir

FONT2 = ('', 16)

class ConfigWindow(Window):
    modified = False

    @classmethod
    def init(cls):
        cls.window = sg.Window('连续复制-设置', layout=cls.build(), enable_close_attempted_event=True, finalize=True)
        if configure['music'].music_selected:
            cls.window['-MUSIC_SELECT-'].update(value=configure['music'].music_selected)
        cls.window['-MUSIC_SELECT-'].update(disabled=not configure['music'].music_enabled)

    @classmethod
    def build(cls):
        settings_tab = [
            [sg.T('Music: ', font=FONT2), 
            sg.Combo(configure['music'].musics, size=(10,1), readonly=True, font=FONT2, enable_events=True, k='-MUSIC_SELECT-'), 
            sg.Button('open', font=FONT2, k='-OPEN-', enable_events=True), sg.Checkbox('', default=configure['music'].music_enabled, k='-CHECK-', enable_events=True)],
            [sg.B('Save', font=FONT, disabled=True, k='-SAVE-', enable_events=True, disabled_button_color='#cccccc'), sg.B('Quit', font=FONT, k='-QUIT-', enable_events=True)]
        ]

        about_tab = [
            [sg.T('PasTk', font=('', 32), text_color='white')],
            [sg.T('Written in python using PySimpleGUI', font=('', 14))]
        ]

        cls.layout = [
            [sg.TabGroup([[sg.Tab('Settings', settings_tab), sg.Tab('About', about_tab, font=FONT)]])]
        ]
        return cls.layout

    @classmethod
    def update_state(cls, comp, raw):
        cls.modified = True if comp != raw else False
        cls.window['-SAVE-'].update(disabled=not cls.modified)

    @classmethod
    def run_loop(cls):
        super().run_loop()

        cls.modified = False
        window = cls.window

        while True:
            e, v = window.read()

            if e in (sg.WINDOW_CLOSE_ATTEMPTED_EVENT, '-QUIT-'):
                if cls.modified:
                    res = sg.popup_yes_no('是否保存修改', title='连续复制-设置', font=FONT, keep_on_top=True)
                    if res is None:
                        continue
                    elif res == 'Yes':
                        configure.save()
                    else:
                        configure.rollback()
                break

            if e == '-MUSIC_SELECT-':
                if v[e] != configure['music'].music_selected:
                    configure['music'].music_selected = v[e]
                    cls.update_state(v[e], configure['music'].data['music_selected'])

            elif e == '-SAVE-':
                configure.save()
                cls.modified = False
                cls.window['-SAVE-'].update(disabled=True)

            elif e == '-CHECK-':
                configure['music'].music_enabled = v[e]
                if v[e] and not configure['music'].music_enabled:
                    if configure['music'].musics:
                        configure['music'].music_selected = configure['music'].musics[0]
                        configure['music'].music_enabled = True
                        window['-MUSIC_SELECT-'].update(values=configure['music'].musics)
                    else:
                        sg.popup_ok('没有在音乐文件夹下找到合适的音乐文件，请放入音乐后再尝试开启此选项', title='连续复制-告示', font=FONT)
                        window['-CHECK-'].update(False)
                        continue
                cls.update_state(v[e], configure['music'].data['enabled'])
                window['-MUSIC_SELECT-'].update(disabled=not v[e], readonly=False, value=configure['music'].music_selected)
                window['-MUSIC_SELECT-'].update(readonly=True)
            
            elif e == '-OPEN-':
                try:
                    from os import startfile
                    startfile(music_dir)
                except ImportError:
                    from subprocess import call
                    call(['open', music_dir])
