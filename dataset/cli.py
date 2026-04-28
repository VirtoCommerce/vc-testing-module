import argparse
import logging
import sys
from pathlib import Path

from core.global_settings import global_settings
from core.logger import RichLogger
from rich.console import Console

from dataset.dataset_manager import DatasetManager

_LOG_FILE = Path(__file__).parent / "dataset_manager.log"


def main() -> None:
    args = _parse_args()
    console_level = logging.INFO if args.mode == "ci" else logging.DEBUG
    console_width = 200 if args.mode == "ci" else 150
    console = Console(stderr=True, width=console_width, force_terminal=True)
    logger = RichLogger(
        "dataset.manager",
        console_level=console_level,
        log_file=_LOG_FILE,
        console=console,
    )
    manager = DatasetManager.create(global_settings=global_settings, logger=logger)
    if args.seed is None:
        return
    failures = manager.seed(names=args.seed or None)
    if failures:
        logger.error(f"[red]Seeding finished with {failures} failed entit{'y' if failures == 1 else 'ies'}[/red]")
        sys.exit(1)


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed the dataset via WebAPI")
    parser.add_argument(
        "--seed",
        nargs="*",
        metavar="ENTITY",
        help="Entity names in snake_case to seed, e.g. 'platform_settings currencies' (omit to seed all)",
    )
    parser.add_argument(
        "--mode",
        choices=["dev", "ci"],
        default="dev",
        help="Logging mode: dev shows per-item details, ci shows summary only (default: dev)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
