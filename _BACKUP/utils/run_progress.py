from collections import deque
from typing import Callable

from rich.console import Console, Group
from rich.live import Live
from rich.progress import Progress
from rich.text import Text


def run_progress(
    title: str,
    total: int,
    console: Console,
    task_fn: Callable[[Progress, int, Callable[[str], None]], None],
) -> None:
    progress = Progress(console=console)
    task_id = progress.add_task(title, total=total)
    messages: deque[str] = deque(maxlen=5)

    def render() -> Group:
        rows = [Text.from_markup(entry) for entry in messages]
        return Group(*rows, progress)

    with Live(render(), console=console, refresh_per_second=10):
        task_fn(progress, task_id)
