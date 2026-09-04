"""REST API operations for VirtoCommerce organization memberships.

Endpoints (VirtoCommerce.CustomerModule.Web.Controllers.Api.OrganizationMembershipController):
  POST   /api/customer/organization-memberships/search              — search
  GET    /api/customer/organization-memberships/user/{userId}/org/{organizationId} — get by user+org
  POST   /api/customer/organization-memberships                     — create
  POST   /api/customer/organization-memberships/{id}/lock           — lock (optionally until lockoutEnd)
  POST   /api/customer/organization-memberships/{id}/unlock         — unlock
  DELETE /api/customer/organization-memberships?ids=                — delete
"""

from datetime import datetime
from typing import Any

import requests

from restapi.operations.base import RestBaseOperations
from restapi.types.organization_membership import OrganizationMembership


class OrganizationMembershipOperations(RestBaseOperations):
    PATH = "/api/customer/organization-memberships"

    def search(self, *, user_id: str | None = None, organization_id: str | None = None, **extra: Any) -> dict:
        payload: dict[str, Any] = {**extra}
        if user_id is not None:
            payload["userId"] = user_id
        if organization_id is not None:
            payload["organizationId"] = organization_id
        return self._client.post(self._url(f"{self.PATH}/search"), json=payload)

    def get_by_user_and_org(self, user_id: str, organization_id: str) -> OrganizationMembership | None:
        """The controller returns 404 when no membership row exists for this pair — that's
        the normal "not found" case here, not a failure, so it's translated to None rather
        than left to propagate as RestClient's HTTPError."""
        try:
            response = self._client.get(self._url(f"{self.PATH}/user/{user_id}/org/{organization_id}"))
        except requests.HTTPError as exc:
            if exc.response is not None and exc.response.status_code == 404:
                return None
            raise
        return OrganizationMembership.model_validate(response) if response else None

    def create(self, *, user_id: str, organization_id: str, **overrides: Any) -> OrganizationMembership:
        payload = {"userId": user_id, "organizationId": organization_id, **overrides}
        response = self._client.post(self._url(self.PATH), json=payload)
        return OrganizationMembership.model_validate(response)

    def delete(self, *membership_ids: str) -> None:
        self._client.delete(self._url(self.PATH), params={"ids": list(membership_ids)})

    def lock(self, membership_id: str, *, lockout_end: datetime | None = None) -> OrganizationMembership:
        payload = {"lockoutEnd": lockout_end.isoformat()} if lockout_end else None
        response = self._client.post(self._url(f"{self.PATH}/{membership_id}/lock"), json=payload)
        return OrganizationMembership.model_validate(response)

    def unlock(self, membership_id: str) -> OrganizationMembership:
        response = self._client.post(self._url(f"{self.PATH}/{membership_id}/unlock"), json=None)
        return OrganizationMembership.model_validate(response)
