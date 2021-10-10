class SimpleSet:
    """Stands for the simple part in the settings.json"""

    def __init__(self, value):
        self.data = value
        self.active_value = value

    def is_modified(self):
        return self.active_value != self.data

    def rollback(self):
        self.active_value = self.data

    def save(self):
        self.data = self.active_value
        return self.data
