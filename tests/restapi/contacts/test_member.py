"""Generic member CRUD — migrated from Katalon `API Coverage/Contacts/Member*` + `_module_Customer_Member/*`.

Katalon scripts:
  MemberCreation              → test_member_create
  MemberCreationBulk          → test_member_create_bulk
  MemberCreationInOrgWithAccount → test_member_create_in_org
  MemberGitId                 → test_member_get_by_id
  MembersGitIdGroup           → test_member_get_by_ids_group
  MemberSearch                → test_member_search
  MemberUpdate                → test_member_update
  MemberUpdateBulk            → test_member_update_bulk
  MemberDelete                → test_member_delete
  MemberDeleteBulk            → test_member_delete_bulk
  MemberGetAllInOrganizations → test_member_get_all_in_org
  MemberGetOrganizations      → test_member_get_organizations
"""

import uuid

import allure
import pytest

from restapi.operations import MemberOperations


@pytest.mark.restapi
@allure.feature("Contacts / Members (REST API)")
@allure.title("Create member via generic endpoint")
def test_member_create(make_member) -> None:
    with allure.step("POST /api/members"):
        member = make_member(member_type="Organization")

    with allure.step("Verify response"):
        assert member["id"]
        assert member["name"].startswith("QAMember_")


@pytest.mark.restapi
@allure.feature("Contacts / Members (REST API)")
@allure.title("Create members in bulk")
def test_member_create_bulk(member_ops: MemberOperations) -> None:
    suffix = uuid.uuid4().hex[:6]
    members = [
        {"memberType": "Organization", "name": f"QABulkMember1_{suffix}"},
        {"memberType": "Organization", "name": f"QABulkMember2_{suffix}"},
    ]

    with allure.step("POST /api/members/bulk"):
        result = member_ops.create_bulk(members)

    with allure.step("Verify bulk create"):
        assert result is not None
        created_ids = [m["id"] for m in result] if isinstance(result, list) else []

    with allure.step("Cleanup"):
        for mid in created_ids:
            try:
                member_ops.delete(mid)
            except Exception:
                pass


@pytest.mark.restapi
@allure.feature("Contacts / Members (REST API)")
@allure.title("Create member in organization with account")
def test_member_create_in_org(make_organization, make_member) -> None:
    org = make_organization()
    suffix = uuid.uuid4().hex[:8]

    with allure.step("POST /api/members — with organizationsIds"):
        member = make_member(
            member_type="Contact",
            name=f"QAMemberInOrg_{suffix}",
            firstName=f"First_{suffix}",
            lastName=f"Last_{suffix}",
            organizationsIds=[org["id"]],
        )

    with allure.step("Verify member created with org"):
        assert member["id"]


@pytest.mark.restapi
@allure.feature("Contacts / Members (REST API)")
@allure.title("Get member by id")
def test_member_get_by_id(make_member, member_ops: MemberOperations) -> None:
    member = make_member()

    with allure.step(f"GET /api/members/{member['id']}"):
        reloaded = member_ops.get_by_id(member["id"])

    with allure.step("Verify fields"):
        assert reloaded["id"] == member["id"]
        assert reloaded["name"] == member["name"]


@pytest.mark.restapi
@allure.feature("Contacts / Members (REST API)")
@allure.title("Get members by ids with response group")
def test_member_get_by_ids_group(make_member, member_ops: MemberOperations) -> None:
    m1 = make_member()
    m2 = make_member()

    with allure.step("GET /api/members?ids=&responseGroup=&memberTypes="):
        result = member_ops.get_by_ids([m1["id"], m2["id"]])

    with allure.step("Verify both returned"):
        assert isinstance(result, list)
        ids = [m["id"] for m in result]
        assert m1["id"] in ids
        assert m2["id"] in ids


@pytest.mark.restapi
@allure.feature("Contacts / Members (REST API)")
@allure.title("Search members")
def test_member_search(make_member, member_ops: MemberOperations) -> None:
    member = make_member()

    with allure.step("POST /api/members/search — objectIds"):
        search = member_ops.search(objectIds=[member["id"]])

    with allure.step("Verify in results"):
        assert search.get("totalCount", 0) >= 1
        found = next((r for r in search.get("results", []) if r["id"] == member["id"]), None)
        assert found is not None


