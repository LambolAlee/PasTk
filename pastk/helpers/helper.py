import pyautogui as auto
import PySimpleGUI as sg
from time import sleep
from queue import Queue
from pathlib import Path
from threading import Thread
from ..abstract_window import Window
from .system_manager import platform

# copier is the public list used to store the copied contents temporarily,
# all the members in the package can read and write the list
copier = []

# basic path root: path of the outer directory where main.py lives
root = Path(__file__).parent.parent.parent
resources = root / 'resources'
music_dir = resources / 'musics'

supported_musics = ['.mp3', '.wav']


def check_music_dir():
    if not music_dir.exists():
        music_dir.mkdir()


def set_input_pos():
    """
    activate the target input place in advance, so I can tap command+tab and command+v keystroke using pyautogui
    for the purpose of automaticly paste
    """
    sg.Window("连续复制", [[sg.T('请点击需要粘贴的地方')], [sg.B('选好了', font=('', 12)), sg.T('自动粘贴失败仍可手动粘贴', text_color='#E6E6FA')]], keep_on_top=True).read(close=True)


def notify(title: str, cont='若自动粘贴失败，仍可手动粘贴'):
    sg.popup_notify(cont, title=title, display_duration_in_ms=1500, fade_in_duration=500, location=(sg.Window.get_screen_size()[0]-364, 0))


######################################
#           path getter              #
######################################
def get_resource(name: str):
    resource: Path = resources / name
    return resource.resolve()


def get_icon():
    icon = get_resource(f'logo/PasTk_logo{platform.icon_suffix}')
    return icon.read_bytes()


def get_musics():
    files = (root / 'resources' / 'musics').glob('*')
    return [f.name for f in files if f.suffix in supported_musics]


# a decorater to wrap the class call
def get_callable(class_: Window):
    def wrapper():
        ret = class_.run_loop()
        class_.close()
        return ret
    return wrapper


def auto_paste():
    auto.hotkey(*platform.switch_app_keys, interval=.02)
    auto.hotkey(*platform.paste_keys, interval=.02)


def auto_paste_servive(window: sg.Window, queue: Queue):
    def service():
        print('*[auto paste]* start listening...')
        while True:
            sig = queue.get()
            if sig == 'quit':
                print('*[auto paste]* quitting...')
                return
            else:
                print('*[auto paste]* pasting...')
                auto_paste()
                sleep(.5)
                window.write_event_value('*EXECUTED*', True)
    return Thread(target=service, name='AutoPaste_Service')
