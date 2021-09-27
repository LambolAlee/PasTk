from .home_view import HomeWindow
from .details_view import DetailWindow
from .helper import copier, get_callable, FONT, set_input_pos, get_icon
from .continuous_paste_view import ContinueWindow
from .selection_paste_view import SelectionWindow
from .junction_view import merge, subsection

run_HomeWindow = get_callable(HomeWindow)
run_DetailWindow = get_callable(DetailWindow)
run_ContinueWindow = get_callable(ContinueWindow)
run_SelectionWindow = get_callable(SelectionWindow)
run_Merge = merge
run_Subsection = subsection

handlers = {
    '-HE_BING-': run_Merge,
    '-FEN_DUAN-': run_Subsection,
    '-LIAN_XU-': run_ContinueWindow,
    '-XUAN_ZE-': run_SelectionWindow
}

__all__ = ("handlers", "run_HomeWindow", "copier", "FONT", "set_input_pos", "get_icon")
