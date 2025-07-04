import allure, pytest


@pytest.fixture(scope="session")
@allure.title("Fixture to handle anonymous catalog requests")
def anonymous_catalog_requests(config, auth, webapi_client):
    class AnonymousCatalogRequests:
        def __init__(self):
            self.auth = auth
            self.webapi_client = webapi_client

        def set(self, value: bool) -> None:
            self.auth.authenticate(username=config["username"], password=config["password"])

            self.webapi_client.patch(
                f"/api/stores/{config['store_id']}",
                data=[{"op": "replace", "path": "/settings/1/value", "value": value}],
            )

            self.auth.clear_token()

    return AnonymousCatalogRequests()
