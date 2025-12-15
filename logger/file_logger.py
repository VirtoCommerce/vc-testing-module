import logging
from pathlib import Path
from typing import Any


class FileLogger:
    def __init__(self, name: str, file_path: Path):
        self._logger = logging.getLogger(f"{name}.file")
        if not self._logger.handlers:
            handler = logging.FileHandler(file_path, mode="w", encoding="utf-8")
            formatter = logging.Formatter("%(asctime)s [%(levelname)s]: %(message)s")
            handler.setFormatter(formatter)
            self._logger.addHandler(handler)
        self._logger.setLevel(logging.DEBUG)
        self._logger.propagate = False

    def info(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._logger.info(message, *args, **kwargs)

    def error(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._logger.error(message, *args, **kwargs)

    def warning(self, message: str, *args: Any, **kwargs: Any) -> None:
        self._logger.warning(message, *args, **kwargs)
