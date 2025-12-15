from typing import Any

import allure
import pytest

from .auth import Auth
from .webapi_client import WebAPISession


class AnonymousCatalogRequests:
    def __init__(
        self, config: dict[str, Any], auth: Auth, webapi_client: WebAPISession
    ):
        self.config = config
        self.auth = auth
        self.webapi_client = webapi_client

    def toggle(self, value: bool) -> None:
        self.auth.authenticate(
            username=self.config["ADMIN_USERNAME"],
            password=self.config["ADMIN_PASSWORD"],
        )

        self.webapi_client.patch(
            f"/api/stores/{self.config['STORE_ID']}",
            data=[{"op": "replace", "path": "/settings/1/value", "value": value}],
        )

        self.auth.clear_token()


@pytest.fixture(scope="session")
@allure.title("Fixture to handle anonymous catalog requests")
def anonymous_catalog_requests(
    config: dict[str, Any], auth: Auth, webapi_client: WebAPISession
) -> AnonymousCatalogRequests:
    return AnonymousCatalogRequests(config, auth, webapi_client)
