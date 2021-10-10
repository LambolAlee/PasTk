import PySimpleGUI as sg

from .abstract_window import Window
from .helpers.helper import music_dir
from .config.configure import configure
from .config.system_manager import platform
from .helpers.helper import playsound_thread


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
        launch_music_layout = cls.generate_simple_setting('launch_music')
        launch_music_layout.append(cls.generate_play_button('LAUNCH'))
        over_music_layout = cls.generate_simple_setting('over_music')
        over_music_layout.append(cls.generate_play_button('OVER'))
        settings_tab = [
            cls.generate_simple_setting('one_piece'),
            launch_music_layout,
            over_music_layout,
            [sg.T('Music: ', font=platform.get_font('setting_text')), sg.Checkbox('', default=cls.music.music_enabled, k='-CHECK-', enable_events=True), 
            sg.Combo(cls.music.musics, size=(10,1), font=platform.get_font('setting_text'), enable_events=True, k='-MUSIC_SELECT-'), 
            cls.generate_play_button('HINT'), sg.Button('open', font=platform.get_font('button'), k='-OPEN-', enable_events=True)],
            [sg.T(' ')], 
            [sg.B('Save', font=platform.get_font('setting_button'), disabled=True, k='-SAVE-', enable_events=True, disabled_button_color='#cccccc'), sg.B('Quit', font=platform.get_font('setting_button'), k='-QUIT-', enable_events=True)]
        ]

        about_tab = [
            [sg.T('PasTk', font=platform.get_font('big'), text_color='white')],
            [sg.T('Written in python using PySimpleGUI')]
        ]

        cls.layout = [
            [sg.TabGroup([[sg.Tab('Settings', settings_tab), sg.Tab('About', about_tab)]], font=platform.get_font('hint'))]
        ]
        return cls.layout

    @staticmethod
    def generate_simple_setting(name: str):
        hint = name.replace('_', ' ').capitalize() + ': '
        return [sg.T(hint, font=platform.get_font('setting_text')), sg.Checkbox(on_off_state[configure[name].active_value], default=configure[name].active_value, font=platform.get_font('hint'), k=name.upper(), enable_events=True)]

    @staticmethod
    def generate_play_button(type_):
        return sg.B('play', font=platform.get_font('setting_button'), k=f'-PLAY_{type_}_MUSIC-', enable_events=True)

    @classmethod
    def update_music_state(cls, state):
        cls.window['-SAVE-'].update(disabled=not cls.music.is_modified())
        cls.window['-MUSIC_SELECT-'].update(disabled=not state, value=cls.music.music_selected)

    @classmethod
    def set_default_music(cls):
        cls.music.set_default_music()
        cls.window['-MUSIC_SELECT-'].update(values=cls.music.musics)

    @classmethod
    def loop(cls):
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

            elif e in ('ONE_PIECE', 'LAUNCH_MUSIC', 'OVER_MUSIC'):
                configure[e.lower()].active_value = v[e]
                window['-SAVE-'].update(disabled=not configure.is_modified(e.lower()))
                window[e].update(text=on_off_state[v[e]])

            elif e.endswith('_MUSIC-'):
                type_ = e.split('_')[1]
                if type_ == 'HINT':
                    playsound_thread(cls.music.music_path)
                elif type_ == 'LAUNCH':
                    # No modification is provided for the time being
                    playsound_thread(music_dir / 'launch' / 'launch_music.mp3')
                else:
                    # No modification is provided for the time being
                    playsound_thread(music_dir / 'launch' / 'over_music.wav')

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
