from abc import ABC, abstractmethod

TRACE = 5


class Logger(ABC):
    @abstractmethod
    def trace(self, message: str) -> None: ...

    @abstractmethod
    def debug(self, message: str) -> None: ...

    @abstractmethod
    def info(self, message: str) -> None: ...

    @abstractmethod
    def warning(self, message: str) -> None: ...

    @abstractmethod
    def error(self, message: str) -> None: ...

    @abstractmethod
    def exception(
        self, message: str, exc_info: BaseException | None = None
    ) -> None: ...

    def close(self) -> None:
        pass
