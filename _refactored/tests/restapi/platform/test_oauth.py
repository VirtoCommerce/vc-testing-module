"""OAuth client CRUD — migrated from Katalon `API Coverage/ModulePlatform/OauthClient*`."""

import allure
import pytest

from restapi.operations import OAuthOperations


@pytest.mark.restapi
@allure.feature("Platform / OAuth (REST API)")
@allure.title("Create OAuth client")
def test_oauth_client_create(make_oauth_client):
    with allure.step("POST /api/platform/security/oauth/clients"):
        result = make_oauth_client()

    with allure.step("Verify client created"):
        assert result.get("_client_id")


@pytest.mark.restapi
@allure.feature("Platform / OAuth (REST API)")
@allure.title("Search OAuth clients")
def test_oauth_client_search(make_oauth_client, oauth_ops: OAuthOperations):
    client = make_oauth_client()

    with allure.step("POST /api/platform/security/oauth/clients/search"):
        search = oauth_ops.search()

    with allure.step("Verify client in results"):
        assert search.get("totalCount", 0) >= 1
        results = search.get("results", [])
        found = next((r for r in results if r.get("clientId") == client["_client_id"]), None)
        assert found is not None, f"OAuth client {client['_client_id']} not in search results"


@pytest.mark.restapi
@allure.feature("Platform / OAuth (REST API)")
@allure.title("Delete OAuth client")
def test_oauth_client_delete(make_oauth_client, oauth_ops: OAuthOperations):
    client = make_oauth_client()

    with allure.step(f"DELETE /api/platform/security/oauth/clients/{client['_client_id']}"):
        oauth_ops.delete(client["_client_id"])

    with allure.step("Verify client removed from search"):
        search = oauth_ops.search()
        results = search.get("results", [])
        found = next((r for r in results if r.get("clientId") == client["_client_id"]), None)
        assert found is None, "OAuth client still present after delete"
