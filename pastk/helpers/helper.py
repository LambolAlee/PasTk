import pyautogui as auto
import PySimpleGUI as sg
from pathlib import Path
from time import sleep
from queue import Queue
from base64 import encodebytes
from threading import Thread
from ..abstract_window import Window

# copier is the public list used to store the copied contents temporarily,
# all the members in the package can read and write the list
copier = []

FONT = ('', 14)

# basic path root: path of the outer directory where main.py lives
root = Path(__file__).parent.parent.parent
resources = root / 'resources'
music_dir = resources / 'musics'

supported_musics = ['.mp3', '.wav']


def set_input_pos():
    """
    activate the target input place in advance, so I can tap command+tab and command+v keystroke using pyautogui
    for the purpose of automaticly paste
    """
    sg.Window("连续复制", [[sg.T('请点击需要粘贴的地方', font=FONT)], [sg.B('选好了', font=('', 12)), sg.T('自动粘贴失败仍可手动粘贴', text_color='#E6E6FA')]], keep_on_top=True).read(close=True)


def notify(title: str, cont='若自动粘贴失败，仍可手动粘贴'):
    sg.popup_notify(cont, title=title, display_duration_in_ms=1500, fade_in_duration=500, location=(sg.Window.get_screen_size()[0]-364, 0))

######################################
#           path getter              #
######################################
def get_resource(name: str):
    resource: Path = resources / name
    return str(resource.resolve())


def get_icon():
    icon = get_resource('paste-128.png')
    with open(icon, 'rb') as f:
        res = encodebytes(f.read())
    return res


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
    auto.hotkey('command', 'tab')
    auto.hotkey('command', 'v')


def auto_paste_servive(window: sg.Window, queue: Queue):
    def service():
        print('[auto paste] start listening...')
        while True:
            sig = queue.get()
            if sig == 'q':
                print('[auto paste] quitting...')
                return
            else:
                print('[auto paste] pasting...')
                auto_paste()
                sleep(.5)
                window.write_event_value('*EXECUTED*', True)
    return Thread(target=service, name='AutoPaste_Service')
