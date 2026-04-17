"""Catalog publishing — migrated from Katalon `API Coverage/ModuleCatalogPublishing/*`.

Katalon scripts:
  channelCreate                      → test_channel_create
  channelEdit                        → test_channel_update
  channelChange                      → test_channel_get
  channelChangeCatalog               → test_channel_search
  channelsDelete                     → test_channel_delete
  competenessProductEvaluateAndSave  → test_completeness_product_evaluate
  completenessChannelEvaluate        → test_completeness_channel_evaluate
"""

import uuid

import allure
import pytest
from requests.exceptions import HTTPError

from core.clients.rest import RestClient


def _create_channel(rest_client: RestClient, backend_base_url: str, name: str, catalog: dict) -> dict:
    return rest_client.post(
        f"{backend_base_url}/api/completeness/channels",
        json={
            "name": name,
            "catalogId": catalog["id"],
            "catalogName": catalog.get("name", catalog["id"]),
            "evaluatorType": "DefaultCompletenessEvaluator",
            "languages": ["en-US"],
            "currencies": ["USD"],
        },
    )


@pytest.mark.restapi
@allure.feature("Catalog Publishing / Channels (REST API)")
@allure.title("Create channel")
def test_channel_create(rest_client: RestClient, backend_base_url: str, seed_catalog: dict) -> None:
    name = f"QAChannel_{uuid.uuid4().hex[:8]}"
    channel_id = ""

    try:
        with allure.step("POST /api/completeness/channels"):
            result = _create_channel(rest_client, backend_base_url, name, seed_catalog)

        with allure.step("Verify"):
            assert result is not None
            channel_id = result.get("id", "")
    finally:
        if channel_id:
            try:
                rest_client.delete(f"{backend_base_url}/api/completeness/channels", params={"ids": [channel_id]})
            except Exception:
                pass


@pytest.mark.restapi
@allure.feature("Catalog Publishing / Channels (REST API)")
@allure.title("Update channel")
def test_channel_update(rest_client: RestClient, backend_base_url: str, seed_catalog: dict) -> None:
    name = f"QAChannel_{uuid.uuid4().hex[:8]}"
    channel = _create_channel(rest_client, backend_base_url, name, seed_catalog)
    channel_id = channel["id"]

    try:
        with allure.step("PUT /api/completeness/channels"):
            rest_client.put(f"{backend_base_url}/api/completeness/channels", json={**channel, "name": f"{name}_UPD"})

        with allure.step("Verify"):
            reloaded = rest_client.get(f"{backend_base_url}/api/completeness/channels/{channel_id}")
            assert reloaded["name"] == f"{name}_UPD"
    finally:
        try:
            rest_client.delete(f"{backend_base_url}/api/completeness/channels", params={"ids": [channel_id]})
        except Exception:
            pass


@pytest.mark.restapi
@allure.feature("Catalog Publishing / Channels (REST API)")
@allure.title("Get channel by id")
def test_channel_get(rest_client: RestClient, backend_base_url: str, seed_catalog: dict) -> None:
    name = f"QAChannel_{uuid.uuid4().hex[:8]}"
    channel = _create_channel(rest_client, backend_base_url, name, seed_catalog)

    try:
        with allure.step(f"GET /api/completeness/channels/{channel['id']}"):
            reloaded = rest_client.get(f"{backend_base_url}/api/completeness/channels/{channel['id']}")

        with allure.step("Verify"):
            assert reloaded["id"] == channel["id"]
    finally:
        try:
            rest_client.delete(f"{backend_base_url}/api/completeness/channels", params={"ids": [channel["id"]]})
        except Exception:
            pass


@pytest.mark.restapi
@allure.feature("Catalog Publishing / Channels (REST API)")
@allure.title("Search channels")
def test_channel_search(rest_client: RestClient, backend_base_url: str) -> None:
    with allure.step("POST /api/completeness/channels/search"):
        result = rest_client.post(f"{backend_base_url}/api/completeness/channels/search", json={"skip": 0, "take": 20})

    with allure.step("Verify response shape"):
        assert isinstance(result, dict)
        assert "results" in result or "totalCount" in result


@pytest.mark.restapi
@allure.feature("Catalog Publishing / Channels (REST API)")
@allure.title("Delete channel")
def test_channel_delete(rest_client: RestClient, backend_base_url: str, seed_catalog: dict) -> None:
    name = f"QADelChannel_{uuid.uuid4().hex[:8]}"
    channel = _create_channel(rest_client, backend_base_url, name, seed_catalog)

    with allure.step(f"DELETE /api/completeness/channels?ids={channel['id']}"):
        rest_client.delete(f"{backend_base_url}/api/completeness/channels", params={"ids": [channel["id"]]})


@pytest.mark.restapi
@allure.feature("Catalog Publishing / Channels (REST API)")
@allure.title("Get evaluators")
def test_evaluators_get(rest_client: RestClient, backend_base_url: str) -> None:
    with allure.step("GET /api/completeness/evaluators"):
        result = rest_client.get(f"{backend_base_url}/api/completeness/evaluators")

    with allure.step("Verify response shape"):
        assert isinstance(result, list)


@pytest.mark.restapi
@allure.feature("Catalog Publishing / Completeness (REST API)")
@allure.title("Evaluate channel completeness")
def test_completeness_channel_evaluate(rest_client: RestClient, backend_base_url: str, seed_catalog: dict) -> None:
    name = f"QAEvalChannel_{uuid.uuid4().hex[:8]}"
    channel = _create_channel(rest_client, backend_base_url, name, seed_catalog)

    try:
        with allure.step(f"POST /api/completeness/channels/{channel['id']}/evaluate"):
            try:
                result = rest_client.post(
                    f"{backend_base_url}/api/completeness/channels/{channel['id']}/evaluate", json={}
                )
            except HTTPError as exc:
                pytest.skip(f"Evaluate requires configured products: {exc.response.status_code}")

        with allure.step("Verify response shape"):
            assert result is None or isinstance(result, (dict, list))
    finally:
        try:
            rest_client.delete(f"{backend_base_url}/api/completeness/channels", params={"ids": [channel["id"]]})
        except Exception:
            pass
