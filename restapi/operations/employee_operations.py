"""REST API operations for VirtoCommerce employees.

Endpoints verified from Katalon Object Repository:
  POST   /api/employees           — create
  GET    /api/employees?ids=      — get by ids
  POST   /api/members/search      — search (shared member search)
  POST   /api/employees/bulk      — update bulk
"""

from typing import Any

from restapi.operations.base import RestBaseOperations
from restapi.types import Employee


class EmployeeOperations(RestBaseOperations):
    PATH = "/api/employees"

    def create(self, *, first_name: str, last_name: str, **overrides: Any) -> Employee:
        payload: dict[str, Any] = {
            "memberType": "Employee",
            "firstName": first_name,
            "lastName": last_name,
            "name": f"{first_name} {last_name}",
            **overrides,
        }
        response = self._client.post(self._url(self.PATH), json=payload)
        return Employee.model_validate(response)

    def get_by_ids(self, employee_ids: list[str]) -> list[Employee]:
        response = self._client.get(self._url(self.PATH), params={"ids": employee_ids})
        return [Employee.model_validate(e) for e in response or []]

    def search(self, *, keyword: str | None = None, skip: int = 0, take: int = 20, **extra: Any) -> dict:
        payload: dict[str, Any] = {
            "memberType": "Employee",
            "deepSearch": True,
            "sort": "name:asc",
            "skip": skip,
            "take": take,
            **extra,
        }
        if keyword is not None:
            payload["searchPhrase"] = keyword
        return self._client.post(self._url("/api/members/search"), json=payload)

    def update_bulk(self, employees: list[dict]) -> list[Employee]:
        response = self._client.post(self._url(f"{self.PATH}/bulk"), json=employees)
        return [Employee.model_validate(e) for e in response or []]

    def delete(self, *employee_ids: str) -> None:
        self._client.delete(self._url("/api/members"), params={"ids": list(employee_ids)})
