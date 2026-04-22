import json
import re
from pathlib import Path
from typing import Any, cast

import inflection
from core.logger import Logger

from dataset.manifest_entry import ManifestEntry

_ENV_PATTERN = re.compile(r"\{ENV:([^}]+)\}")


class JsonResolver:
    def __init__(self, data_dir: Path, env_vars: dict[str, str], logger: Logger) -> None:
        self._data_dir = data_dir
        self._env_vars = env_vars
        self._logger = logger
        self._manifest_path = data_dir / "manifest.json"
        self._manifest: list[ManifestEntry] = []
        self._raw_data: dict[str, list[dict[str, Any]]] = {}

    @property
    def manifest(self) -> list[ManifestEntry]:
        return self._manifest

    @property
    def raw_data(self) -> dict[str, list[dict[str, Any]]]:
        return self._raw_data

    def _load_manifest(self) -> list[ManifestEntry]:
        with open(file=self._manifest_path, encoding="utf-8") as file:
            raw = json.load(file)
        return [ManifestEntry(**entry) for entry in raw]

    def _validate_directories(self, manifest: list[ManifestEntry]) -> None:
        manifest_names = {entry.name for entry in manifest}
        existing_dirs = {p.name for p in self._data_dir.iterdir() if p.is_dir()}
        missing = manifest_names - existing_dirs
        if missing:
            self._logger.warning(
                f"[yellow]Manifest entries have no matching directories:[/yellow] {', '.join(sorted(missing))}"
            )
        empty = [name for name in manifest_names & existing_dirs if not list((self._data_dir / name).glob("*.json"))]
        if empty:
            self._logger.warning(f"[yellow]Directories contain no JSON files:[/yellow] {', '.join(sorted(empty))}")

    def _resolve_env(self, value: Any, entity_name: str) -> Any:
        if isinstance(value, str):

            def replace(m: re.Match[str]) -> str:
                var_name = m.group(1)
                env_value = self._env_vars.get(var_name)
                if env_value is None:
                    self._logger.warning(f"[yellow]\\[{entity_name}] ENV variable not set:[/yellow] {var_name}")
                    return m.group(0)
                return env_value

            return _ENV_PATTERN.sub(replace, value)
        if isinstance(value, dict):
            d = cast(dict[str, Any], value)
            return {k: self._resolve_env(v, entity_name) for k, v in d.items()}
        if isinstance(value, list):
            items = cast(list[Any], value)
            return [self._resolve_env(item, entity_name) for item in items]
        return value

    @staticmethod
    def _has_unresolved_env(value: Any) -> bool:
        raw = json.dumps(value)
        return bool(_ENV_PATTERN.search(raw))

    def _load_entity_items(self, name: str) -> list[dict[str, Any]]:
        entity_dir = self._data_dir / name
        items: list[dict[str, Any]] = []
        for path in sorted(entity_dir.glob("*.json")):
            with open(file=path, encoding="utf-8") as file:
                raw = json.load(file)
            items.append(self._resolve_env(raw, name))
        return items

    def resolve(self) -> dict[str, list[dict[str, Any]]]:
        if not self._data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {self._data_dir}")

        self._manifest = self._load_manifest()
        self._validate_directories(self._manifest)

        import copy

        dataset: dict[str, list[dict[str, Any]]] = {}
        for entry in self._manifest:
            items = self._load_entity_items(entry.name)
            if items:
                self._raw_data[entry.name] = items
                key = inflection.camelize(entry.name, uppercase_first_letter=False)
                dataset[key] = copy.deepcopy(items)
        return dataset
