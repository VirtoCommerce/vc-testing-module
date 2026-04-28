import re
from functools import cache
from pathlib import Path
from typing import Final

from core.clients.graphql import GraphQLClient

_FRAGMENTS_DIR: Final = Path(__file__).parent.parent / "fragments"
_SPREAD_RE: Final = re.compile(r"\.\.\.([\w]+)")


@cache
def _load_fragments() -> dict[str, str]:
    fragments: dict[str, str] = {}
    for path in _FRAGMENTS_DIR.glob("*.graphql"):
        content = path.read_text(encoding="utf-8")
        for match in re.finditer(r"fragment\s+(\w+)\s+on\s+\w+", content):
            fragments[match.group(1)] = content
    return fragments


def _collect_fragments(operation: str, library: dict[str, str]) -> list[str]:
    collected: dict[str, str] = {}
    pending = set(_SPREAD_RE.findall(operation))
    while pending:
        name = pending.pop()
        if name in collected or name not in library:
            continue
        fragment = library[name]
        collected[name] = fragment
        pending.update(_SPREAD_RE.findall(fragment))
    return list(collected.values())


def gql(operation: str) -> str:
    return operation


class BaseOperations:
    def __init__(self, client: GraphQLClient) -> None:
        self._client = client

    def _build_query(self, operation: str) -> str:
        fragments = _collect_fragments(operation, _load_fragments())
        return "\n".join([*fragments, operation])
