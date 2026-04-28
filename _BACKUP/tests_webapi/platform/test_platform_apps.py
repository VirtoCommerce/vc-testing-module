import allure
import pytest

from fixtures.webapi_client import WebAPISession


@pytest.mark.webapi
@allure.feature("Platform / Apps (WebAPI)")
@allure.title("List installed platform apps")
def test_platform_apps(webapi_client: WebAPISession):
    with allure.step("GET /api/platform/apps"):
        platform_apps = webapi_client.get("/api/platform/apps")

    assert platform_apps is not None, "Platform apps are None"
    assert len(platform_apps) > 0, "Platform apps are empty"
