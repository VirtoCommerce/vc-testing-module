import copy
from pathlib import Path
from typing import Any, cast

import inflection
from core.auth.provider import AuthProvider
from core.clients.rest import RestClient
from core.global_settings import GlobalSettings
from core.logger import Logger

from dataset.dataset_seeder import DatasetSeeder, fetch_installed_modules
from dataset.json_loader import load_entity_files
from dataset.manifest import ManifestEntry, load_manifest
from dataset.request_builder import build_requests, substitute_env
from dataset.topological_sorter import topological_sort

_DATA_DIR = Path(__file__).parent / "data"
_MANIFEST_PATH = _DATA_DIR / "manifest.json"


class DatasetManager:
    def __init__(self, global_settings: GlobalSettings, logger: Logger) -> None:
        self._global_settings = global_settings
        self._logger = logger
        self._manifest = load_manifest(_MANIFEST_PATH)
        self._items_by_entry = self._load_items()
        self._dataset = {
            inflection.camelize(name, uppercase_first_letter=False): copy.deepcopy(items)
            for name, items in self._items_by_entry.items()
        }

    @classmethod
    def create(cls, global_settings: GlobalSettings, logger: Logger) -> "DatasetManager":
        return cls(global_settings=global_settings, logger=logger)

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

    def seed(self, names: list[str] | None = None) -> int:
        """Seed the dataset and return the number of failed entities.

        An entity is considered failed if any of: building its requests raises,
        a request returns an HTTP error, or any other exception bubbles up from
        the seeder. Other entities continue to be processed regardless.
        """
        entries = self._select_entries(names)
        if not entries:
            return 0

        auth = AuthProvider(self._global_settings.backend_base_url)
        auth.sign_in(
            username=self._global_settings.admin_username,
            password=self._global_settings.admin_password,
        )
        try:
            with RestClient(global_settings=self._global_settings, auth=auth) as rest_client:
                base_url = self._global_settings.backend_base_url
                installed_modules = fetch_installed_modules(rest_client, base_url, self._logger)
                seeder = DatasetSeeder(rest_client=rest_client, logger=self._logger)
                failures = 0
                for entry in entries:
                    if not self._seed_entry(entry, installed_modules, base_url, seeder):
                        failures += 1
                return failures
        finally:
            auth.sign_out()

    def _load_items(self) -> dict[str, list[dict[str, Any]]]:
        env_vars = self._global_settings.env_vars
        result: dict[str, list[dict[str, Any]]] = {}
        for entry in self._manifest:
            raw = load_entity_files(_DATA_DIR / entry.name)
            if not raw:
                continue
            resolved = [substitute_env(item, env_vars) for item in raw]
            if entry.parent_ref_field:
                resolved = topological_sort(resolved, entry.parent_ref_field)
            result[entry.name] = resolved
        return result

    def _select_entries(self, names: list[str] | None) -> list[ManifestEntry]:
        if names is None:
            return list(self._manifest)
        known = {e.name for e in self._manifest}
        unknown = [n for n in names if n not in known]
        if unknown:
            raise ValueError(f"Unknown entity name(s): {unknown}")
        return [e for e in self._manifest if e.name in names]

    def _seed_entry(
        self,
        entry: ManifestEntry,
        installed_modules: set[str],
        base_url: str,
        seeder: DatasetSeeder,
    ) -> bool:
        if installed_modules and entry.module_id not in installed_modules:
            self._logger.warning(
                f"[yellow]Skipping {entry.name}:[/yellow] module {entry.module_id} is not installed"
            )
            return True
        items = self._items_by_entry.get(entry.name)
        if not items:
            self._logger.warning(f"[yellow]No data for entity:[/yellow] {entry.name}")
            return True
        try:
            requests = build_requests(
                entry=entry,
                items=items,
                env_vars=self._global_settings.env_vars,
                base_url=base_url,
                installed_modules=installed_modules or None,
                logger=self._logger,
            )
            seeder.seed(requests)
        except Exception as e:
            self._logger.error(
                f"[red]\\[{entry.name}] Aborted:[/red] {type(e).__name__}: {e}"
            )
            return False
        return True


if __name__ == "__main__":
    from dataset.cli import main

    main()
