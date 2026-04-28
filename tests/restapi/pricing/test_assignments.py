"""Pricelist assignments — migrated from Katalon `API Coverage/ModulePricing/pricelistAssignment*`.

Katalon scripts:
  pricelistAssignmentCreate              → test_assignment_create
  pricelistAssignmentEdit                → test_assignment_update
  pricelistAssignmentEdit_AlternativeWay → test_assignment_update_alt
  pricelistAssignmentGetNew              → test_assignment_get_new
  pricelistAssignmentsGet                → test_assignment_get_by_id
  pricelistAssignmentsSearch             → test_assignment_search
  pricelistAssignmentDelete              → test_assignment_delete
  pricelistAssignmentsDeleteFiltered     → test_assignment_delete_filtered
"""

import uuid

import allure
import pytest

from restapi.operations import PricelistAssignmentOperations


@pytest.mark.restapi
@allure.feature("Pricing / Assignments (REST API)")
@allure.title("Create pricelist assignment")
def test_assignment_create(make_assignment) -> None:
    with allure.step("POST /api/pricing/assignments"):
        assignment = make_assignment()

    with allure.step("Verify response"):
        assert assignment.id
        assert assignment.name.startswith("QAAssign_")


@pytest.mark.restapi
@allure.feature("Pricing / Assignments (REST API)")
@allure.title("Update pricelist assignment")
def test_assignment_update(make_assignment, assignment_ops: PricelistAssignmentOperations) -> None:
    assignment = make_assignment()
    new_name = f"{assignment.name}_UPD_{uuid.uuid4().hex[:4]}"

    with allure.step(f"PUT /api/pricing/assignments — name={new_name}"):
        assignment_ops.update(assignment, name=new_name)

    with allure.step("Verify update"):
        reloaded = assignment_ops.get_by_id(assignment.id)
        assert reloaded.name == new_name


@pytest.mark.restapi
@allure.feature("Pricing / Assignments (REST API)")
@allure.title("Update pricelist assignment — alternative way")
def test_assignment_update_alt(make_assignment, assignment_ops: PricelistAssignmentOperations) -> None:
    assignment = make_assignment()
    new_desc = f"Updated description {uuid.uuid4().hex[:6]}"

    with allure.step("PUT /api/pricing/assignments — description update"):
        assignment_ops.update(assignment, description=new_desc)

    with allure.step("Verify"):
        reloaded = assignment_ops.get_by_id(assignment.id)
        assert (reloaded.model_extra or {}).get("description") == new_desc


@pytest.mark.restapi
@allure.feature("Pricing / Assignments (REST API)")
@allure.title("Get new assignment template")
def test_assignment_get_new(assignment_ops: PricelistAssignmentOperations) -> None:
    with allure.step("GET /api/pricing/assignments/new"):
        template = assignment_ops.get_new()

    with allure.step("Verify template"):
        assert template is not None


@pytest.mark.restapi
@allure.feature("Pricing / Assignments (REST API)")
@allure.title("Get assignment by id")
def test_assignment_get_by_id(make_assignment, assignment_ops: PricelistAssignmentOperations) -> None:
    assignment = make_assignment()

    with allure.step(f"GET /api/pricing/assignments/{assignment.id}"):
        reloaded = assignment_ops.get_by_id(assignment.id)

    with allure.step("Verify fields"):
        assert reloaded.id == assignment.id
        assert reloaded.name == assignment.name


@pytest.mark.restapi
@allure.feature("Pricing / Assignments (REST API)")
@allure.title("Search assignments by pricelist")
def test_assignment_search(make_pricelist, make_assignment, assignment_ops: PricelistAssignmentOperations) -> None:
    pricelist = make_pricelist()
    assignment = make_assignment(pricelist=pricelist)

    with allure.step(f"GET /api/pricing/assignments?pricelistIds={pricelist.id}"):
        result = assignment_ops.search(pricelist_id=pricelist.id)

    with allure.step("Verify assignment in results"):
        items = result if isinstance(result, list) else result.get("results", [])
        found = next((r for r in items if r["id"] == assignment.id), None)
        assert found is not None


@pytest.mark.restapi
@allure.feature("Pricing / Assignments (REST API)")
@allure.title("Delete pricelist assignment")
def test_assignment_delete(assignment_ops: PricelistAssignmentOperations, make_pricelist, seed_catalog_id: str) -> None:
    pricelist = make_pricelist()
    name = f"QADelAssign_{uuid.uuid4().hex[:8]}"
    assignment = assignment_ops.create(pricelist_id=pricelist.id, catalog_id=seed_catalog_id, name=name)

    with allure.step(f"DELETE /api/pricing/assignments?ids={assignment.id}"):
        assignment_ops.delete(assignment.id)


@pytest.mark.restapi
@allure.feature("Pricing / Assignments (REST API)")
@allure.title("Delete assignments filtered by search phrase")
def test_assignment_delete_filtered(
    assignment_ops: PricelistAssignmentOperations, make_pricelist, seed_catalog_id: str
) -> None:
    pricelist = make_pricelist()
    unique = f"QAFiltered_{uuid.uuid4().hex[:8]}"
    assignment_ops.create(pricelist_id=pricelist.id, catalog_id=seed_catalog_id, name=unique)

    with allure.step(f"DELETE /api/pricing/filteredAssignments?SearchPhrase={unique}"):
        assignment_ops.delete_filtered(unique)
