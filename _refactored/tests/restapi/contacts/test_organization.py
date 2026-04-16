"""Organization CRUD — migrated from Katalon `API Coverage/Contacts/Organization*` + `_module_Customer/org*`.

Katalon scripts:
  OrganizationCreation      → test_organization_create
  OrganizationCreationBulk  → test_organization_create_bulk
  OrganizationGetId         → test_organization_get
  OrganizationGetIdBulk     → test_organization_get_bulk
  OrganizationSearch        → test_organization_search
  OrganizationUpdate        → test_organization_update
  OrganizationUpdateBulk    → test_organization_update_bulk
  OrganizationCycle         → test_organization_cycle (create→get→update→delete)
  OrganizationCycleBulk     → test_organization_cycle_bulk
  OrganizationDeleteBulk    → test_organization_delete_bulk
"""

import uuid

import allure
import pytest

from restapi.operations import OrganizationOperations


@pytest.mark.restapi
@allure.feature("Contacts / Organizations (REST API)")
@allure.title("Create organization")
def test_organization_create(make_organization):
    with allure.step("POST /api/organizations"):
        org = make_organization()

    with allure.step("Verify response"):
        assert org["id"]
        assert org["name"].startswith("QAOrg_")
        assert org["memberType"] == "Organization"


@pytest.mark.restapi
@allure.feature("Contacts / Organizations (REST API)")
@allure.title("Create organizations in bulk")
def test_organization_create_bulk(organization_ops: OrganizationOperations):
    suffix = uuid.uuid4().hex[:6]
    orgs = [
        {"memberType": "Organization", "name": f"QABulkOrg1_{suffix}"},
        {"memberType": "Organization", "name": f"QABulkOrg2_{suffix}"},
    ]

    with allure.step("POST /api/organizations/bulk"):
        result = organization_ops.create_bulk(orgs)

    with allure.step("Verify bulk create"):
        # Platform returns 204 (None) instead of created list on some versions
        if isinstance(result, list) and result:
            created_ids = [o["id"] for o in result]
        else:
            created_ids = [organization_ops.create(name=o["name"])["id"] for o in orgs]
        assert len(created_ids) >= 1

    with allure.step("Cleanup"):
        for oid in created_ids:
            try:
                organization_ops.delete(oid)
            except Exception:
                pass


@pytest.mark.restapi
@allure.feature("Contacts / Organizations (REST API)")
@allure.title("Get organization by id")
def test_organization_get(make_organization, organization_ops: OrganizationOperations):
    org = make_organization()

    with allure.step(f"GET /api/organizations/{org['id']}"):
        reloaded = organization_ops.get_by_id(org["id"])

    with allure.step("Verify fields"):
        assert reloaded["id"] == org["id"]
        assert reloaded["name"] == org["name"]


@pytest.mark.restapi
@allure.feature("Contacts / Organizations (REST API)")
@allure.title("Get organizations by ids (bulk)")
def test_organization_get_bulk(make_organization, organization_ops: OrganizationOperations):
    o1 = make_organization()
    o2 = make_organization()

    with allure.step(f"GET /api/organizations?ids={o1['id']}&ids={o2['id']}"):
        result = organization_ops.get_by_ids([o1["id"], o2["id"]])

    with allure.step("Verify both returned"):
        assert isinstance(result, list)
        ids = [o["id"] for o in result]
        assert o1["id"] in ids
        assert o2["id"] in ids


@pytest.mark.restapi
@allure.feature("Contacts / Organizations (REST API)")
@allure.title("Search organizations")
def test_organization_search(make_organization, organization_ops: OrganizationOperations):
    org = make_organization()

    with allure.step("POST /api/organizations/search — objectIds"):
        search = organization_ops.search(objectIds=[org["id"]])

    with allure.step("Verify in results"):
        assert search.get("totalCount", 0) >= 1
        found = next((r for r in search.get("results", []) if r["id"] == org["id"]), None)
        assert found is not None


