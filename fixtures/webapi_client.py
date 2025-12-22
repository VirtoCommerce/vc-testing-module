import json
from textwrap import dedent
from typing import Any, Union

import allure
import pytest
import requests

from fixtures.auth import Auth
from fixtures.config import Config


class WebAPISession(requests.Session):
    def __init__(self, config: Config, auth: Auth):
        super().__init__()
        self.config = config
        self.auth_handler = auth
        self.headers.update({"Content-Type": "application/json"})

    def update_auth_headers(self) -> None:
        auth_headers = self.auth_handler.get_auth_headers()

        if auth_headers:
            self.headers.update(auth_headers)
        else:
            self.headers.pop("Authorization", None)

    def send_request(
        self, method: str, endpoint: str, **kwargs
    ) -> Union[dict, str, bytes]:
        self.update_auth_headers()

        url = f"{self.config['BACKEND_BASE_URL']}{endpoint}"

        try:
            response = super().request(method, url, **kwargs)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            message = dedent(
                f"""
                    HTTP Error: {e}
                    URL: {method} {url}
                    PAYLOAD: {kwargs.get('data')}
                    RESPONSE: {e.response.text}
                """
            )
            e.message = message
            raise e

        content_type = response.headers.get("Content-Type", "")

        if "application/json" in content_type:
            return response.json()
        elif "text/" in content_type:
            return response.text
        elif "application/octet-stream" in content_type:
            return response.content
        else:
            return response.text

    def get(
        self, endpoint: str, params: dict[str, Any] | None = None, **kwargs
    ) -> Union[dict, str, bytes]:
        return self.send_request("GET", endpoint, params=params, **kwargs)

    def post(
        self, endpoint: str, data: dict[str, Any] | None = None, **kwargs
    ) -> Union[dict, str, bytes]:
        return self.send_request("POST", endpoint, data=json.dumps(data), **kwargs)

    def put(
        self, endpoint: str, data: dict[str, Any] | None = None, **kwargs
    ) -> Union[dict, str, bytes]:
        return self.send_request("PUT", endpoint, data=json.dumps(data), **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Union[dict, str, bytes]:
        return self.send_request("DELETE", endpoint, **kwargs)

    def patch(
        self, endpoint: str, data: dict[str, Any] | None = None, **kwargs
    ) -> Union[dict, str, bytes]:
        return self.send_request("PATCH", endpoint, data=json.dumps(data), **kwargs)

    def request(
        self, method: str, endpoint: str, data: dict[str, Any] | None = None, **kwargs
    ) -> Union[dict, str, bytes]:
        return self.send_request(method, endpoint, data=json.dumps(data), **kwargs)


@pytest.fixture(scope="session")
@allure.title("Fixture to initialize Web API Client")
def webapi_client(config: Config, auth: Auth) -> WebAPISession:
    return WebAPISession(config, auth)
