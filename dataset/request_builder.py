import re
from dataclasses import dataclass
from typing import Any, cast

from core.logger import Logger

from dataset.manifest import ManifestEntry

_ENV_PATTERN = re.compile(r"\{ENV:([^}]+)\}")
_PAYLOAD_ITEM_PATTERN = re.compile(r"\{PAYLOAD_ITEM:([^}]+)\}")


@dataclass(frozen=True)
class PreparedRequest:
    method: str
    url: str
    payload: dict[str, Any] | list[dict[str, Any]]
    label: str


def build_requests(
    entry: ManifestEntry,
    items: list[dict[str, Any]],
    env_vars: dict[str, str],
    base_url: str,
    installed_modules: set[str] | None,
    logger: Logger,
) -> list[PreparedRequest]:
    """Resolve placeholders, filter by installed modules, and build seed requests.

    `installed_modules=None` disables module filtering (used when modules info is unavailable).
    Raises ValueError on any unresolved {ENV:...} or {PAYLOAD_ITEM:...} placeholder —
    the caller decides how to react. The whole entry either builds cleanly or fails.
    """
    endpoint = substitute_env(entry.endpoint, env_vars)
    _assert_no_unresolved_env(endpoint, f"endpoint {entry.endpoint!r}", entry.name)

    prepared_items = [
        _filter_by_modules(substitute_env(item, env_vars), installed_modules, entry.name, logger)
        for item in items
    ]
    for item in prepared_items:
        _assert_no_unresolved_env(item, f"item {_label(item) or '<unlabeled>'!r}", entry.name)

    if entry.payload_type == "array":
        return [PreparedRequest(
            method=entry.method,
            url=f"{base_url}{endpoint}",
            payload=prepared_items,
            label=entry.name,
        )]

    requests: list[PreparedRequest] = []
    for item in prepared_items:
        url = _substitute_payload_item(endpoint, item)
        missing = _PAYLOAD_ITEM_PATTERN.findall(url)
        if missing:
            raise ValueError(
                f"[{entry.name}] Item {_label(item) or '<unlabeled>'!r} is missing "
                f"PAYLOAD_ITEM fields {missing} required by endpoint {entry.endpoint!r}"
            )
        item_label = _label(item)
        label = f"{entry.name}: {item_label}" if item_label else entry.name
        requests.append(PreparedRequest(
            method=entry.method,
            url=f"{base_url}{url}",
            payload=item,
            label=label,
        ))
    return requests


def substitute_env(value: Any, env_vars: dict[str, str]) -> Any:
    """Recursively substitute {ENV:NAME} placeholders. Leaves unmatched placeholders intact."""
    if isinstance(value, str):
        return _ENV_PATTERN.sub(lambda m: env_vars.get(m.group(1), m.group(0)), value)
    if isinstance(value, dict):
        d = cast(dict[str, Any], value)
        return {k: substitute_env(v, env_vars) for k, v in d.items()}
    if isinstance(value, list):
        items = cast(list[Any], value)
        return [substitute_env(item, env_vars) for item in items]
    return value


def _assert_no_unresolved_env(value: Any, where: str, entity_name: str) -> None:
    missing = _find_unresolved_env(value)
    if missing:
        raise ValueError(
            f"[{entity_name}] Unresolved ENV variables {sorted(set(missing))} in {where}"
        )


def _find_unresolved_env(value: Any) -> list[str]:
    if isinstance(value, str):
        return _ENV_PATTERN.findall(value)
    if isinstance(value, dict):
        d = cast(dict[str, Any], value)
        return [name for v in d.values() for name in _find_unresolved_env(v)]
    if isinstance(value, list):
        items = cast(list[Any], value)
        return [name for v in items for name in _find_unresolved_env(v)]
    return []


def _substitute_payload_item(endpoint: str, item: dict[str, Any]) -> str:
    def replace(m: re.Match[str]) -> str:
        value = item.get(m.group(1))
        return m.group(0) if value is None else str(value)

    return _PAYLOAD_ITEM_PATTERN.sub(replace, endpoint)


def _filter_by_modules(
    item: dict[str, Any],
    installed_modules: set[str] | None,
    entity_name: str,
    logger: Logger,
) -> dict[str, Any]:
    if installed_modules is None:
        return item
    filtered: dict[str, Any] = {}
    for key, value in item.items():
        if isinstance(value, list) and value and isinstance(value[0], dict):
            original = cast(list[dict[str, Any]], value)
            kept: list[dict[str, Any]] = []
            for entry in original:
                module_id = entry.get("moduleId")
                if module_id is None or module_id in installed_modules:
                    kept.append(entry)
                    continue
                label = entry.get("name") or entry.get("code") or entry.get("id") or "unknown"
                logger.warning(
                    f"[yellow]\\[{entity_name}] Filtered {key}:[/yellow] "
                    f"\"{label}\" — module {module_id} is not installed"
                )
            filtered[key] = kept
        else:
            filtered[key] = value
    return filtered


def _label(item: dict[str, Any]) -> str | None:
    return item.get("name") or item.get("code") or item.get("id")
