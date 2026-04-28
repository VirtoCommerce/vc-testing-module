import json
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, get_args

HttpMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
PayloadType = Literal["single", "array"]

_VALID_METHODS = frozenset(get_args(HttpMethod))
_VALID_PAYLOAD_TYPES = frozenset(get_args(PayloadType))


@dataclass(frozen=True)
class ManifestEntry:
    name: str
    module_id: str
    method: HttpMethod
    endpoint: str
    payload_type: PayloadType
    parent_ref_field: str | None = None


def load_manifest(path: Path) -> list[ManifestEntry]:
    try:
        with open(file=path, encoding="utf-8") as file:
            raw = json.load(file)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in manifest {path}: {e}") from e

    if not isinstance(raw, list):
        raise ValueError(f"Manifest must be a JSON array, got {type(raw).__name__}: {path}")

    entries: list[ManifestEntry] = []
    for index, item in enumerate(raw):
        if not isinstance(item, dict):
            raise ValueError(f"Manifest entry #{index} must be an object: {path}")
        try:
            entry = ManifestEntry(**item)
        except TypeError as e:
            name = item.get("name", "<unnamed>")
            raise ValueError(f"Invalid manifest entry #{index} ({name}): {e}") from e
        _validate(entry, index, path)
        entries.append(entry)

    return entries


def _validate(entry: ManifestEntry, index: int, path: Path) -> None:
    location = f"manifest entry #{index} ({entry.name}) in {path}"
    if entry.method not in _VALID_METHODS:
        raise ValueError(
            f"Invalid method {entry.method!r} in {location}; expected one of {sorted(_VALID_METHODS)}"
        )
    if entry.payload_type not in _VALID_PAYLOAD_TYPES:
        raise ValueError(
            f"Invalid payload_type {entry.payload_type!r} in {location}; "
            f"expected one of {sorted(_VALID_PAYLOAD_TYPES)}"
        )
    if not entry.name or not entry.endpoint or not entry.module_id:
        raise ValueError(f"Empty name/endpoint/module_id in {location}")
