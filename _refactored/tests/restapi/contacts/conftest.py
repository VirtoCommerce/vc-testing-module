"""Contacts module fixtures — operations + factory fixtures for contacts, organizations, employees, members, vendors."""

import uuid
from typing import Any, Callable, Generator

import pytest

from core.clients.rest import RestClient
from restapi.constants import ADDRESS_TEMPLATE, CONTACT_TEMPLATE, ORGANIZATION_TEMPLATE
from restapi.operations import (
    ContactOperations,
    EmployeeOperations,
    MemberOperations,
    OrganizationOperations,
    VendorOperations,
)


# ---------------------------------------------------------------- ops fixtures


@pytest.fixture
def contact_ops(rest_client: RestClient, backend_base_url: str) -> ContactOperations:
    return ContactOperations(rest_client, backend_base_url)


@pytest.fixture
def organization_ops(rest_client: RestClient, backend_base_url: str) -> OrganizationOperations:
    return OrganizationOperations(rest_client, backend_base_url)


@pytest.fixture
def employee_ops(rest_client: RestClient, backend_base_url: str) -> EmployeeOperations:
    return EmployeeOperations(rest_client, backend_base_url)


@pytest.fixture
def member_ops(rest_client: RestClient, backend_base_url: str) -> MemberOperations:
    return MemberOperations(rest_client, backend_base_url)


@pytest.fixture
def vendor_ops(rest_client: RestClient, backend_base_url: str) -> VendorOperations:
    return VendorOperations(rest_client, backend_base_url)


# ---------------------------------------------------------------- factories


@pytest.fixture
def make_contact(contact_ops: ContactOperations) -> Generator[Callable[..., dict], None, None]:
    """Factory: creates a fresh contact per call, cleans up at teardown."""
    created_ids: list[str] = []

    def _make(**overrides: Any) -> dict:
        suffix = uuid.uuid4().hex[:8]
        first_name = overrides.pop("first_name", f"QAFirst_{suffix}")
        last_name = overrides.pop("last_name", f"QALast_{suffix}")
        contact = contact_ops.create(first_name=first_name, last_name=last_name, **overrides)
        created_ids.append(contact["id"])
        return contact

    yield _make

    for cid in reversed(created_ids):
        try:
            contact_ops.delete(cid)
        except Exception:
            pass


@pytest.fixture
def make_organization(organization_ops: OrganizationOperations) -> Generator[Callable[..., dict], None, None]:
    """Factory: creates a fresh organization per call, cleans up at teardown."""
    created_ids: list[str] = []

    def _make(**overrides: Any) -> dict:
        name = overrides.pop("name", f"QAOrg_{uuid.uuid4().hex[:8]}")
        org = organization_ops.create(name=name, **overrides)
        created_ids.append(org["id"])
        return org

    yield _make

    for oid in reversed(created_ids):
        try:
            organization_ops.delete(oid)
        except Exception:
            pass


@pytest.fixture
def make_employee(employee_ops: EmployeeOperations) -> Generator[Callable[..., dict], None, None]:
    """Factory: creates a fresh employee per call, cleans up at teardown."""
    created_ids: list[str] = []

    def _make(**overrides: Any) -> dict:
        suffix = uuid.uuid4().hex[:8]
        first_name = overrides.pop("first_name", f"QAEmp_{suffix}")
        last_name = overrides.pop("last_name", f"QAEmpLast_{suffix}")
        emp = employee_ops.create(first_name=first_name, last_name=last_name, **overrides)
        created_ids.append(emp["id"])
        return emp

    yield _make

    for eid in reversed(created_ids):
        try:
            employee_ops.delete(eid)
        except Exception:
            pass


@pytest.fixture
def make_member(member_ops: MemberOperations) -> Generator[Callable[..., dict], None, None]:
    """Factory: creates a fresh member via generic endpoint, cleans up at teardown."""
    created_ids: list[str] = []

    def _make(*, member_type: str = "Organization", **overrides: Any) -> dict:
        name = overrides.pop("name", f"QAMember_{uuid.uuid4().hex[:8]}")
        member = member_ops.create(member_type=member_type, name=name, **overrides)
        created_ids.append(member["id"])
        return member

    yield _make

    for mid in reversed(created_ids):
        try:
            member_ops.delete(mid)
        except Exception:
            pass
