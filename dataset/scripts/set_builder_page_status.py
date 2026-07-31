"""Apply a page-builder grouped-page status transition.

Publishing and archiving a page is a backend workflow, not a settable field, so
the dataset seeds every grouped page as ``Draft``. This script transitions a
chosen page to a target status on demand:

    python -m dataset.scripts.set_builder_page_status --page-id <grouped-page-id> --status Published
    python -m dataset.scripts.set_builder_page_status --page-id <grouped-page-id> --status Archived

``--page-id`` takes the grouped page **id** — the stable key the workflow
endpoints use (``/grouped/publishing/{id}``, ``/grouped/archive?ids={id}``).
Names are not guaranteed unique, so the id avoids ambiguity and needs no lookup.

Endpoint mapping:
    Published -> POST /api/page-builder-pages/grouped/publishing/{id}?publish=true
    Archived  -> POST /api/page-builder-pages/grouped/archive?ids={id}
"""

import argparse
import logging
import sys
from pathlib import Path

from core.auth.provider import AuthProvider
from core.clients.rest import RestClient
from core.global_settings import global_settings
from core.logger import Logger, RichLogger
from rich.console import Console

_GROUPED = "/api/page-builder-pages/grouped"
_LOG_FILE = Path(__file__).parent.parent / "dataset_manager.log"
_STATUSES = ("Published", "Archived")


def apply_status(rest_client: RestClient, base_url: str, page_id: str, status: str, logger: Logger) -> None:
    """Transition a single grouped page to `status`. Raises on HTTP error."""
    if status == "Published":
        rest_client.post(f"{base_url}{_GROUPED}/publishing/{page_id}", json={}, params={"publish": "true"})
    elif status == "Archived":
        rest_client.post(f"{base_url}{_GROUPED}/archive", json={}, params={"ids": page_id})
    else:
        raise ValueError(f"Unsupported --status {status!r}; expected one of {list(_STATUSES)}")
    logger.info(f"\\[{page_id}] [green]{status}[/green]")


def main() -> None:
    args = _parse_args()
    console_level = logging.INFO if args.mode == "ci" else logging.DEBUG
    console = Console(stderr=True, width=200 if args.mode == "ci" else 150, force_terminal=True)
    logger = RichLogger("dataset.builder_page_status", console_level=console_level, log_file=_LOG_FILE, console=console)

    base_url = global_settings.backend_base_url
    auth = AuthProvider(base_url)
    auth.sign_in(username=global_settings.admin_username, password=global_settings.admin_password)
    try:
        with RestClient(global_settings=global_settings, auth=auth) as rest_client:
            apply_status(rest_client, base_url, args.page_id, args.status, logger)
    except Exception as e:
        logger.error(f"[red]Failed to set {args.page_id!r} to {args.status!r}:[/red] {type(e).__name__}: {e}")
        sys.exit(1)
    finally:
        auth.sign_out()


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Apply a grouped-page status transition after seeding")
    parser.add_argument(
        "--page-id",
        required=True,
        metavar="PAGE_ID",
        help="Grouped page id (e.g. 'acme-store-grouped-page-about-store')",
    )
    parser.add_argument(
        "--status",
        required=True,
        choices=_STATUSES,
        help="Target status to apply to the page",
    )
    parser.add_argument(
        "--mode",
        choices=["dev", "ci"],
        default="dev",
        help="Logging mode: dev shows detail, ci shows summary only (default: dev)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    main()
