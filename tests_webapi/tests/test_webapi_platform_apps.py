import os

import allure

from fixtures.webapi_client import WebAPISession


@allure.feature("Get platform apps info (WebAPI)")
def test_platform_apps(webapi_client: WebAPISession):
    print(f"{os.linesep}Running test to get platform apps info...", end=" ")

    platform_apps = webapi_client.get("/api/platform/apps")

    assert platform_apps is not None, "Platform apps are None"
    assert len(platform_apps) > 0, "Platform apps are empty"
