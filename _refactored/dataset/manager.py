import argparse
import logging
import re
from pathlib import Path
from typing import Any

from core.auth.provider import AuthProvider
from core.clients.rest import RestClient
from core.global_settings import GlobalSettings, global_settings
from core.logger import Logger, RichLogger
from dataset.entity import EntityDescriptor
from dataset.resolver import JsonResolver, Resolver

_CURRENT_DIR = Path(__file__).parent
_DATA_DIR = _CURRENT_DIR / "data"
_LOG_FILE = _CURRENT_DIR / "dataset_manager.log"

_PAYLOAD_ITEM_PATTERN = re.compile(r"\{PAYLOAD_ITEM:([^}]+)\}")


class DatasetManager:
    def __init__(
        self, resolver: Resolver, global_settings: GlobalSettings, logger: Logger
    ) -> None:
        self._resolver = resolver
        self._global_settings = global_settings
        self._logger = logger
        self._entities = resolver.load()

    @classmethod
    def create(
        cls, global_settings: GlobalSettings, logger: Logger | None = None
    ) -> "DatasetManager":
        from core.logger import NullLogger

        _logger = logger or NullLogger()
        resolver = JsonResolver(
            global_settings=global_settings, data_dir=_DATA_DIR, logger=_logger
        )
        return cls(resolver=resolver, global_settings=global_settings, logger=_logger)

    @property
    def dataset(self) -> dict[str, list[dict[str, Any]]]:
        return {entity.name: entity.data for entity in self._entities}

    def find_shipping_method(self, code: str, option: str) -> dict[str, Any]:
        method = next(
            (m for m in self.dataset["shipping_methods"] if m["code"] == code),
            None,
        )
        if method is None:
            raise ValueError(f"Shipping method with code='{code}' not found in dataset")
        settings = method.get("settings", [])
        setting = next((s for s in settings if option in s["name"]), None)
        if settings and setting is None:
            raise ValueError(
                f"Shipping method '{code}' has no option matching '{option}' in settings"
            )
        return {
            "code": method["code"],
            "name": method["name"],
            "option": {
                "name": option,
                "price": setting["value"] if setting else None,
            },
        }

    def find_payment_method(self, code: str) -> dict[str, Any]:
        method = next(
            (m for m in self.dataset["payment_methods"] if m["code"] == code),
            None,
        )
        if method is None:
            raise ValueError(f"Payment method with code='{code}' not found in dataset")
        return method

    def seed(self, rest_client: RestClient, names: list[str] | None = None) -> None:
        entities = sorted(self._entities, key=lambda e: e.priority)
        if names:
            entities = [e for e in entities if e.name in names]
        for entity in entities:
            self._seed_entity(entity=entity, rest_client=rest_client)

    def _seed_entity(self, entity: EntityDescriptor, rest_client: RestClient) -> None:
        base_url = self._global_settings.backend_base_url
        if entity.payload_type == "array":
            url = f"{base_url}{entity.endpoint}"
            self._call(
                rest_client=rest_client,
                method=entity.method,
                url=url,
                payload=entity.data,
                entity_name=entity.name,
            )
        else:
            for item in entity.data:
                endpoint = self._resolve_endpoint(
                    endpoint=entity.endpoint, item=item, entity_name=entity.name
                )
                url = f"{base_url}{endpoint}"
                self._call(
                    rest_client=rest_client,
                    method=entity.method,
                    url=url,
                    payload=item,
                    entity_name=entity.name,
                )

    def _resolve_endpoint(
        self, endpoint: str, item: dict[str, Any], entity_name: str
    ) -> str:
        def replace(m: re.Match) -> str:
            field = m.group(1)
            value = item.get(field)
            if value is None:
                self._logger.warning(
                    f"[{entity_name}] PAYLOAD_ITEM field not found: {field}"
                )
                self._logger.debug(
                    f"[{entity_name}] Unresolved placeholder '{m.group(0)}' in endpoint '{endpoint}'"
                )
                return m.group(0)
            return str(value)

        return _PAYLOAD_ITEM_PATTERN.sub(replace, endpoint)

    def _call(
        self,
        rest_client: RestClient,
        method: str,
        url: str,
        payload: Any,
        entity_name: str,
    ) -> None:
        try:
            match method:
                case "POST":
                    rest_client.post(url=url, json=payload)
                case "PUT":
                    rest_client.put(url=url, json=payload)
                case "PATCH":
                    rest_client.patch(url=url, json=payload)
                case "DELETE":
                    rest_client.delete(url=url)
                case "GET":
                    rest_client.get(url=url)
                case _:
                    raise ValueError(f"Unsupported HTTP method: {method}")
            self._logger.info(f"[{entity_name}] {method} {url} OK")
        except Exception as e:
            self._logger.error(f"[{entity_name}] {method} {url} failed: {e}")
            self._logger.trace(f"[{entity_name}] Failed payload: {payload}")


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Seed the dataset via WebAPI")
    parser.add_argument(
        "--seed",
        nargs="*",
        metavar="ENTITY",
        help="Entity names to seed (omit to seed all loaded entities)",
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
    logger = RichLogger(
        "dataset.manager", console_level=console_level, log_file=_LOG_FILE
    )
    auth = AuthProvider(global_settings=global_settings)
    manager = DatasetManager.create(global_settings, logger=logger)
    if args.seed is not None:
        auth.sign_in(
            username=global_settings.admin_username,
            password=global_settings.admin_password,
        )
        with RestClient(global_settings=global_settings, auth=auth) as rest_client:
            manager.seed(rest_client=rest_client, names=args.seed or None)
        auth.sign_out()


if __name__ == "__main__":
    _main()
