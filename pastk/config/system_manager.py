from platform import system


class Platform:
    app = None
    size_darwin = {
        "text": 14,
        "button": 12,
        "home_hint": 12,
        "setting_text": 16,
        "setting_button": 12,
        "hint": 12,
        "big": 32
    }

    size_windows = {
        "text": 10,
        "button": 10,
        "home_hint": 8,
        "setting_text": 9,
        "setting_button": 8,
        "hint": 7,
        "big": 22
    }

    def __init__(self):
        self.sys_name = system()
        self.init_by_sys()

    def init_by_sys(self):
        self.icon_suffix = '.png'
        # self.switch_app_keys = ('command', 'tab')
        self.paste_keys = ('ctrl', 'v')

        if self.sys_name == 'Darwin':
            self.paste_keys = ('command', 'v')
        elif self.sys_name == 'Windows':
            self.icon_suffix = '_128.png'

    def get_font(self, key):
        if self.sys_name == 'Windows':
            return ('Microsoft YaHei', self.size_windows[key])
        else:
            return ('default', self.size_darwin[key])

platform = Platform()
