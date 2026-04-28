"""Health check — migrated from Katalon `API Coverage/ModuleHealthCheck/*`.

Katalon scripts:
  HealthCheck(initial) → test_health_check
  HealthCheck          → test_health_check_status
  HealthCheckElastic   → test_health_check_elastic
"""

import allure
import pytest
import requests

from core.global_settings import GlobalSettings


@pytest.mark.restapi
@allure.feature("Health Check (REST API)")
@allure.title("Health check — basic")
def test_health_check(global_settings: GlobalSettings) -> None:
    with allure.step("GET /health"):
        response = requests.get(
            f"{global_settings.backend_base_url}/health",
            timeout=global_settings.requests_timeout,
            verify=global_settings.verify_ssl,
        )

    with allure.step("Verify healthy"):
        assert response.status_code == 200


@pytest.mark.restapi
@allure.feature("Health Check (REST API)")
@allure.title("Health check — verify status text")
def test_health_check_status(global_settings: GlobalSettings) -> None:
    with allure.step("GET /health"):
        response = requests.get(
            f"{global_settings.backend_base_url}/health",
            timeout=global_settings.requests_timeout,
            verify=global_settings.verify_ssl,
        )

    with allure.step("Verify status"):
        assert response.status_code == 200
        assert "healthy" in response.text.lower(), f"Expected 'healthy' in body, got: {response.text[:200]}"


@pytest.mark.restapi
@allure.feature("Health Check (REST API)")
@allure.title("Health check — Elasticsearch connectivity")
def test_health_check_elastic(rest_client, backend_base_url: str) -> None:
    with allure.step("GET /api/search/indexes"):
        result = rest_client.get(f"{backend_base_url}/api/search/indexes")

    with allure.step("Verify ES indexes available"):
        assert isinstance(result, list)
