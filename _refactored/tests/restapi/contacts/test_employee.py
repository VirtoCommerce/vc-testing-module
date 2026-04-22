"""Employee CRUD — migrated from Katalon `API Coverage/Contacts/Employees*` + `_module_Customer/employees*`.

Katalon scripts:
  EmployeesCreation     → test_employee_create
  EmployeesGet          → test_employee_get
  EmployeesUpdateBulk   → test_employee_update_bulk
  employeesSearch       → test_employee_search
  employeesDeleteBulk   → test_employee_delete_bulk
"""

import uuid

import allure
import pytest

from restapi.operations import EmployeeOperations


@pytest.mark.restapi
@allure.feature("Contacts / Employees (REST API)")
@allure.title("Create employee")
def test_employee_create(make_employee) -> None:
    with allure.step("POST /api/employees"):
        emp = make_employee()

    with allure.step("Verify response"):
        assert emp["id"]
        assert emp["memberType"] == "Employee"
        assert emp["firstName"].startswith("QAEmp_")


@pytest.mark.restapi
@allure.feature("Contacts / Employees (REST API)")
@allure.title("Get employee by id")
def test_employee_get(make_employee, employee_ops: EmployeeOperations) -> None:
    emp = make_employee()

    with allure.step(f"GET /api/employees?ids={emp['id']}"):
        result = employee_ops.get_by_ids([emp["id"]])

    with allure.step("Verify returned"):
        assert isinstance(result, list)
        assert len(result) >= 1
        assert result[0]["id"] == emp["id"]


@pytest.mark.restapi
@allure.feature("Contacts / Employees (REST API)")
@allure.title("Search employees")
def test_employee_search(make_employee, employee_ops: EmployeeOperations) -> None:
    emp = make_employee()

    with allure.step("POST /api/members/search — memberType=Employee, objectIds"):
        search = employee_ops.search(objectIds=[emp["id"]])

    with allure.step("Verify employee in results"):
        assert search.get("totalCount", 0) >= 1
        found = next((r for r in search.get("results", []) if r["id"] == emp["id"]), None)
        assert found is not None


@pytest.mark.restapi
@allure.feature("Contacts / Employees (REST API)")
@allure.title("Update employees in bulk")
def test_employee_update_bulk(make_employee, employee_ops: EmployeeOperations) -> None:
    e1 = make_employee()
    e2 = make_employee()
    suffix = uuid.uuid4().hex[:4]

    with allure.step("POST /api/employees/bulk"):
        employee_ops.update_bulk(
            [
                {**e1, "firstName": f"BulkEmp1_{suffix}"},
                {**e2, "firstName": f"BulkEmp2_{suffix}"},
            ]
        )

    with allure.step("Verify updates"):
        r1 = employee_ops.get_by_ids([e1["id"]])[0]
        r2 = employee_ops.get_by_ids([e2["id"]])[0]
        assert r1["firstName"] == f"BulkEmp1_{suffix}"
        assert r2["firstName"] == f"BulkEmp2_{suffix}"


@pytest.mark.restapi
@allure.feature("Contacts / Employees (REST API)")
@allure.title("Delete employees in bulk")
def test_employee_delete_bulk(employee_ops: EmployeeOperations) -> None:
    suffix = uuid.uuid4().hex[:6]
    e1 = employee_ops.create(first_name=f"QADelEmp1_{suffix}", last_name="Del")
    e2 = employee_ops.create(first_name=f"QADelEmp2_{suffix}", last_name="Del")

    with allure.step("DELETE /api/members?ids=..."):
        employee_ops.delete(e1["id"], e2["id"])

    with allure.step("Verify deleted"):
        search = employee_ops.search(objectIds=[e1["id"], e2["id"]])
        assert search.get("totalCount", 0) == 0
