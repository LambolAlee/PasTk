import sys
import PySimpleGUI as sg

from pastk import run_HomeWindow
from pastk import handlers, set_input_pos, get_icon


def main():
    sg.set_global_icon(get_icon())
    handle_type = run_HomeWindow()
    if handle_type is None:
        sys.exit(1)
    set_input_pos()
    # handlers handle the different type of pasting
    handlers[handle_type]()


if __name__ == '__main__':
    main()
