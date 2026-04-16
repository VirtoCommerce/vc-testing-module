from core.logger.base import Logger


class NullLogger(Logger):
    def trace(self, message: str) -> None:
        pass

    def debug(self, message: str) -> None:
        pass

    def info(self, message: str) -> None:
        pass

    def warning(self, message: str) -> None:
        pass

    def error(self, message: str) -> None:
        pass

    def exception(self, message: str, exc_info: BaseException | None = None) -> None:
        pass
