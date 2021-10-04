import sys
import PySimpleGUI as sg

from typing import Dict
from pathlib import Path
from json import dump, load
from collections import UserDict
from json.decoder import JSONDecodeError
from .helper import root
from .settings import template
from .music_manager import Music


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
        self['one_piece'] = self.raw_data['one_piece']

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

    def save(self):
        self.raw_data.update({
            'one_piece': self['one_piece'],
            'music': self['music'].save(),
        })
        Configure._save(self.path, self.raw_data)

    def rollback(self):
        self['music'].rollback()

# Outer class can use the instance directly rather than initializing one themselves
configure = Configure()
