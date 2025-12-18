import os

import pytest
from dotenv import dotenv_values


class Config:
    def __init__(self):
        file_values = dotenv_values(encoding="utf-8")
        env_vaues = dict(os.environ)
        self._config = {**file_values, **env_vaues}

    def __getitem__(self, key: str):
        return self._config[key]

    def to_dict(self) -> dict:
        return dict(self._config)


@pytest.fixture(scope="session")
def config() -> Config:
    return Config()
