import PySimpleGUI as sg

from time import sleep
from queue import Queue
from pathlib import Path
from pyperclip import paste
from threading import Thread
from playsound import playsound

from .abstract_window import Window
from .details_view import DetailWindow
from .helper import copier, FONT, get_resource

background_color = sg.theme_background_color()

B_mode = lambda title, key: sg.Button(title, k=key, font=FONT, enable_events=True, size=(18, 1))
Image_B = lambda key, filename, **kwargs: sg.Button('', pad=(0,0), mouseover_colors='#a6a6b9', k=key, image_filename=get_resource(filename), button_color='#a6a6b9', enable_events=True, **kwargs)


class HomeWindow(Window):
    count = 0
    listening = False
    listener_thread = None
    music_thread = None
    music_queue = Queue()
    music = Path(__file__).parent.parent / 'resources' / 'musics' / 'ding2.mp3'

    layout_home = [
        [sg.T('0 0', font=('', 32), pad=(0,5), justification='right', k='-COUNTER-'), sg.Column([[sg.T(' ')], [sg.T('条已复制', font=('', 12), text_color='#d1cfa3')]], pad=(0,5)), sg.T(' ', size=(9,1)), sg.Column([[sg.B('', k='-DETAIL-', enable_events=True, image_filename=get_resource('detail.png'), button_color=background_color, image_subsample=2, mouseover_colors=background_color)], [sg.T(' ')]])],
        [sg.Frame('', [[Image_B('-SET-', 'settings.png'), sg.T(' ', background_color='#a6a6b9'), sg.B('Start', k='-START-', size=(10, 1), font=('', 14), button_color=('white', '#464d64'), mouseover_colors=('white', '#575d70'), focus=True), sg.T(' ', background_color='#a6a6b9'), Image_B('-RESET-', 'reset.png', disabled=True)]], background_color='#a6a6b9')]
    ]

    layout_mode = [
        [B_mode('合并粘贴', '-HE_BING-')],
        [B_mode('分段粘贴', '-FEN_DUAN-')],
        [B_mode('连续粘贴', '-LIAN_XU-')],
        [B_mode('选择粘贴', '-XUAN_ZE-')]
    ]

    layout = [
        [sg.pin(sg.Frame('', layout_home, k='-HOME-', border_width=0))],
        [sg.pin(sg.Frame('', layout_mode, k='-MODE-', visible=False))]
    ]

    @classmethod
    def init(cls):
        cls.report('Initializing home window')
        x = (sg.Window.get_screen_size()[0] - 264) // 2
        cls.window = sg.Window('连续复制', layout=cls.layout, location=(x, 0), keep_on_top=True, finalize=True)
        cls.window['-SET-'].Widget.config(takefocus=0)
        cls.window['-RESET-'].Widget.config(takefocus=0)
        cls.window['-DETAIL-'].Widget.config(takefocus=0)

    @classmethod
    def start_listener(cls):
        cls.listening = True

        def wrapper_listener():
            cls.report('Start listening...')
            original_text = paste()
            while cls.listening:
                current_text = paste()
                if original_text != current_text and current_text is not None:
                    cls.window.write_event_value('*NEW_CONTENT*', current_text)
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
                    playsound(cls.music)
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
    def run_loop(cls):
        super().run_loop()

        cls.count = 0
        window: sg.Window = cls.window
        started = False

        while True:
            e, v = window.read()

            if e in (sg.WINDOW_CLOSED, '-QUIT-'):
                if started:
                    cls.quit_listener()
                break

            if e == '*NEW_CONTENT*':
                cls.report(v[e])
                copier.append(v['*NEW_CONTENT*'])
                cls.count += 1
                if cls.count > 99:
                    cls.count = 99
                    window.ding()
                    sg.popup_ok('亲，已经到达数量上限了哦！', title='连续复制', font=FONT)
                    continue
                cls.update_digital()

            elif e == '-START-' or e == '-RESET-':
                if started:
                    cls.count = 0
                    started = False
                    window['-START-'].update('Start')
                    window['-RESET-'].update(disabled=True)
                    window['-COUNTER-'].update('0 0')
                    cls.quit_listener()

                    if e == '-START-':
                        if copier == []:
                            sg.popup_notify('没有复制任何文字，请重新开始！', title='连续复制', location=(window.get_screen_size()[0]-364, 0))
                            continue
                        window['-HOME-'].update(visible=False)
                        window['-MODE-'].update(visible=True)
                        cls.report(copier)
                    else:
                        copier.clear()
                else:
                    started = True
                    window['-START-'].update('Over')
                    window['-RESET-'].update(disabled=False)
                    cls.start_listener()

            elif e == '-DETAIL-':
                window.hide()
                DetailWindow.run_loop()
                DetailWindow.close()
                cls.count = len(copier)
                cls.update_digital()
                window.un_hide()

            if e in ('-HE_BING-', '-FEN_DUAN-', '-LIAN_XU-', '-XUAN_ZE-'):
                return e

    @classmethod
    def close(cls):
        cls.layout_home = cls.layout_mode = cls.listener_thread = None
        super().close()
        cls.report('home quit')
