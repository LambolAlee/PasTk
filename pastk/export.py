from .home_view import HomeWindow
from .continuous_paste_view import ContinueWindow
from .selection_paste_view import SelectionWindow
from .junction_view import merge, subsection
from .helpers.helper import get_callable, FONT, set_input_pos, get_icon

run_HomeWindow = get_callable(HomeWindow)

handlers = {
    '-HE_BING-': merge,
    '-FEN_DUAN-': subsection,
    '-LIAN_XU-': get_callable(ContinueWindow),
    '-XUAN_ZE-': get_callable(SelectionWindow)
}

__all__ = ("handlers", "run_HomeWindow", "FONT", "set_input_pos", "get_icon")
