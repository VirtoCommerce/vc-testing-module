import json
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from core.global_settings import GlobalSettings
from core.logger import Logger
from dataset.entity import EntityDescriptor

_ENV_PATTERN = re.compile(r"\{ENV:([^}]+)\}")


class Resolver(ABC):
    @abstractmethod
    def load(self) -> list[EntityDescriptor]: ...


class JsonResolver(Resolver):
    def __init__(self, global_settings: GlobalSettings, data_dir: Path, logger: Logger):
        self._data_dir = data_dir
        self._logger = logger
        self._env = global_settings.env_vars

    def _resolve_env(self, value: Any, entity_name: str) -> Any:
        if isinstance(value, str):

            def replace(m: re.Match) -> str:
                var_name = m.group(1)
                env_value = self._env.get(var_name)
                if env_value is None:
                    self._logger.warning(f"[{entity_name}] Env var not set: {var_name}")
                    self._logger.debug(
                        f"[{entity_name}] Placeholder '{m.group(0)}' left unresolved in data"
                    )
                    return m.group(0)
                return env_value

            return _ENV_PATTERN.sub(replace, value)
        if isinstance(value, dict):
            return {k: self._resolve_env(v, entity_name) for k, v in value.items()}
        if isinstance(value, list):
            return [self._resolve_env(item, entity_name) for item in value]
        return value

    def _load_file(self, path: Path) -> EntityDescriptor:
        with open(file=path, encoding="utf-8") as file:
            raw = json.load(file)
        raw["endpoint"] = self._resolve_env(raw.get("endpoint", ""), entity_name=path.stem)
        raw["data"] = self._resolve_env(raw.get("data", []), entity_name=path.stem)
        return EntityDescriptor(name=path.stem, **raw)

    def load(self) -> list[EntityDescriptor]:
        entities: list[EntityDescriptor] = []

        if not self._data_dir.exists():
            raise FileNotFoundError(f"Data directory not found: {self._data_dir}")

        paths = sorted(self._data_dir.glob("*.json"))
        if not paths:
            raise FileNotFoundError(f"No JSON files found in: {self._data_dir}")

        for path in paths:
            try:
                entity = self._load_file(path=path)
                entities.append(entity)
            except Exception as e:
                self._logger.warning(f"Failed to load {path.name}: {e}")
                continue

        return entities
