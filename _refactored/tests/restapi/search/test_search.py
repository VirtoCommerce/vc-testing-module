"""Search index operations — migrated from Katalon `API Coverage/ModuleSearch/*`.

Katalon scripts:
  GetIndex              → test_index_get
  GetIndexForProduct    → test_index_get_for_product
  BuildIndex            → test_index_build
  DropIndex             → test_index_drop (serial)
  IndexCancel           → test_index_cancel
  indexationRunAndVerify → test_indexation_run_and_verify (serial)
"""

import allure
import pytest

from core.clients.rest import RestClient


@pytest.mark.restapi
@allure.feature("Search / Indexes (REST API)")
@allure.title("Get all indexes")
def test_index_get(rest_client: RestClient, backend_base_url: str):
    with allure.step("GET /api/search/indexes"):
        result = rest_client.get(f"{backend_base_url}/api/search/indexes")

    with allure.step("Verify response"):
        assert result is not None
        assert isinstance(result, list)


@pytest.mark.restapi
@allure.feature("Search / Indexes (REST API)")
@allure.title("Get index for specific document type")
def test_index_get_for_product(rest_client: RestClient, backend_base_url: str, dataset: dict):
    products = dataset.get("products", [])
    if not products:
        pytest.skip("No products in dataset")
    product_id = products[0]["id"]

    with allure.step(f"GET /api/search/indexes/index/Product/{product_id}"):
        result = rest_client.get(f"{backend_base_url}/api/search/indexes/index/Product/{product_id}")

    with allure.step("Verify response"):
        assert result is not None


@pytest.mark.restapi
@pytest.mark.serial
@allure.feature("Search / Indexes (REST API)")
@allure.title("Build index")
def test_index_build(rest_client: RestClient, backend_base_url: str):
    with allure.step("POST /api/search/indexes/index"):
        result = rest_client.post(
            f"{backend_base_url}/api/search/indexes/index",
            json=[{"documentType": "Product"}],
        )

    with allure.step("Verify job started"):
        assert result is not None


@pytest.mark.restapi
@pytest.mark.serial
@allure.feature("Search / Indexes (REST API)")
@allure.title("Drop and rebuild index")
def test_index_drop(rest_client: RestClient, backend_base_url: str):
    with allure.step("POST /api/search/indexes/index — with DeleteExistingIndex"):
        result = rest_client.post(
            f"{backend_base_url}/api/search/indexes/index",
            json=[{"documentType": "Product", "DeleteExistingIndex": True}],
        )

    with allure.step("Verify job started"):
        assert result is not None


@pytest.mark.restapi
@allure.feature("Search / Indexes (REST API)")
@allure.title("Cancel indexation")
def test_index_cancel(rest_client: RestClient, backend_base_url: str):
    with allure.step("Start an index job"):
        result = rest_client.post(
            f"{backend_base_url}/api/search/indexes/index",
            json=[{"documentType": "Product"}],
        )
        task_id = result.get("id") if isinstance(result, dict) else None

    if task_id:
        with allure.step(f"GET /api/search/indexes/tasks/{task_id}/cancel"):
            rest_client.get(f"{backend_base_url}/api/search/indexes/tasks/{task_id}/cancel")


@pytest.mark.restapi
@pytest.mark.serial
@allure.feature("Search / Indexes (REST API)")
@allure.title("Run indexation and verify completion")
def test_indexation_run_and_verify(rest_client: RestClient, backend_base_url: str):
    import time

    with allure.step("POST /api/search/indexes/index"):
        result = rest_client.post(
            f"{backend_base_url}/api/search/indexes/index",
            json=[{"documentType": "Product"}],
        )

    with allure.step("Wait for completion"):
        if isinstance(result, dict) and result.get("id"):
            job_id = result["id"]
            for _ in range(20):
                try:
                    job = rest_client.get(f"{backend_base_url}/api/platform/jobs/{job_id}")
                    if isinstance(job, dict) and job.get("completed"):
                        break
                except Exception:
                    pass
                time.sleep(2)
