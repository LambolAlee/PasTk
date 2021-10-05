from .home_view import HomeWindow
from .selection_paste_view import SelectionWindow
from .continuous_paste_view import ContinueWindow
from .popup_view import subsection, PopupMergeWindow, SetInputPos
from .helpers.configure import configure
from .helpers.helper import get_callable, get_icon
from .helpers.auto_paste_service import auto_paste_service

run_HomeWindow = get_callable(HomeWindow)
set_input_pos = get_callable(SetInputPos)

handlers = {
    '-FEN_DUAN-': subsection,
    '-HE_BING-': get_callable(PopupMergeWindow),
    '-LIAN_XU-': get_callable(ContinueWindow),
    '-XUAN_ZE-': get_callable(SelectionWindow)
}

__all__ = (
    "run_HomeWindow", "get_icon", "handlers", 
    "configure", "auto_paste_service", "set_input_pos"
)
