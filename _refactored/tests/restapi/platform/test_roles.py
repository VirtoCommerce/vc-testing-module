"""Platform roles — migrated from Katalon `API Coverage/ModulePlatform/Roles*`."""

import uuid

import allure
import pytest

from restapi.operations import RoleOperations


@pytest.mark.restapi
@allure.feature("Platform / Roles (REST API)")
@allure.title("Create role")
def test_role_create(make_role, role_ops: RoleOperations):
    with allure.step("POST /api/platform/security/roles"):
        role = make_role(permissions=[{"name": "security:call_api"}])

    with allure.step("Verify role created"):
        assert role["id"]
        assert role["name"].startswith("QARole_")


@pytest.mark.restapi
@allure.feature("Platform / Roles (REST API)")
@allure.title("Get role by name")
def test_role_get_by_name(make_role, role_ops: RoleOperations):
    role = make_role(permissions=[{"name": "security:call_api"}])

    with allure.step(f"GET /api/platform/security/roles/{role['name']}"):
        fetched = role_ops.get_by_name(role["name"])

    with allure.step("Verify fields"):
        assert fetched["id"] == role["id"]
        assert fetched["name"] == role["name"]


@pytest.mark.restapi
@allure.feature("Platform / Roles (REST API)")
@allure.title("Search roles")
def test_role_search(make_role, role_ops: RoleOperations):
    role = make_role()

    with allure.step("POST /api/platform/security/roles/search"):
        search = role_ops.search(keyword=role["name"])

    with allure.step("Verify role in results"):
        assert search.get("totalCount", 0) >= 1
        found = next((r for r in search.get("results", []) if r["id"] == role["id"]), None)
        assert found is not None


@pytest.mark.restapi
@allure.feature("Platform / Roles (REST API)")
@allure.title("Update role — change description")
def test_role_update(make_role, role_ops: RoleOperations):
    role = make_role()
    new_desc = f"Updated_{uuid.uuid4().hex[:6]}"

    with allure.step(f"PUT /api/platform/security/roles — description={new_desc}"):
        role_ops.update(role, description=new_desc)

    with allure.step("Verify update"):
        fetched = role_ops.get_by_name(role["name"])
        assert fetched["description"] == new_desc


@pytest.mark.restapi
@allure.feature("Platform / Roles (REST API)")
@allure.title("Delete role")
def test_role_delete(make_role, role_ops: RoleOperations):
    role = make_role()

    with allure.step(f"DELETE /api/platform/security/roles?ids={role['id']}"):
        role_ops.delete(role["id"])

    with allure.step("Verify role removed"):
        search = role_ops.search(keyword=role["name"])
        ids = [r["id"] for r in search.get("results", [])]
        assert role["id"] not in ids


@pytest.mark.restapi
@allure.feature("Platform / Roles (REST API)")
@allure.title("Remove permission from role")
def test_role_remove_permission(make_role, role_ops: RoleOperations):
    role = make_role(permissions=[{"name": "security:call_api"}, {"name": "cache:reset"}])

    with allure.step("Remove one permission"):
        role_ops.update(role, permissions=[{"name": "security:call_api"}])

    with allure.step("Verify permission removed"):
        fetched = role_ops.get_by_name(role["name"])
        perm_names = [p.get("name") for p in fetched.get("permissions", [])]
        assert "cache:reset" not in perm_names
        assert "security:call_api" in perm_names


@pytest.mark.restapi
@allure.feature("Platform / Roles (REST API)")
@allure.title("Get all permissions")
def test_role_get_all_permissions(role_ops: RoleOperations):
    with allure.step("GET /api/platform/security/permissions"):
        permissions = role_ops.get_all_permissions()

    with allure.step("Verify permissions list"):
        assert isinstance(permissions, list)
        assert len(permissions) > 0
        names = [p.get("id", p.get("name", "")) for p in permissions]
        assert any("cache:reset" in n for n in names), f"Expected 'cache:reset' permission, got: {names[:10]}..."
