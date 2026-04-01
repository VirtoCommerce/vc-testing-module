import logging
from pathlib import Path

from rich.console import Console
from rich.logging import RichHandler

from core.logger.base import TRACE, Logger

_default_console = Console(stderr=True)

logging.addLevelName(TRACE, "TRACE")


class RichLogger(Logger):
    def __init__(
        self,
        name: str,
        console_level: int = logging.DEBUG,
        show_path: bool = False,
        log_file: Path | None = None,
        console: Console | None = None,
    ) -> None:
        self._logger = logging.getLogger(name)
        for handler in self._logger.handlers[:]:
            handler.close()
            self._logger.removeHandler(handler)

        console_handler = RichHandler(
            console=console or _default_console,
            rich_tracebacks=True,
            show_path=show_path,
            omit_repeated_times=False,
        )
        console_handler.setLevel(console_level)
        self._logger.addHandler(console_handler)

        if log_file is not None:
            file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
            file_handler.setFormatter(
                logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
            )
            file_handler.setLevel(TRACE)
            self._logger.addHandler(file_handler)

        self._logger.setLevel(TRACE)
        self._logger.propagate = False

    def trace(self, message: str) -> None:
        self._logger.log(TRACE, message, stacklevel=2)

    def debug(self, message: str) -> None:
        self._logger.debug(message, stacklevel=2)

    def info(self, message: str) -> None:
        self._logger.info(message, stacklevel=2)

    def warning(self, message: str) -> None:
        self._logger.warning(message, stacklevel=2)

    def error(self, message: str) -> None:
        self._logger.error(message, stacklevel=2)

    def exception(self, message: str, exc_info: BaseException | None = None) -> None:
        self._logger.exception(message, stacklevel=2, exc_info=exc_info or True)

    def close(self) -> None:
        for handler in self._logger.handlers[:]:
            handler.flush()
            handler.close()
            self._logger.removeHandler(handler)
