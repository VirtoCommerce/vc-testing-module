"""Store module fixtures."""

import uuid
from typing import Any, Callable, Generator

import pytest

from core.clients.rest import RestClient
from restapi.operations import StoreOperations
from restapi.types import Store


@pytest.fixture
def store_ops(rest_client: RestClient, backend_base_url: str) -> StoreOperations:
    return StoreOperations(rest_client, backend_base_url)


@pytest.fixture
def make_store(store_ops: StoreOperations) -> Generator[Callable[..., Store], None, None]:
    created_ids: list[str] = []

    def _make(**overrides: Any) -> Store:
        name = overrides.pop("name", f"QAStore_{uuid.uuid4().hex[:8]}")
        store = store_ops.create(name=name, **overrides)
        created_ids.append(store.id)
        return store

    yield _make

    for sid in reversed(created_ids):
        try:
            store_ops.delete(sid)
        except Exception:
            pass
