from .home_view import HomeWindow
from .selection_paste_view import SelectionWindow
from .continuous_paste_view import ContinueWindow
from .junction_view import subsection, merge
from .helpers.configure import configure
from .helpers.helper import get_callable, get_icon, set_input_pos

run_HomeWindow = get_callable(HomeWindow)

handlers = {
    '-HE_BING-': merge,
    '-FEN_DUAN-': subsection,
    '-LIAN_XU-': get_callable(ContinueWindow),
    '-XUAN_ZE-': get_callable(SelectionWindow)
}

__all__ = ("run_HomeWindow", "get_icon", "handlers", "configure", "set_input_pos")
