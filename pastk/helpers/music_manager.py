from typing import Dict
from .helper import get_musics, music_dir, check_music_dir


class Music:
    """Stands for the music part in the settings.json"""
    _music_path = None
    _music_selected = ""

    def __init__(self, data: Dict):
        self.data = data
        self.musics = get_musics()
        self.init()

    def init(self):
        check_music_dir()
        self.music_selected = self.data['music_selected']
        self.music_enabled = self.data['enabled']

    @property
    def music_path(self):
        return self._music_path

    @property
    def music_selected(self):
        return self._music_selected

    @music_selected.setter
    def music_selected(self, value: str):
        self._music_selected = value
        self._music_path = music_dir / value

    def check_has_musics_with_refresh(self):
        self.refresh_musics()
        return bool(self.musics)

    def check_music_selected(self):
        return self.music_path.exists()

    def check_availability(self):
        return self.check_has_musics_with_refresh() and self.check_music_selected()

    def set_default_music(self):
        self.music_selected = self.musics[0]
        self.music_enabled = True

    def refresh_musics(self):
        self.musics = get_musics()
        return self.musics

    def is_modified(self):
        return self.music_enabled != self.data['enabled'] \
                or self.music_selected != self.data['music_selected']

    def is_playable(self):
        return self.check_music_selected() and self.music_enabled

    def rollback(self):
        self.init()

    def save(self):
        self.data.update({
            'enabled': self.music_enabled,
            'music_selected': self.music_selected
        })
        return self.data
