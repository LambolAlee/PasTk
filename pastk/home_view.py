"""
home_view.py

this file is the main page of the whole app
"""

import PySimpleGUI as sg

from time import sleep
from queue import Queue
from pyperclip import paste
from threading import Thread
from playsound import playsound

from .config.configure import tr
from .config_view import configure
from .abstract_window import Window
from .config_view import ConfigWindow
from .details_view import DetailWindow
from .config.system_manager import platform
from .helpers.helper import copier, get_resource, music_dir, playsound_thread

try:
    from AppKit import NSWorkspace
except ImportError:
    if platform.sys_name == 'Darwin':
        import sys
        sg.popup_error("Detect that you are on MacOS, need to install PyObjC", "run `pip install pyobjc` to fix", title='连续复制')
        sys.exit(1)

background_color = sg.theme_background_color()

B_mode = lambda title, key: sg.Button(title, k=key, enable_events=True, size=(18, 1))
Image_B = lambda key, filename, **kwargs: sg.Button('', pad=(0,0), mouseover_colors='#a6a6b9', k=key, image_filename=get_resource(filename), button_color='#a6a6b9', enable_events=True, border_width=0, **kwargs)


class HomeWindow(Window):
    count = 0
    listening = False
    listener_thread = None
    music_thread = None
    music_queue = Queue()
    home_frame_visible = True

    @classmethod
    def init(cls):
        cls.report('Initializing home window')
        x = (sg.Window.get_screen_size()[0] - 264) // 2
        cls.window = sg.Window(tr('连续复制'), layout=cls.build(), location=(x, 0), keep_on_top=True, enable_close_attempted_event=True, finalize=True)
        cls.window['-SET-'].Widget.config(takefocus=0)
        cls.window['-RESET-'].Widget.config(takefocus=0)
        cls.window['-DETAIL-'].Widget.config(takefocus=0)
        # Use apple built in class to switch between python and the place waiting to paste
        if platform.sys_name == 'Darwin' and platform.app is None:
            platform.app = NSWorkspace.sharedWorkspace().frontmostApplication()     # NSRunningApplication

    @classmethod
    def build(cls):
        layout_home = [
            [sg.T('0 0', font=platform.get_font('big'), pad=(0,5), justification='right', k='-COUNTER-'), sg.Column([[sg.T(' ')], [sg.T(tr('条已复制'), font=platform.get_font('home_hint'), text_color='#d1cfa3')]], pad=(0,5)), sg.T(' ', size=(7,1)), sg.Column([[sg.B('', k='-DETAIL-', enable_events=True, image_filename=get_resource('detail.png'), button_color=background_color, image_subsample=2, mouseover_colors=background_color)], [sg.T(' ')]])],
            [sg.Frame('', [[Image_B('-SET-', 'settings.png'), sg.T(' ', background_color='#a6a6b9'), sg.B(tr('开始'), k='-START-', size=(10, 1), button_color=('white', '#464d64'), mouseover_colors=('white', '#575d70'), focus=True), sg.T(' ', background_color='#a6a6b9'), Image_B('-RESET-', 'reset.png', disabled=True)]], background_color='#a6a6b9')]
        ]

        layout_mode = [
            [B_mode(tr('合并粘贴'), '-HE_BING-')],
            [B_mode(tr('分段粘贴'), '-FEN_DUAN-')],
            [B_mode(tr('连续粘贴'), '-LIAN_XU-')],
            [B_mode(tr('选择粘贴'), '-XUAN_ZE-')]
        ]

        cls.layout = [
            [sg.pin(sg.Frame('', layout_home, k='-HOME-', border_width=0))],
            [sg.pin(sg.Frame('', layout_mode, k='-MODE-', visible=False))]
        ]
        return cls.layout

    @classmethod
    def start_listener(cls):
        music = configure['music']
        cls.listening = True
        playable = music.is_playable()

        def is_current_text_ok(current_text, original_text):
            if current_text is not None and current_text.strip():
                if original_text != current_text:
                    return True
            return False

        def wrapper_listener():
            cls.report('Start listening...')
            original_text = paste()
            while cls.listening:
                current_text = paste()
                if is_current_text_ok(current_text, original_text):
                    cls.window.write_event_value('*NEW_CONTENT*', current_text)
                    if playable:
                        cls.music_queue.put('play')
                    original_text = current_text
                sleep(0.01)
            cls.report('Quitting...')

        def wrapper_music():
            cls.report('Start music...')
            while True:
                sig = cls.music_queue.get()
                if sig == 'quit':
                    break
                elif sig == 'play':
                    cls.report('playing')
                    playsound(music.music_path)
            cls.report('Quit music...')

        cls.listener_thread = Thread(target=wrapper_listener, name='Copy_Listener')
        cls.music_thread = Thread(target=wrapper_music, name='Music_Player')
        cls.listener_thread.start()
        cls.music_thread.start()
