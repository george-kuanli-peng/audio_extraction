import configparser
import os
from typing import Optional


class Config:

    cfg: configparser.ConfigParser

    def __init__(self, config_path: Optional[str] = None):
        if not config_path:
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config.ini')
        self.cfg = configparser.ConfigParser()
        self.cfg.read(config_path)

    def get_value(self, section: str, option: str) -> str:
        try:
            env_key = self._get_env_key(section, option)
            return os.environ[env_key]
        except KeyError:
            return self.cfg[section][option]

    @staticmethod
    def _get_env_key(section: str, option: str):
        return '_'.join([section.upper(), option.upper()])

    def get_bool(self, section: str, option: str) -> bool:
        raw_val = self.get_value(section, option)
        return self._get_bool(raw_val)

    @staticmethod
    def _get_bool(raw_val: str) -> bool:
        return raw_val.lower() in ('1', 'yes', 'true', 'on')


config = Config()
