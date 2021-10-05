import PySimpleGUI as sg

from .abstract_window import Window
from .helpers.helper import music_dir
from .helpers.configure import configure

FONT2 = ('PingFang', 16)

on_off_state = {True: 'enabled', False: 'disabled'}

class ConfigWindow(Window):
    music = configure['music']

    @classmethod
    def init(cls):
        cls.window = sg.Window('连续复制-设置', layout=cls.build(), enable_close_attempted_event=True, finalize=True)
        if cls.music.music_enabled:
            if not cls.music.check_availability():
                sg.popup_error(f"所选音乐{cls.music.music_selected}不可用，已禁用", "如有需要，请检查音乐文件夹并手动开启音乐！", title='连续复制-设置')
                cls.music.music_enabled = False
                configure.save()
            else:
                cls.window['-MUSIC_SELECT-'].update(value=cls.music.music_selected)
        cls.window['-MUSIC_SELECT-'].update(disabled=not cls.music.music_enabled)
        cls.window['-CHECK-'].update(cls.music.music_enabled)

    @classmethod
    def build(cls):
        settings_tab = [
            [sg.T('One Piece: ', font=FONT2), sg.Checkbox('enabled' if configure['one_piece'] else 'disabled', default=configure['one_piece'], k='-ONE-', enable_events=True)],
            [sg.T('Music: ', font=FONT2), 
            sg.Combo(cls.music.musics, size=(10,1), readonly=True, font=FONT2, enable_events=True, k='-MUSIC_SELECT-'), 
            sg.Button('open', font=('PingFang', 12), k='-OPEN-', enable_events=True), sg.Checkbox('', default=cls.music.music_enabled, k='-CHECK-', enable_events=True)],
            [sg.T(' ')], 
            [sg.B('Save', font=('PingFang', 12), disabled=True, k='-SAVE-', enable_events=True, disabled_button_color='#cccccc'), sg.B('Quit', font=('PingFang', 12), k='-QUIT-', enable_events=True)]
        ]

        about_tab = [
            [sg.T('PasTk', font=('PingFang', 32), text_color='white')],
            [sg.T('Written in python using PySimpleGUI')]
        ]

        cls.layout = [
            [sg.TabGroup([[sg.Tab('Settings', settings_tab), sg.Tab('About', about_tab)]], font=('PingFang', 12))]
        ]
        return cls.layout

    @classmethod
    def update_music_state(cls, state):
        cls.window['-SAVE-'].update(disabled=not cls.music.is_modified())
        cls.window['-MUSIC_SELECT-'].update(disabled=not state, readonly=False, value=cls.music.music_selected)
        cls.window['-MUSIC_SELECT-'].update(readonly=True)

    @classmethod
    def set_default_music(cls):
        cls.music.set_default_music()
        cls.window['-MUSIC_SELECT-'].update(values=cls.music.musics)

    @classmethod
    def run_loop(cls):
        super().run_loop()

        cls.modified = False
        window = cls.window

        while True:
            e, v = window.read()

            if e in (sg.WINDOW_CLOSE_ATTEMPTED_EVENT, '-QUIT-'):
                if cls.music.is_modified():
                    res = sg.popup_yes_no('是否保存修改', title='连续复制-设置', keep_on_top=True)
                    if res is None:
                        continue
                    elif res == 'Yes':
                        configure.save()
                    else:
                        configure.rollback()
                window.hide()
                break

            if e == '-MUSIC_SELECT-':
                if v[e] != cls.music.music_selected:
                    cls.music.music_selected = v[e]
                    cls.window['-SAVE-'].update(disabled=not cls.music.is_modified())

            elif e == '-SAVE-':
                configure.save()
                cls.window['-SAVE-'].update(disabled=True)

            elif e == '-ONE-':
                configure['one_piece'] = v[e]
                window['-SAVE-'].update(disabled=not configure.is_modified('one_piece'))
                window['-ONE-'].update(text=on_off_state[v[e]])

            elif e == '-CHECK-':
                cls.music.music_enabled = v[e]
                if v[e]:
                    if cls.music.check_has_musics_with_refresh():
                        if not cls.music.check_music_selected():
                            cls.set_default_music()
                    else:
                        sg.popup_ok('没有在音乐文件夹下找到合适的音乐文件，请放入音乐后再尝试开启此选项', title='连续复制-告示')
                        window['-CHECK-'].update(False)
                        cls.music.music_enabled = False
                        continue
                cls.update_music_state(v[e])

            elif e == '-OPEN-':
                try:
                    from os import startfile
                    startfile(cls.music_dir)
                except ImportError:
                    from subprocess import call
                    call(['open', music_dir])
