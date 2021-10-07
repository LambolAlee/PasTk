import PySimpleGUI as sg

from pastk import run_HomeWindow
from pastk.helpers.helper import set_input_pos
from pastk import configure, auto_paste_service
from pastk import get_icon, handlers, set_input_pos
from pastk import play_launch_music


@auto_paste_service
@play_launch_music(configure['launch_music'])
def main():
    sg.set_options(icon=get_icon(), font=('PingFang', 14), use_ttk_buttons=True)
    while True:
        handle_type = run_HomeWindow()
        if handle_type in handlers:
            set_input_pos()
            handlers[handle_type]()
        if configure['one_piece'] or handle_type == 1:
            break


if __name__ == '__main__':
    main()
