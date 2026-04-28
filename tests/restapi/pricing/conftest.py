"""Pricing module fixtures — operations + factory fixtures for pricelists, prices, assignments."""

import logging
import uuid
from typing import Any, Callable, Generator

import pytest

from core.clients.rest import RestClient
from restapi.operations import PricelistAssignmentOperations, PricelistOperations, PriceOperations
from restapi.types import Pricelist, PricelistAssignment

logger = logging.getLogger(__name__)


@pytest.fixture
def pricelist_ops(rest_client: RestClient, backend_base_url: str) -> PricelistOperations:
    return PricelistOperations(rest_client, backend_base_url)


@pytest.fixture
def price_ops(rest_client: RestClient, backend_base_url: str) -> PriceOperations:
    return PriceOperations(rest_client, backend_base_url)


@pytest.fixture
def assignment_ops(rest_client: RestClient, backend_base_url: str) -> PricelistAssignmentOperations:
    return PricelistAssignmentOperations(rest_client, backend_base_url)


@pytest.fixture
def make_pricelist(pricelist_ops: PricelistOperations) -> Generator[Callable[..., Pricelist], None, None]:
    created_ids: list[str] = []

    def _make(**overrides: Any) -> Pricelist:
        name = overrides.pop("name", f"QAPricelist_{uuid.uuid4().hex[:8]}")
        pricelist = pricelist_ops.create(name=name, **overrides)
        created_ids.append(pricelist.id)
        return pricelist

    yield _make

    for pid in reversed(created_ids):
        try:
            pricelist_ops.delete(pid)
        except Exception as e:
            logger.warning("Cleanup failed for pricelist %s: %s", pid, e)


@pytest.fixture
def make_assignment(
    assignment_ops: PricelistAssignmentOperations,
    make_pricelist: Callable[..., Pricelist],
    seed_catalog_id: str,
) -> Generator[Callable[..., PricelistAssignment], None, None]:
    created_ids: list[str] = []

    def _make(
        *, pricelist: Pricelist | None = None, catalog_id: str | None = None, **overrides: Any
    ) -> PricelistAssignment:
        if pricelist is None:
            pricelist = make_pricelist()
        name = overrides.pop("name", f"QAAssign_{uuid.uuid4().hex[:8]}")
        assignment = assignment_ops.create(
            pricelist_id=pricelist.id,
            catalog_id=catalog_id or seed_catalog_id,
            name=name,
            **overrides,
        )
        created_ids.append(assignment.id)
        return assignment

    yield _make

    for aid in reversed(created_ids):
        try:
            assignment_ops.delete(aid)
        except Exception as e:
            logger.warning("Cleanup failed for pricelist assignment %s: %s", aid, e)
