import json
import os
from pathlib import Path
from traceback import print_exc


class Config:
    def __init__(self, file_path: str, **defaults):
        self.file_path = file_path.replace('\\', '/')
        self.defaults = defaults
        self.data = defaults

        if not self.exists:
            self.save()

        self.load()

        self.ensure_defaults()

    def ensure_defaults(self):
        if not any(k not in self.data for k in self.defaults):
            return

        for k, v in self.defaults.items():
            if k not in self.data:
                self.data[k] = v

        self.save()

    def save(self):
        path = Path()

        for p in self.file_path.split('/')[:-1]:
            path /= p

            if not path.exists():
                os.mkdir(path)

        with open(self.file_path, 'w') as f:
            json.dump(self.data, f, indent=2)

    def load(self):
        with open(self.file_path) as f:
            self.data = json.load(f)

    @property
    def exists(self):
        return os.path.exists(self.file_path)

    def reset(self):
        self.data = self.defaults
        self.save()

    def get(self, *path: str):
        """
        :param path: the path to the config value
        :return: the config value asked for
        """
        if not path or not path[0]:
            raise ValueError('path to config value cannot be empty')

        if len(path) == 1:
            path = path[0].split('/')

        try:
            value = self.data[path[0]]
            for v in path[1:]:
                value = value[v]

        except (IndexError, KeyError):
            print_exc()
            return None

        return value

    def __getattr__(self, item):
        return self.__dict__[item] if item in self.__dict__ else self.data[item]


cfg = Config('config/config.json', oauth='BOT_OAUTH', command_prefix='!')
