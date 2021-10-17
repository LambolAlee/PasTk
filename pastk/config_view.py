import PySimpleGUI as sg

from .config.configure import tr
from .abstract_window import Window
from .helpers.helper import music_dir
from .config.configure import configure
from .config.system_manager import platform
from .helpers.helper import playsound_thread


on_off_state = {True: tr('开启'), False: tr('禁用')}

class ConfigWindow(Window):
    music = configure['music']

    @classmethod
    def init(cls):
        cls.window = sg.Window(tr('连续复制-设置'), layout=cls.build(), enable_close_attempted_event=True, finalize=True)
        cls.init_music()

    @classmethod
    def init_music(cls):
        if cls.music.music_enabled:
            if not cls.music.check_availability():
                sg.popup_error(tr("所选音乐{}不可用，已禁用").format(cls.music.music_selected), tr("如有需要，请检查音乐文件夹并手动开启音乐！"), title=tr('连续复制-设置'))
                cls.music.music_enabled = False
                configure.save()
            else:
                cls.window['-MUSIC_SELECT-'].update(value=cls.music.music_selected)
        cls.window['-MUSIC_SELECT-'].update(disabled=not cls.music.music_enabled)
        cls.window['-CHECK-'].update(cls.music.music_enabled)

    @classmethod
    def build(cls):
        launch_music_layout = cls.generate_simple_setting(tr('启动音乐: '), 'launch_music')
        launch_music_layout.append(cls.generate_play_button('LAUNCH'))
        over_music_layout = cls.generate_simple_setting(tr('结束粘贴音乐: '), 'over_music')
        over_music_layout.append(cls.generate_play_button('OVER'))
        settings_tab = [
            cls.generate_simple_setting(tr('一次性模式: '), 'one_piece'),
            launch_music_layout,
            over_music_layout,
            [sg.T(tr('粘贴音乐: '), font=platform.get_font('setting_text')), sg.Checkbox('', default=cls.music.music_enabled, k='-CHECK-', enable_events=True), 
            sg.Combo(cls.music.musics, size=(10,1), font=platform.get_font('setting_text'), enable_events=True, k='-MUSIC_SELECT-'), 
            cls.generate_play_button('HINT'), sg.Button(tr('打开文件夹'), font=platform.get_font('button'), k='-OPEN-', enable_events=True)],
            [sg.T(tr('语言: '), font=platform.get_font('setting_text')), sg.Combo(configure['lang'].get_lang_list(), default_value=configure['lang'].get_local_name(), size=(6, 1), font=platform.get_font('setting_text'), enable_events=True, k='LANG')],
            [sg.T(' ')], 
            [sg.B(tr('保存'), font=platform.get_font('setting_button'), disabled=True, k='-SAVE-', enable_events=True, disabled_button_color='#cccccc'), sg.B(tr('退出'), font=platform.get_font('setting_button'), k='-QUIT-', enable_events=True)]
        ]

        about_tab = [
            [sg.T('PasTk', font=platform.get_font('big'), text_color='white')],
            [sg.T('Written in python using PySimpleGUI')]
        ]

        cls.layout = [
            [sg.TabGroup([[sg.Tab(tr('设置'), settings_tab), sg.Tab(tr('关于'), about_tab)]], font=platform.get_font('hint'))]
        ]
        return cls.layout

    @staticmethod
    def generate_simple_setting(hint, name: str):
        return [sg.T(hint, font=platform.get_font('setting_text')), sg.Checkbox(on_off_state[configure[name].active_value], default=configure[name].active_value, font=platform.get_font('hint'), k=name.upper(), enable_events=True)]

    @staticmethod
    def generate_play_button(type_):
        return sg.B(tr('播放'), font=platform.get_font('setting_button'), k=f'-PLAY_{type_}_MUSIC-', enable_events=True)

    @classmethod
    def update_music_state(cls, state):
        cls.window['-SAVE-'].update(disabled=not cls.music.is_modified())
        cls.window['-MUSIC_SELECT-'].update(disabled=not state, value=cls.music.music_selected)

    @classmethod
    def set_default_music(cls):
        cls.music.set_default_music()
        cls.window['-MUSIC_SELECT-'].update(values=cls.music.musics)

    @classmethod
    def ask_for_relaunch(cls, parent: sg.Window):
        res = sg.popup_yes_no(tr('语言已修改，是否立即重启'), title=tr('连续复制-设置'), keep_on_top=True)
        if res == 'Yes':
            configure.save()
            parent.write_event_value('*RELAUNCH*', configure['lang'].active_lang)
            return True
        else:
            return False

    @classmethod
    def ask_for_save(cls):
        res = sg.popup_yes_no(tr('是否保存修改'), title=tr('连续复制-设置'), keep_on_top=True)
        if res is None:
            return False
        elif res == 'Yes':
            configure.save()
            return 'save'
        else:
            return 'rollback'

    @classmethod
    def save(cls, parent):
        ret = -1
        if configure.is_modified('lang'):
            ret = 2 if cls.ask_for_relaunch(parent) else 1   # 2 is relaunch, lang updated; 1 means normal save

        if ret == 1 or configure.any_modified():
            status_str = cls.ask_for_save()
            if not status_str:
                ret = 1
            elif status_str == 'save':
                ret = 0
            else:
                ret = -2    # rollback

        if ret >= 0 and ret != 1:
            configure.save()
            cls.window['-SAVE-'].update(disabled=True)
        return ret

    @classmethod
    def rollback(cls):
        window = cls.window
        modified = configure.any_modified()
        configure.rollback()
        for i in modified:
            if i == 'music':
                cls.init_music()
            elif i == 'lang':
                window['LANG'].update(value=modified[i].get_local_name())
            else:
                window[i.upper()].update(modified[i].active_value)
        window['-SAVE-'].update(disabled=True)

    @classmethod
    def loop(cls, parent=None):
        cls.modified = False
        window = cls.window

        while True:
            e, v = window.read()

            if e in (sg.WINDOW_CLOSE_ATTEMPTED_EVENT, '-QUIT-'):
                status_code = cls.save(parent)
                if status_code == 1:
                    continue
                elif status_code == -2:
                    cls.rollback()
                window.hide()
                break

            if e == '-MUSIC_SELECT-':
                if v[e] != cls.music.music_selected:
                    cls.music.music_selected = v[e]
                    cls.window['-SAVE-'].update(disabled=not cls.music.is_modified())

            elif e == '-SAVE-':
                if cls.save(parent) == 2:
                    break

            elif e in ('ONE_PIECE', 'LAUNCH_MUSIC', 'OVER_MUSIC'):
                configure[e.lower()].active_value = v[e]
                window['-SAVE-'].update(disabled=not configure.is_modified(e.lower()))
                window[e].update(text=on_off_state[v[e]])

            elif e == 'LANG':
                lang = e.lower()
                configure[lang].active_lang = configure[lang].get_lang_name_in_en(v[e])
                window['-SAVE-'].update(disabled=not configure.is_modified(lang))

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
                        sg.popup_ok(tr('没有在音乐文件夹下找到合适的音乐文件，请放入音乐后再尝试开启此选项'), title=tr('连续复制-设置'))
                        window['-CHECK-'].update(False)
                        cls.music.music_enabled = False
                        continue
                cls.update_music_state(v[e])

            elif e == '-OPEN-':
                try:
                    from os import startfile
                    startfile(music_dir)
                except ImportError:
                    from subprocess import call
                    call(['open', music_dir])