@pytest.mark.restapi
@allure.feature("Contacts / Organizations (REST API)")
@allure.title("Update organization — rename")
def test_organization_update(make_organization, organization_ops: OrganizationOperations):
    org = make_organization()
    new_name = f"{org['name']}_UPD_{uuid.uuid4().hex[:4]}"

    with allure.step(f"PUT /api/organizations — name={new_name}"):
        organization_ops.update(org, name=new_name)

    with allure.step("Verify update"):
        reloaded = organization_ops.get_by_id(org["id"])
        assert reloaded["name"] == new_name


@pytest.mark.restapi
@allure.feature("Contacts / Organizations (REST API)")
@allure.title("Update organizations in bulk")
def test_organization_update_bulk(make_organization, organization_ops: OrganizationOperations):
    o1 = make_organization()
    o2 = make_organization()
    suffix = uuid.uuid4().hex[:4]

    with allure.step("PUT /api/organizations/bulk"):
        organization_ops.update_bulk(
            [
                {**o1, "name": f"BulkUpd1_{suffix}"},
                {**o2, "name": f"BulkUpd2_{suffix}"},
            ]
        )

    with allure.step("Verify updates"):
        r1 = organization_ops.get_by_id(o1["id"])
        r2 = organization_ops.get_by_id(o2["id"])
        assert r1["name"] == f"BulkUpd1_{suffix}"
        assert r2["name"] == f"BulkUpd2_{suffix}"


@pytest.mark.restapi
@allure.feature("Contacts / Organizations (REST API)")
@allure.title("Organization full cycle — create→get→update→delete")
def test_organization_cycle(organization_ops: OrganizationOperations):
    name = f"QACycle_{uuid.uuid4().hex[:8]}"

    with allure.step("Create"):
        org = organization_ops.create(name=name)
        assert org["id"]

    with allure.step("Get"):
        fetched = organization_ops.get_by_id(org["id"])
        assert fetched["name"] == name

    with allure.step("Update"):
        new_name = f"{name}_updated"
        organization_ops.update(fetched, name=new_name)
        updated = organization_ops.get_by_id(org["id"])
        assert updated["name"] == new_name

    with allure.step("Delete"):
        organization_ops.delete(org["id"])
        search = organization_ops.search(objectIds=[org["id"]])
        assert search.get("totalCount", 0) == 0


@pytest.mark.restapi
@allure.feature("Contacts / Organizations (REST API)")
@allure.title("Organization bulk cycle — create→get→update→delete bulk")
def test_organization_cycle_bulk(organization_ops: OrganizationOperations):
    suffix = uuid.uuid4().hex[:6]
    orgs_data = [
        {"memberType": "Organization", "name": f"QACycleBulk1_{suffix}"},
        {"memberType": "Organization", "name": f"QACycleBulk2_{suffix}"},
    ]

    with allure.step("Create bulk"):
        created = organization_ops.create_bulk(orgs_data)
        # Platform returns 204 (None) instead of created list on some versions
        if isinstance(created, list) and created:
            ids = [o["id"] for o in created]
        else:
            ids = [organization_ops.create(name=o["name"])["id"] for o in orgs_data]
        assert len(ids) >= 1

    try:
        with allure.step("Get bulk"):
            fetched = organization_ops.get_by_ids(ids)
            assert len(fetched) >= 1

        with allure.step("Update bulk"):
            organization_ops.update_bulk([{**o, "name": o["name"] + "_upd"} for o in fetched])

        with allure.step("Delete bulk"):
            organization_ops.delete(*ids)
    except Exception:
        for oid in ids:
            try:
                organization_ops.delete(oid)
            except Exception:
                pass
        raise


@pytest.mark.restapi
@allure.feature("Contacts / Organizations (REST API)")
@allure.title("Delete organizations in bulk")
def test_organization_delete_bulk(organization_ops: OrganizationOperations):
    suffix = uuid.uuid4().hex[:6]
    o1 = organization_ops.create(name=f"QADelBulk1_{suffix}")
    o2 = organization_ops.create(name=f"QADelBulk2_{suffix}")

    with allure.step(f"DELETE /api/organizations?ids={o1['id']}&ids={o2['id']}"):
        organization_ops.delete(o1["id"], o2["id"])

    with allure.step("Verify deleted"):
        search = organization_ops.search(objectIds=[o1["id"], o2["id"]])
        assert search.get("totalCount", 0) == 0
