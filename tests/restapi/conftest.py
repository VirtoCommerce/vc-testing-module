"""Shared fixtures for REST API tests.

`admin_auth` / `rest_client` / `backend_base_url` live in the root conftest
(tests/conftest.py) since e2e and graphql tests also need REST admin access
to set up state (e.g. locking an organization membership) that has no
GraphQL/UI equivalent.

HAR recording is handled by the root conftest's autouse `har_recorder`
fixture, which hooks into `rest_client._session` automatically.
"""

import pytest


@pytest.fixture(scope="session")
def seed_catalog(dataset: dict) -> dict:
    """The first seeded physical catalog from dataset; use `seed_catalog['id']` / `seed_catalog['name']`."""
    catalogs = dataset.get("catalogs") or []
    if not catalogs:
        pytest.skip("No seeded catalogs in dataset")
    return catalogs[0]


@pytest.fixture(scope="session")
def seed_catalog_id(seed_catalog: dict) -> str:
    return seed_catalog["id"]