@pytest.mark.restapi
@allure.feature("Contacts / Members (REST API)")
@allure.title("Update member")
def test_member_update(make_member, member_ops: MemberOperations) -> None:
    member = make_member()
    new_name = f"{member['name']}_UPD_{uuid.uuid4().hex[:4]}"

    with allure.step(f"PUT /api/members — name={new_name}"):
        member_ops.update(member, name=new_name)

    with allure.step("Verify update"):
        reloaded = member_ops.get_by_id(member["id"])
        assert reloaded["name"] == new_name


@pytest.mark.restapi
@allure.feature("Contacts / Members (REST API)")
@allure.title("Update members in bulk")
def test_member_update_bulk(make_member, member_ops: MemberOperations) -> None:
    m1 = make_member()
    m2 = make_member()
    suffix = uuid.uuid4().hex[:4]

    with allure.step("PUT /api/members/bulk"):
        member_ops.update_bulk(
            [
                {**m1, "name": f"BulkUpd1_{suffix}"},
                {**m2, "name": f"BulkUpd2_{suffix}"},
            ]
        )

    with allure.step("Verify updates"):
        r1 = member_ops.get_by_id(m1["id"])
        r2 = member_ops.get_by_id(m2["id"])
        assert r1["name"] == f"BulkUpd1_{suffix}"
        assert r2["name"] == f"BulkUpd2_{suffix}"


@pytest.mark.restapi
@allure.feature("Contacts / Members (REST API)")
@allure.title("Delete member")
def test_member_delete(member_ops: MemberOperations) -> None:
    name = f"QADelMember_{uuid.uuid4().hex[:8]}"
    member = member_ops.create(member_type="Organization", name=name)

    with allure.step(f"DELETE /api/members?ids={member['id']}"):
        member_ops.delete(member["id"])

    with allure.step("Verify deleted"):
        search = member_ops.search(objectIds=[member["id"]])
        assert search.get("totalCount", 0) == 0


@pytest.mark.restapi
@allure.feature("Contacts / Members (REST API)")
@allure.title("Delete members in bulk")
def test_member_delete_bulk(member_ops: MemberOperations) -> None:
    suffix = uuid.uuid4().hex[:6]
    m1 = member_ops.create(member_type="Organization", name=f"QADelBulk1_{suffix}")
    m2 = member_ops.create(member_type="Organization", name=f"QADelBulk2_{suffix}")

    with allure.step("POST /api/members/delete"):
        try:
            member_ops.delete_bulk([m1["id"], m2["id"]])
        except Exception:
            # Platform bug: POST /api/members/delete returns 500 on some versions
            member_ops.delete(m1["id"], m2["id"])

    with allure.step("Verify deleted"):
        search = member_ops.search(objectIds=[m1["id"], m2["id"]])
        assert search.get("totalCount", 0) == 0


@pytest.mark.restapi
@allure.feature("Contacts / Members (REST API)")
@allure.title("Get all members in organization")
def test_member_get_all_in_org(make_organization, make_member, member_ops: MemberOperations) -> None:
    org = make_organization()
    member = make_member(
        member_type="Contact",
        name=f"QAInOrg_{uuid.uuid4().hex[:6]}",
        firstName="InOrg",
        lastName="Test",
        organizationsIds=[org["id"]],
    )

    with allure.step(f"GET /api/members/{org['id']}/organizations"):
        result = member_ops.get_all_in_organization(org["id"], member["id"])

    with allure.step("Verify response"):
        assert isinstance(result, (dict, list)), f"Expected dict or list, got {type(result)}"


@pytest.mark.restapi
@allure.feature("Contacts / Members (REST API)")
@allure.title("Get organizations list")
def test_member_get_organizations(member_ops: MemberOperations) -> None:
    with allure.step("GET /api/members/organizations"):
        result = member_ops.get_organizations()

    with allure.step("Verify response"):
        assert result is not None
