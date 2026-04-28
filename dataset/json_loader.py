import json
from pathlib import Path
from typing import Any


def load_entity_files(entity_dir: Path) -> list[dict[str, Any]]:
    """Recursively load all *.json files under entity_dir as raw dicts.

    Returns an empty list if the directory does not exist.
    Files are returned in path-sorted order for deterministic results.
    Raises ValueError if any file is invalid JSON or its top-level value is not an object.
    """
    if not entity_dir.exists():
        return []

    items: list[dict[str, Any]] = []
    for path in sorted(entity_dir.rglob("*.json")):
        try:
            with open(file=path, encoding="utf-8") as file:
                content = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {path}: {e}") from e
        if not isinstance(content, dict):
            raise ValueError(
                f"Expected JSON object at top level of {path}, got {type(content).__name__}"
            )
        items.append(content)
    return items
