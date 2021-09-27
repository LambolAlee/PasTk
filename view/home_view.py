import PySimpleGUI as sg
from time import sleep
from queue import Queue
from pathlib import Path
from pyperclip import paste
from threading import Thread
from playsound import playsound
from .abstract_window import Window
from .helper import copier, FONT
from .details_view import DetailWindow

B = lambda title, key, **kwargs: sg.Button(title, font=FONT, k=key, size=(5, 1), enable_events=True, **kwargs)
B_mode = lambda title, key: sg.Button(title, k=key, font=FONT, enable_events=True, size=(18, 1))
B_digi = lambda title, key: sg.Button(title, k=key, font=('IBM 3270', 20), enable_events=True, button_color=('white', sg.theme_background_color()), border_width=0, disabled_button_color='#b2b4b6')


class HomeWindow(Window):
    count = 0
    listening = False
    listener_thread = None
    music_thread = None
    music_queue = Queue()
    music = Path(__file__).parent.parent / 'resources' / 'musics' / 'ding2.mp3'

    layout_home = [
        [B('Start', '-START-'), B('Reset', '-RESET-', disabled=True, disabled_button_color='#b2b4b6'), B('Quit', '-QUIT-')],
        [sg.HorizontalSeparator(),
        sg.Frame('', [[B_digi('0', '-TENS-'), B_digi('0', '-BASICS-')]], border_width=0),
        sg.HorizontalSeparator()]
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
        x = (sg.Window.get_screen_size()[0] - 229) // 2
        cls.window = sg.Window('连续复制', layout=cls.layout, location=(x, 0), keep_on_top=True, finalize=True)
        cls.window['-TENS-'].Widget.config(takefocus=0)
        cls.window['-BASICS-'].Widget.config(takefocus=0)

    @classmethod
    def start_listener(cls):
        cls.listening = True

        def wrapper_listener():
            print('Start listening...')
            original_text = paste()
            while cls.listening:
                current_text = paste()
                if original_text != current_text and current_text is not None:
                    cls.window.write_event_value('*NEW_CONTENT*', current_text)
                    cls.music_queue.put('play')
                    original_text = current_text
                sleep(0.01)
            print('Quitting...')

        def wrapper_music():
            print('Start music...')
            while True:
                sig = cls.music_queue.get()
                if sig == 'quit':
                    break
                elif sig == 'play':
                    print('playing')
                    playsound(cls.music)
            print('Quit music...')

        cls.listener_thread = Thread(target=wrapper_listener, name='Copy_Listener')
        cls.music_thread = Thread(target=wrapper_music, name='Music_Player')
        cls.listener_thread.start()
        cls.music_thread.start()
# 《赵进喜三阴三阳〈伤寒论〉讲稿》
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
        cls.window['-TENS-'].update(str(tens))
        cls.window['-BASICS-'].update(str(basics))

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
                print(v[e])
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
                    window['-TENS-'].update('0')
                    window['-BASICS-'].update('0')
                    cls.quit_listener()

                    if e == '-START-':
                        if copier == []:
                            sg.popup_notify('没有复制任何文字，请重新开始！', title='连续复制', location=(window.get_screen_size()[0]-364, 0))
                            continue
                        window['-HOME-'].update(visible=False)
                        window['-MODE-'].update(visible=True)
                        print(copier)
                    else:
                        copier.clear()
                else:
                    started = True
                    window['-START-'].update('Over')
                    window['-RESET-'].update(disabled=False)
                    cls.start_listener()

            elif e in ('-TENS-', '-BASICS-'):
                # print(window.size)
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
        print('home quit')
        DetailWindow.close()
        print('detail quit')
        cls.listener_thread = None
        cls.layout_home = cls.layout_mode = None
        super().close()
