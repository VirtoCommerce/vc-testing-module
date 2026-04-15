from typing import Any

import allure
import pytest

from fixtures.auth import Auth
from fixtures.config import Config
from fixtures.webapi_client import WebAPISession


@pytest.mark.webapi
@allure.feature("Contacts / Organizations (WebAPI)")
@allure.title("Update organization — remove addresses")
def test_update_members_remove_addresses(
    webapi_client: WebAPISession,
    config: Config,
    auth: Auth,
    dataset: dict[str, Any],
):
    with allure.step("Authenticate as admin"):
        auth.authenticate(
            config["ADMIN_USERNAME"],
            config["ADMIN_PASSWORD"],
        )

    organization_id = dataset["organizations"][0]["id"]

    with allure.step(f"GET /api/members/{organization_id}"):
        get_organization = webapi_client.get(f"/api/members/{organization_id}")
        assert get_organization is not None, "Organization is None"

    with allure.step("PUT /api/members — remove addresses"):
        update_data = {
            "id": organization_id,
            "name": get_organization.get("name"),
            "memberType": "Organization",
            "addresses": [],
        }
        webapi_client.put("/api/members", data=update_data)

    with allure.step("Verify addresses were removed"):
        get_updated = webapi_client.get(f"/api/members/{organization_id}")
        assert get_updated is not None, "Updated organization is None"
        assert get_updated.get("addresses") == [] or get_updated.get("addresses") is None, "Addresses were not removed"
