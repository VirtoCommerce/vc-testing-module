"""Organization CRUD — migrated from Katalon `API Coverage/ModuleContacts/Organization*`.

Originals:
- OrganizationCreate          -> test_organization_create
- OrganizationGetById         -> test_organization_get_by_id
- OrganizationUpdate          -> test_organization_update
- OrganizationDelete          -> test_organization_delete
- UpdateMembersRemoveAddress  -> test_update_members_remove_addresses

Key differences from Katalon:
- Each test creates its own organization via `make_organization`, cleaned up
  at teardown — parallel-safe under pytest-xdist. No dataset-entity mutation.
- Unique names via uuid suffix.
- Auth via Bearer token (password grant) instead of the `api_key` header.
"""

import uuid

import allure
import pytest

from webapi_operations.contacts.organization_operations import OrganizationOperations


@pytest.mark.webapi
@allure.feature("Contacts / Organizations (WebAPI)")
@allure.title("Create organization")
def test_organization_create(make_organization):
    with allure.step("POST /api/members"):
        org = make_organization()

    with allure.step("Verify response contains expected fields"):
        assert org["id"], "Organization id missing from create response"
        assert org["name"].startswith("QAOrganization_"), f"Unexpected name: {org['name']}"
        assert org["memberType"] == "Organization", f"Expected memberType=Organization, got {org['memberType']}"


@pytest.mark.webapi
@allure.feature("Contacts / Organizations (WebAPI)")
@allure.title("Get organization by id")
def test_organization_get_by_id(make_organization, organization_operations: OrganizationOperations):
    org = make_organization()

    with allure.step(f"GET /api/members/{org['id']}"):
        reloaded = organization_operations.get_by_id(org["id"])

    with allure.step("Verify returned fields match"):
        assert reloaded["id"] == org["id"], f"Expected id {org['id']}, got {reloaded['id']}"
        assert reloaded["name"] == org["name"], f"Expected name {org['name']}, got {reloaded['name']}"
        assert (
            reloaded["memberType"] == "Organization"
        ), f"Expected memberType=Organization, got {reloaded['memberType']}"


@pytest.mark.webapi
@allure.feature("Contacts / Organizations (WebAPI)")
@allure.title("Update organization — rename")
def test_organization_update(make_organization, organization_operations: OrganizationOperations):
    org = make_organization()
    new_name = f"{org['name']}_UPD_{uuid.uuid4().hex[:4]}"

    with allure.step(f"PUT /api/members — rename to {new_name}"):
        organization_operations.update(org, name=new_name)

    with allure.step("Verify rename via GET"):
        reloaded = organization_operations.get_by_id(org["id"])
        assert reloaded["name"] == new_name, f"Expected {new_name}, got {reloaded['name']}"


@pytest.mark.webapi
@allure.feature("Contacts / Organizations (WebAPI)")
@allure.title("Search organization by object ids")
def test_organization_search(make_organization, organization_operations: OrganizationOperations):
    org = make_organization()

    with allure.step(f"POST /api/members/search objectIds=[{org['id']}]"):
        search = organization_operations.search(objectIds=[org["id"]])

    with allure.step("Verify created organization appears in results"):
        assert search.get("totalCount", 0) >= 1, "Expected at least one result"
        results = search.get("results", [])
        found = next((r for r in results if r["id"] == org["id"]), None)
        assert found is not None, f"Created organization {org['id']} not in search results"
        assert found["name"] == org["name"], f"Expected name {org['name']}, got {found['name']}"


@pytest.mark.webapi
@allure.feature("Contacts / Organizations (WebAPI)")
@allure.title("Delete organization")
def test_organization_delete(make_organization, organization_operations: OrganizationOperations):
    org = make_organization()

    with allure.step(f"DELETE /api/members?ids={org['id']}"):
        organization_operations.delete(org["id"])

    with allure.step("Verify organization no longer appears in search"):
        search = organization_operations.search(keyword=org["name"])
        ids = [r["id"] for r in search.get("results", [])]
        assert org["id"] not in ids, "Organization still present after DELETE"

    # Factory teardown will attempt to delete again and silently swallow the error.


@pytest.mark.webapi
@allure.feature("Contacts / Organizations (WebAPI)")
@allure.title("Update organization — remove addresses")
def test_update_members_remove_addresses(make_organization, organization_operations: OrganizationOperations):
    # ORGANIZATION_TEMPLATE seeds one address, so a fresh org is enough to
    # exercise address removal without touching the shared dataset.
    org = make_organization()
    assert org.get("addresses"), "Fresh org should have at least one address from the template"

    with allure.step("PUT /api/members — addresses=[]"):
        organization_operations.update(org, addresses=[])

    with allure.step("Verify addresses were removed"):
        updated = organization_operations.get_by_id(org["id"])
        assert updated is not None, "Updated organization is None"
        addresses = updated.get("addresses")
        assert addresses == [] or addresses is None, f"Addresses were not removed: {addresses}"
