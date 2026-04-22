import argparse
import logging
from pathlib import Path
from typing import Any, cast

from core.auth.provider import AuthProvider
from core.clients.rest import RestClient
from core.global_settings import GlobalSettings, global_settings
from core.logger import Logger, NullLogger, RichLogger
from rich.console import Console

from dataset.dataset_seeder import DatasetSeeder
from dataset.json_resolver import JsonResolver

_CURRENT_DIR = Path(__file__).parent
_DATA_DIR = _CURRENT_DIR / "data"
_LOG_FILE = _CURRENT_DIR / "dataset_manager.log"


class DatasetManager:
    def __init__(
        self,
        global_settings: GlobalSettings,
        json_resolver: JsonResolver,
        logger: Logger,
    ) -> None:
        self._global_settings = global_settings
        self._json_resolver = json_resolver
        self._dataset = json_resolver.resolve()
        self._logger = logger

    @property
    def dataset(self) -> dict[str, list[dict[str, Any]]]:
        return self._dataset

    def find_shipping_method(self, code: str, option: str) -> dict[str, Any] | None:
        methods = self._dataset.get("shippingMethods", [])
        method = next((m for m in methods if m.get("code") == code), None)
        if method is None:
            return None

        type_name = method.get("typeName", "")
        rate_suffix = f".{type_name}.{option}.Rate"
        settings = cast(list[dict[str, Any]], method.get("settings") or [])
        setting = next(
            (s for s in settings if str(s.get("name", "")).endswith(rate_suffix)),
            None,
        )
        if setting is None:
            return None

        return {
            "code": code,
            "option": {
                "name": option,
                "price": float(cast(float, setting["value"])),
            },
        }

    @classmethod
    def create(cls, global_settings: GlobalSettings, logger: Logger) -> "DatasetManager":
        json_resolver = JsonResolver(data_dir=_DATA_DIR, env_vars=global_settings.env_vars, logger=logger)
        _logger = logger or NullLogger()

        return cls(global_settings=global_settings, json_resolver=json_resolver, logger=_logger)

    def seed(self, names: list[str] | None = None) -> None:
        auth = AuthProvider(self._global_settings)
        auth.sign_in(
            username=self._global_settings.admin_username,
            password=self._global_settings.admin_password,
        )
        try:
            with RestClient(global_settings=self._global_settings, auth=auth) as rest_client:
                seeder = DatasetSeeder(
                    global_settings=self._global_settings,
                    rest_client=rest_client,
                    manifest=self._json_resolver.manifest,
                    dataset=self._json_resolver.raw_data,
                    logger=self._logger,
                )
                seeder.seed(names=names)
        finally:
            auth.sign_out()


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


def _main() -> None:
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
    if args.seed is not None:
        manager.seed(names=args.seed or None)


if __name__ == "__main__":
    _main()
