import os

import pytest
from dotenv import dotenv_values

DEFAULTS = {
    "CHECKOUT_MODE": "single-page",
    "PRODUCT_QUANTITY_CONTROL": "stepper",
    "RANGE_FILTER_TYPE": "slider",
    "SEARCH_QUERIES_KEY": "search-queries",
}


class Config:
    def __init__(self):
        env_file_values = dotenv_values(encoding="utf-8")
        env_os_values = dict[str, str](os.environ)
        self._config = {**DEFAULTS, **env_file_values, **env_os_values}

    def __getitem__(self, key: str):
        return self._config[key]

    def to_dict(self) -> dict:
        return dict[str, str](self._config)


@pytest.fixture(scope="session")
def config() -> Config:
    return Config()
