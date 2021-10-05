import PySimpleGUI as sg

from pastk import run_HomeWindow
from pastk import get_icon, handlers, set_input_pos
from pastk import configure, auto_paste_service
from pastk.helpers.helper import set_input_pos


@auto_paste_service
def main():
    sg.set_options(icon=get_icon(), font=('', 14))
    while True:
        handle_type = run_HomeWindow()
        if configure['one_piece'] or handle_type == 1:
            break
        if not handle_type is None:
            set_input_pos()
            handlers[handle_type]()


if __name__ == '__main__':
    main()
