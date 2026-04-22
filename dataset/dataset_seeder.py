import json
import re
import time
from typing import Any, cast

from core.clients.rest import RestClient
from core.global_settings import GlobalSettings
from core.logger import Logger

from dataset.manifest_entry import ManifestEntry

_PAYLOAD_ITEM_PATTERN = re.compile(r"\{PAYLOAD_ITEM:([^}]+)\}")
_ENV_PATTERN = re.compile(r"\{ENV:([^}]+)\}")


class DatasetSeeder:
    def __init__(
        self,
        global_settings: GlobalSettings,
        rest_client: RestClient,
        manifest: list[ManifestEntry],
        dataset: dict[str, list[dict[str, Any]]],
        logger: Logger,
    ) -> None:
        self._global_settings = global_settings
        self._rest_client = rest_client
        self._manifest = manifest
        self._dataset = dataset
        self._logger = logger
        self._installed_modules: set[str] = set()

    def _fetch_installed_modules(self) -> set[str]:
        base_url = self._global_settings.backend_base_url
        url = f"{base_url}/api/platform/modules"
        response = self._rest_client.get(url=url)
        if not isinstance(response, list):
            self._logger.warning("Unexpected modules response format")
            return set()
        module_ids = {m["id"] for m in response if "id" in m and m.get("isInstalled") is True}
        self._logger.info(f"Fetched {len(module_ids)} installed module(s)")
        return module_ids

    def _filter_by_installed_modules(self, item: dict[str, Any], entity_name: str) -> dict[str, Any]:
        if not self._installed_modules:
            return item
        filtered: dict[str, Any] = {}
        for key, value in item.items():
            if isinstance(value, list) and value and isinstance(value[0], dict):
                original = cast(list[dict[str, Any]], value)
                kept = [v for v in original if "moduleId" not in v or v["moduleId"] in self._installed_modules]
                skipped = [v for v in original if "moduleId" in v and v["moduleId"] not in self._installed_modules]
                for v in skipped:
                    label = v.get("name") or v.get("code") or v.get("id") or "unknown"
                    self._logger.warning(
                        f"[yellow]\\[{entity_name}] Filtered {key}:[/yellow] "
                        f"\"{label}\" — module {v['moduleId']} is not installed"
                    )
                filtered[key] = kept
            else:
                filtered[key] = value
        return filtered

    def seed(self, names: list[str] | None = None) -> None:
        self._installed_modules = self._fetch_installed_modules()
        entries = self._manifest
        if names:
            entries = [e for e in entries if e.name in names]
        for entry in entries:
            if self._installed_modules and entry.module_id not in self._installed_modules:
                self._logger.warning(
                    f"[yellow]Skipping {entry.name}:[/yellow] module {entry.module_id} is not installed"
                )
                continue
            items = self._dataset.get(entry.name, [])
            if not items:
                self._logger.warning(f"[yellow]No data for entity:[/yellow] {entry.name}")
                continue
            self._seed_entity(entry=entry, items=items)

    @staticmethod
    def _has_unresolved_env(value: Any) -> bool:
        return bool(_ENV_PATTERN.search(json.dumps(value)))

    @staticmethod
    def _item_label(item: dict[str, Any]) -> str | None:
        return item.get("name") or item.get("code") or item.get("id")

    def _seed_entity(
        self,
        entry: ManifestEntry,
        items: list[dict[str, Any]],
    ) -> None:
        base_url = self._global_settings.backend_base_url
        if entry.payload_type == "array":
            endpoint = self._resolve_env_in_endpoint(entry.endpoint, entry.name)
            url = f"{base_url}{endpoint}"
            self._call(
                method=entry.method,
                url=url,
                payload=items,
                log_prefix=f"Seeding \\[{entry.name}]",
            )
        else:
            for item in items:
                item = self._filter_by_installed_modules(item, entry.name)
                label = self._item_label(item)
                if self._has_unresolved_env(item):
                    self._logger.warning(
                        f"[yellow]\\[{entry.name}] Skipping {label or 'item'}:[/yellow] " f"unresolved ENV placeholders"
                    )
                    continue
                endpoint = self._resolve_endpoint(endpoint=entry.endpoint, item=item, entity_name=entry.name)
                url = f"{base_url}{endpoint}"
                prefix = f"Seeding \\[{entry.name}: {label}]" if label else f"Seeding \\[{entry.name}]"
                self._call(
                    method=entry.method,
                    url=url,
                    payload=item,
                    log_prefix=prefix,
                )

    def _resolve_env_in_endpoint(self, endpoint: str, entity_name: str) -> str:
        env_vars = self._global_settings.env_vars

        def replace(m: re.Match[str]) -> str:
            var_name = m.group(1)
            value = env_vars.get(var_name)
            if value is None:
                self._logger.warning(f"\\[{entity_name}] ENV variable not set: {var_name}")
                return m.group(0)
            return value

        return _ENV_PATTERN.sub(replace, endpoint)

    def _resolve_endpoint(self, endpoint: str, item: dict[str, Any], entity_name: str) -> str:
        def replace(m: re.Match[str]) -> str:
            field = m.group(1)
            value = item.get(field)
            if value is None:
                self._logger.warning(f"\\[{entity_name}] PAYLOAD_ITEM field not found: {field}")
                return m.group(0)
            return str(value)

        endpoint = self._resolve_env_in_endpoint(endpoint, entity_name)
        return _PAYLOAD_ITEM_PATTERN.sub(replace, endpoint)

    def _call(
        self,
        method: str,
        url: str,
        payload: Any,
        log_prefix: str,
    ) -> None:
        start = time.perf_counter()
        try:
            match method:
                case "POST":
                    self._rest_client.post(url=url, json=payload)
                case "PUT":
                    self._rest_client.put(url=url, json=payload)
                case "PATCH":
                    self._rest_client.patch(url=url, json=payload)
                case "DELETE":
                    self._rest_client.delete(url=url)
                case "GET":
                    self._rest_client.get(url=url)
                case _:
                    raise ValueError(f"Unsupported HTTP method: {method}")
            elapsed = time.perf_counter() - start
            self._logger.info(f"{log_prefix} {method} {url} [green]DONE[/green] \\[{elapsed:.2f}s]")
        except Exception as e:
            elapsed = time.perf_counter() - start
            self._logger.error(f"{log_prefix} {method} {url} [red]FAILED[/red] \\[{elapsed:.2f}s]: {e}")
