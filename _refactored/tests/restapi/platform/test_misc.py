"""Miscellaneous platform tests — background jobs, restart."""

import allure
import pytest

from core.clients.rest import RestClient


@pytest.mark.restapi
@allure.feature("Platform / Background Jobs (REST API)")
@allure.title("Get background job status")
def test_background_job_get_status(rest_client: RestClient, backend_base_url: str):
    with allure.step("GET /api/platform/jobs"):
        jobs = rest_client.get(f"{backend_base_url}/api/platform/jobs")

    with allure.step("Verify response"):
        assert jobs is not None
