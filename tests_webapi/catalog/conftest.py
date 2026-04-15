import uuid
from typing import Any, Callable

import pytest

from fixtures.auth import Auth
from fixtures.config import Config
from fixtures.webapi_client import WebAPISession
from webapi_operations.catalog.catalog_operations import CatalogOperations


@pytest.fixture
def catalog_operations(webapi_client: WebAPISession) -> CatalogOperations:
    """Thin wrapper fixture to avoid constructing CatalogOperations in every test."""
    return CatalogOperations(webapi_client)


@pytest.fixture
def make_catalog(
    catalog_operations: CatalogOperations,
    auth: Auth,
    config: Config,
) -> Callable[..., dict]:
    """Factory that creates a fresh catalog per call and cleans up at teardown.

    Usage:
        def test_x(make_catalog):
            catalog = make_catalog()                          # default name + template
            catalog = make_catalog(name="custom-name")        # override name
            catalog = make_catalog(isVirtual=True)            # override template field

    Authenticates as admin once per test (idempotent — Auth caches the token).
    Cleanup silently swallows errors so a test failure can't leak into teardown.
    """
    created_ids: list[str] = []

    def _make(**overrides: Any) -> dict:
        # Authenticate once per worker — subsequent calls within the same session
        # already have a valid token. Avoids hammering /connect/token when a test
        # creates multiple catalogs, and reduces cross-worker collisions on startup.
        if auth.token_data is None or not auth.token_data.access_token:
            auth.authenticate(config["ADMIN_USERNAME"], config["ADMIN_PASSWORD"])
        name = overrides.pop("name", f"QACatalog_{uuid.uuid4().hex[:8]}")
        catalog = catalog_operations.create(name=name, **overrides)
        created_ids.append(catalog["id"])
        return catalog

    yield _make

    for cid in created_ids:
        try:
            catalog_operations.delete(cid)
        except Exception:
            pass
