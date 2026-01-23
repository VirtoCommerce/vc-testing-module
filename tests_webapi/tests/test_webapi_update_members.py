import os
from typing import Any

import allure

from fixtures.auth import Auth
from fixtures.config import Config
from fixtures.webapi_client import WebAPISession

@allure.feature("Update members (WebAPI)")
def test_update_members_remove_addresses(
    webapi_client: WebAPISession,
    config: Config,   
    auth: Auth,
    dataset: dict[str, Any],
):
    print(f"{os.linesep}Running test to remove addresses from organization...", end=" ")

    auth.authenticate(
        config["ADMIN_USERNAME"],
        config["ADMIN_PASSWORD"],
    )

    organization_id = dataset['organizations'][0]['id']
    
    # Get current organization data
    get_organization = webapi_client.get(f"/api/members/{organization_id}")
    print(f"Current organization: {get_organization}")
    assert get_organization is not None, "Organization is None"
    
    # Update organization to remove addresses (empty array)
    update_data = {
        "id": organization_id,
        "name": get_organization.get("name"),
        "memberType": "Organization",
        "addresses": []
    }
    
    update_result = webapi_client.put(f"/api/members", data=update_data)
    print(f"Update result: {update_result}")
    
    # Verify addresses were removed
    get_updated = webapi_client.get(f"/api/members/{organization_id}")
    print(f"Updated organization: {get_updated}")
    assert get_updated is not None, "Updated organization is None"
    assert get_updated.get("addresses") == [] or get_updated.get("addresses") is None, "Addresses were not removed"