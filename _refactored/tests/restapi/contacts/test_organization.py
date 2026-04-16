"""Organization CRUD — migrated from Katalon `API Coverage/ModuleContacts/Organization*`."""

import uuid

import allure
import pytest

from restapi.operations import OrganizationOperations


@pytest.mark.restapi
@allure.feature("Contacts / Organizations (REST API)")
@allure.title("Create organization")
def test_organization_create(make_organization):
    with allure.step("POST /api/members"):
        org = make_organization()

    with allure.step("Verify response"):
        assert org["id"], "Organization id missing"
        assert org["name"].startswith("QAOrganization_")
        assert org["memberType"] == "Organization"


@pytest.mark.restapi
@allure.feature("Contacts / Organizations (REST API)")
@allure.title("Get organization by id")
def test_organization_get_by_id(make_organization, organization_ops: OrganizationOperations):
    org = make_organization()

    with allure.step(f"GET /api/members/{org['id']}"):
        reloaded = organization_ops.get_by_id(org["id"])

    with allure.step("Verify fields match"):
        assert reloaded["id"] == org["id"]
        assert reloaded["name"] == org["name"]
        assert reloaded["memberType"] == "Organization"


@pytest.mark.restapi
@allure.feature("Contacts / Organizations (REST API)")
@allure.title("Update organization — rename")
def test_organization_update(make_organization, organization_ops: OrganizationOperations):
    org = make_organization()
    new_name = f"{org['name']}_UPD_{uuid.uuid4().hex[:4]}"

    with allure.step(f"PUT /api/members — rename to {new_name}"):
        organization_ops.update(org, name=new_name)

    with allure.step("Verify rename via GET"):
        reloaded = organization_ops.get_by_id(org["id"])
        assert reloaded["name"] == new_name


@pytest.mark.restapi
@allure.feature("Contacts / Organizations (REST API)")
@allure.title("Search organization by object ids")
def test_organization_search(make_organization, organization_ops: OrganizationOperations):
    org = make_organization()

    with allure.step(f"POST /api/members/search objectIds=[{org['id']}]"):
        search = organization_ops.search(objectIds=[org["id"]])

    with allure.step("Verify organization in results"):
        assert search.get("totalCount", 0) >= 1
        results = search.get("results", [])
        found = next((r for r in results if r["id"] == org["id"]), None)
        assert found is not None


@pytest.mark.restapi
@allure.feature("Contacts / Organizations (REST API)")
@allure.title("Delete organization")
def test_organization_delete(make_organization, organization_ops: OrganizationOperations):
    org = make_organization()

    with allure.step(f"DELETE /api/members?ids={org['id']}"):
        organization_ops.delete(org["id"])

    with allure.step("Verify organization no longer in search"):
        search = organization_ops.search(keyword=org["name"])
        ids = [r["id"] for r in search.get("results", [])]
        assert org["id"] not in ids


@pytest.mark.restapi
@allure.feature("Contacts / Organizations (REST API)")
@allure.title("Update organization — remove addresses")
def test_organization_remove_addresses(make_organization, organization_ops: OrganizationOperations):
    org = make_organization()
    assert org.get("addresses"), "Fresh org should have addresses from the template"

    with allure.step("PUT /api/members — addresses=[]"):
        organization_ops.update(org, addresses=[])

    with allure.step("Verify addresses were removed"):
        updated = organization_ops.get_by_id(org["id"])
        addresses = updated.get("addresses")
        assert addresses == [] or addresses is None
