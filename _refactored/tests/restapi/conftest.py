"""Shared fixtures for REST API tests.

Provides:
- `admin_auth` — session-scoped AuthProvider signed in as admin
- `rest_client` — function-scoped RestClient with admin auth
- `backend_base_url` — convenience string for operations constructors

HAR recording is handled by the root conftest's autouse `har_recorder`
fixture, which hooks into `rest_client._session` automatically.
"""

from typing import Generator

import pytest

from core.auth import AuthProvider
from core.clients.rest import RestClient
from core.global_settings import GlobalSettings


@pytest.fixture(scope="session")
def admin_auth(global_settings: GlobalSettings) -> AuthProvider:
    """Session-scoped admin auth — signed in once, reused across all REST tests."""
    provider = AuthProvider(global_settings)
    provider.sign_in(global_settings.admin_username, global_settings.admin_password)
    return provider


@pytest.fixture
def rest_client(global_settings: GlobalSettings, admin_auth: AuthProvider) -> Generator[RestClient, None, None]:
    with RestClient(global_settings=global_settings, auth=admin_auth) as client:
        yield client


@pytest.fixture(scope="session")
def backend_base_url(global_settings: GlobalSettings) -> str:
    return global_settings.backend_base_url


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
