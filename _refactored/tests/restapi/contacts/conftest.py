"""Contacts module fixtures — factory fixtures for organizations."""

import uuid
from typing import Any, Callable, Generator

import pytest

from core.clients.rest import RestClient
from restapi.operations import OrganizationOperations


@pytest.fixture
def organization_ops(rest_client: RestClient, backend_base_url: str) -> OrganizationOperations:
    return OrganizationOperations(rest_client, backend_base_url)


@pytest.fixture
def make_organization(
    organization_ops: OrganizationOperations,
) -> Generator[Callable[..., dict], None, None]:
    """Factory: creates a fresh organization per call, cleans up at teardown."""
    created_ids: list[str] = []

    def _make(**overrides: Any) -> dict:
        name = overrides.pop("name", f"QAOrganization_{uuid.uuid4().hex[:8]}")
        org = organization_ops.create(name=name, **overrides)
        created_ids.append(org["id"])
        return org

    yield _make

    for oid in reversed(created_ids):
        try:
            organization_ops.delete(oid)
        except Exception:
            pass
