import PySimpleGUI as sg

from pathlib import Path
from functools import wraps
from threading import Thread
from playsound import playsound
from ..abstract_window import Window
from ..config.system_manager import platform

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


def playsound_thread(filepath):
    Thread(target=playsound, args=(filepath,), name='PlayMusic').start()


def play_launch_music(flag):
    def inner_deco(f):
        @wraps(f)
        def wrapper():
            if flag:
                playsound_thread(music_dir / 'launch' / 'launch_music.mp3')
            f()
        return wrapper
    return inner_deco