# 《赵进喜三阴三阳〈伤寒论〉讲稿》墙裂推荐
    @classmethod
    def quit_listener(cls):
        if cls.listening:
            cls.listening = False
            cls.music_queue.put('quit')
            cls.music_thread.join()         # 若界面无响应，则问题在此
            cls.listener_thread.join()      # 若界面无响应，则问题在此

    @classmethod
    def update_digital(cls):
        tens = cls.count // 10
        basics = cls.count - tens * 10
        cls.window['-COUNTER-'].update(f'{tens} {basics}')

    @classmethod
    def check_if_quit(cls, e):
        if e == sg.WINDOW_CLOSE_ATTEMPTED_EVENT:
            if cls.home_frame_visible:
                return 1
            else:
                return 2    # return to the home view
        elif e == '-QUIT-':
            return 1    # quit the app
        elif e == '*RELAUNCH*':
            return 3    # relaunch the app
        else:
            return 0    # other events

    @classmethod
    def toggle_frame(cls):
        cls.home_frame_visible = not cls.home_frame_visible
        cls.window['-HOME-'].update(visible=cls.home_frame_visible)
        cls.window['-MODE-'].update(visible=not cls.home_frame_visible)

    @classmethod
    def loop(cls, parent=None):
        cls.count = 0
        copier.clear()
        window: sg.Window = cls.window
        started = False
        title = tr('连续复制')

        while True:
            e, v = window.read()

            status_code = cls.check_if_quit(e)
            if status_code == 1:
                if started:
                    cls.quit_listener()
                return status_code
            elif status_code == 2:
                cls.toggle_frame()
                continue
            elif status_code == 3:
                configure['lang'].load()
                return status_code

            if e == '*NEW_CONTENT*':
                cls.report(v[e])
                copier.append(v['*NEW_CONTENT*'])
                cls.count += 1
                if cls.count > 99:
                    cls.count = 99
                    window.ding()
                    sg.popup_ok(tr('亲，已经到达数量上限了哦！'), title=title)
                    continue
                cls.update_digital()

            elif e in ('-START-', '-RESET-'):
                if started:
                    started = False
                    window['-START-'].update(tr('开始'))
                    window['-RESET-'].update(disabled=True)
                    cls.quit_listener()

                    if e == '-START-':
                        if copier == []:
                            sg.popup_notify(tr('没有复制任何文字，请重新开始！'), title=title, location=(window.get_screen_size()[0]-364, 0))
                            continue
                        if configure['over_music'].active_value:
                            playsound_thread(music_dir / 'launch' / 'over_music.wav')
                        cls.toggle_frame()
                        cls.report(copier)
                    else:
                        cls.count = 0
                        copier.clear()
                        window['-COUNTER-'].update('0 0')
                else:
                    started = True
                    window['-START-'].update(tr('结束'))
                    window['-RESET-'].update(disabled=False)
                    cls.start_listener()

            elif e == '-DETAIL-':
                DetailWindow.run_loop(window)
                cls.count = len(copier)
                cls.update_digital()

            elif e == '-SET-':
                if started:
                    sg.popup_auto_close(tr('请先结束复制再修改配置！'), title=title, auto_close_duration=1)
                    continue
                ConfigWindow.run_loop(window)

            if e in ('-HE_BING-', '-FEN_DUAN-', '-LIAN_XU-', '-XUAN_ZE-'):
                cls.home_frame_visible = True
                return e

    @classmethod
    def close(cls):
        ConfigWindow.close()
        DetailWindow.close()
        cls.layout_home = cls.layout_mode = cls.listener_thread = cls.paste_server = None
        super().close()
