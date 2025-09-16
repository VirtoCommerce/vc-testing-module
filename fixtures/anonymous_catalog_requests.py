from typing import Any, Dict

import allure
import pytest

from fixtures import Auth, WebAPISession


class AnonymousCatalogRequests:
    def __init__(
        self, config: Dict[str, Any], auth: Auth, webapi_client: WebAPISession
    ):
        self.config = config
        self.auth = auth
        self.webapi_client = webapi_client

    def toggle(self, value: bool) -> None:
        self.auth.authenticate(
            username=self.config["admin_username"],
            password=self.config["admin_password"],
        )

        self.webapi_client.patch(
            f"/api/stores/{self.config['store_id']}",
            data=[{"op": "replace", "path": "/settings/1/value", "value": value}],
        )

        self.auth.clear_token()


@pytest.fixture(scope="session")
@allure.title("Fixture to handle anonymous catalog requests")
def anonymous_catalog_requests(
    config: Dict[str, Any], auth: Auth, webapi_client: WebAPISession
) -> AnonymousCatalogRequests:
    return AnonymousCatalogRequests(config, auth, webapi_client)
