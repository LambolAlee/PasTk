from platform import system


class Platform:
    def __init__(self):
        self.sys_name = system()
        self.init_by_sys()

    def init_by_sys(self):
        self.icon_suffix = '.png'
        self.switch_app_keys = ('alt', 'tab')
        self.paste_keys = ('ctrl', 'v')

        if self.sys_name == 'Darwin':
            self.switch_app_keys = ('command', 'tab')
            self.paste_keys = ('command', 'v')
        elif self.sys_name == 'Windows':
            self.icon_suffix = '.ico'


platform = Platform()
