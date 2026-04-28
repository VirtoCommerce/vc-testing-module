from typing import Any


def topological_sort(
    items: list[dict[str, Any]],
    parent_ref_field: str,
    id_field: str = "id",
) -> list[dict[str, Any]]:
    """Sort items so each parent appears before its children.

    Stable within a topological level (preserves input order among independent items).
    Raises ValueError on missing IDs, duplicate IDs, unknown parent refs, or cycles.
    """
    ids: list[str] = []
    by_id: dict[str, dict[str, Any]] = {}
    for index, item in enumerate(items):
        item_id = item.get(id_field)
        if not isinstance(item_id, str) or not item_id:
            raise ValueError(
                f"Item #{index} has invalid {id_field!r}: expected non-empty string, got {item_id!r}"
            )
        if item_id in by_id:
            raise ValueError(f"Duplicate {id_field}={item_id!r} at item #{index}")
        ids.append(item_id)
        by_id[item_id] = item

    children: dict[str, list[str]] = {item_id: [] for item_id in ids}
    in_degree: dict[str, int] = {item_id: 0 for item_id in ids}
    for item_id in ids:
        parent_id = by_id[item_id].get(parent_ref_field)
        if parent_id is None:
            continue
        if parent_id == item_id:
            raise ValueError(
                f"Item {item_id!r} references itself via {parent_ref_field!r}"
            )
        if parent_id not in by_id:
            raise ValueError(
                f"Item {item_id!r} references unknown parent {parent_id!r} via {parent_ref_field!r}"
            )
        children[parent_id].append(item_id)
        in_degree[item_id] = 1

    queue = [item_id for item_id in ids if in_degree[item_id] == 0]
    result: list[dict[str, Any]] = []
    while queue:
        next_queue: list[str] = []
        for item_id in queue:
            result.append(by_id[item_id])
            for child_id in children[item_id]:
                in_degree[child_id] -= 1
                if in_degree[child_id] == 0:
                    next_queue.append(child_id)
        queue = next_queue

    if len(result) < len(items):
        cycle = _find_cycle(by_id, parent_ref_field, in_degree)
        raise ValueError(
            f"Cycle detected in {parent_ref_field!r} references: {' -> '.join(cycle)}"
        )

    return result


def _find_cycle(
    by_id: dict[str, dict[str, Any]],
    parent_ref_field: str,
    in_degree: dict[str, int],
) -> list[str]:
    """Walk parent refs from any unprocessed node until a node is revisited."""
    start = next(item_id for item_id, d in in_degree.items() if d > 0)
    visited: list[str] = []
    current: str = start
    while current not in visited:
        visited.append(current)
        current = by_id[current][parent_ref_field]
    return visited[visited.index(current):] + [current]
