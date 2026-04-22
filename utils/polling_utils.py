import time
from typing import Callable, TypeVar

T = TypeVar("T")


def poll_until(
    fetch: Callable[[], T | None],
    predicate: Callable[[T], bool],
    attempts: int,
    interval: int,
) -> T | None:
    """Poll *fetch* up to *attempts* times, sleeping *interval* seconds between tries.

    Returns the first result for which *predicate* is ``True``,
    or ``None`` if all attempts are exhausted or *fetch* keeps returning ``None``.
    """
    for _ in range(attempts):
        result = fetch()
        if result is not None and predicate(result):
            return result
        time.sleep(interval)
    return None
