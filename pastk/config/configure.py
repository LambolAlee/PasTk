import sys
import PySimpleGUI as sg

from typing import Dict
from pathlib import Path
from json import dump, load
from collections import UserDict
from json.decoder import JSONDecodeError

from ..helpers.helper import root
from ..helpers.settings import template
from .music_manager import Music
from .simple_setting_manager import SimpleSet


class Configure(UserDict):
    """
    Configure manager

    Each key in the settings.json is written in the `data` attribute, so can call
    each part by using dict syntex

    And the real data is stored in the `raw_data` attribute
    """
    def __init__(self):
        super().__init__(None)
        self.path = root / 'settings.json'
        self.raw_data = Configure._try_load(self.path)

        self['music'] = Music(self.raw_data['music'])
        self['one_piece'] = SimpleSet(self.raw_data['one_piece'])
        self['launch_music'] = SimpleSet(self.raw_data['launch_music'])
        self['over_music'] = SimpleSet(self.raw_data['over_music'])

    @staticmethod
    def _save(path, data: Dict):
        with open(path, 'w', encoding='utf-8') as f:
            dump(data, f, indent=4)

    @staticmethod
    def _try_load(path: Path):
        data = template
        if path.exists():
            with open(path, 'r', encoding='utf-8') as f:
                try:
                    data = load(f)
                except JSONDecodeError:
                    sg.popup_error('配置文件损坏，请删除配置文件并重新启动程序', f'配置文件地址：{path}', title='连续复制-错误', font=('', 14))
                    sys.exit(1)
        else:
            Configure._save(path, template)
        return data

    def is_modified(self, key: str):
        return self[key].is_modified()

    def save(self):
        self.raw_data.update({
            k: self[k].save() for k in self
        })
        Configure._save(self.path, self.raw_data)

    def rollback(self):
        for v in self.values(): v.rollback()

# Outer class can use the instance directly rather than initializing one themselves
configure = Configure()
