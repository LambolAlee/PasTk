import PySimpleGUI as sg

from pastk import run_HomeWindow
from pastk import configure, auto_paste_service
from pastk import get_icon, handlers, set_input_pos
from pastk import play_launch_music, platform


@auto_paste_service
@play_launch_music(configure['launch_music'])
def main():
    sg.set_options(icon=get_icon(), font=platform.get_font('text'), use_ttk_buttons=True)
    while True:
        handle_type = run_HomeWindow()
        if handle_type in handlers:
            set_input_pos()
            handlers[handle_type]()
        if handle_type == 3:
            continue
        if configure['one_piece'].active_value or handle_type == 1:
            break


if __name__ == '__main__':
    main()
