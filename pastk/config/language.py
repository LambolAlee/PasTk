from json import load
from ..helpers.helper import lang_dir


class Language:
    lang_list = [
        'zh_cn',
        'en'
    ]

    def __init__(self, value='zh_cn'):
        if value not in self.lang_list:
            value = 'zh_cn'
        self.lang = self.active_lang = value
        self.load()

    def load(self):
        with open(lang_dir / f"{self.lang}.json", 'r', encoding='utf-8') as f:
            self.data = load(f)

    def tr(self, string):
        if self.lang == 'zh_cn':
            return string
        else:
            return self.data[string]

    def get_lang_name_in_en(self, name):
        return self.data[name]

    def get_local_name(self):
        return self.data[self.lang]

    def get_lang_list(self):
        return self.data["语言列表"]

    def is_modified(self):
        return self.lang != self.active_lang

    def save(self):
        self.lang = self.active_lang
        return self.lang

    def rollback(self):
        self.active_lang = self.lang
