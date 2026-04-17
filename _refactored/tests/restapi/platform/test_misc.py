"""Miscellaneous platform tests — background jobs, restart, modules info."""

import time

import allure
import pytest

from core.clients.rest import RestClient


@pytest.mark.restapi
@allure.feature("Platform / Background Jobs (REST API)")
@allure.title("Get background job status")
def test_background_job_get_status(rest_client: RestClient, backend_base_url: str) -> None:
    with allure.step("GET /api/platform/jobs/1"):
        jobs = rest_client.get(f"{backend_base_url}/api/platform/jobs/1")

    with allure.step("Verify response"):
        assert jobs is not None


@pytest.mark.restapi
@pytest.mark.serial
@pytest.mark.destructive
@allure.feature("Platform / Restart (REST API)")
@allure.title("Restart platform")
def test_restart_platform(rest_client: RestClient, backend_base_url: str) -> None:
    with allure.step("POST /api/platform/modules/restart"):
        rest_client.post(f"{backend_base_url}/api/platform/modules/restart", json={})

    with allure.step("Wait for platform to come back"):
        for _ in range(30):
            try:
                rest_client.get(f"{backend_base_url}/api/platform/diagnostics/systeminfo")
                break
            except Exception:
                time.sleep(5)
