import json
import os
from typing import Any, Dict, Optional, Union

import allure
import pytest
import requests
from colorama import Fore, Style

from fixtures.auth_fixture import Auth


class WebAPISession(requests.Session):
    def __init__(self, config: Dict[str, Any], auth: Auth):
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

        url = f"{self.config['backend_base_url']}{endpoint}"

        try:
            response = super().request(method, url, **kwargs)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(Fore.RED + "Error" + Style.RESET_ALL)
            print(os.linesep)
            print(f"HTTP Error: {e}")
            print(f"URL: {method} {url}")
            print(f"PAYLOAD: {kwargs.get('data')}")
            print(f"RESPONSE: {e.response.text}")
            print(os.linesep)
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
        self, endpoint: str, params: Optional[dict] = None, **kwargs
    ) -> Union[dict, str, bytes]:
        return self.send_request("GET", endpoint, params=params, **kwargs)

    def post(
        self, endpoint: str, data: Optional[dict] = None, **kwargs
    ) -> Union[dict, str, bytes]:
        return self.send_request("POST", endpoint, data=json.dumps(data), **kwargs)

    def put(
        self, endpoint: str, data: Optional[dict] = None, **kwargs
    ) -> Union[dict, str, bytes]:
        return self.send_request("PUT", endpoint, data=json.dumps(data), **kwargs)

    def delete(self, endpoint: str, **kwargs) -> Union[dict, str, bytes]:
        return self.send_request("DELETE", endpoint, **kwargs)

    def patch(
        self, endpoint: str, data: Optional[dict] = None, **kwargs
    ) -> Union[dict, str, bytes]:
        return self.send_request("PATCH", endpoint, data=json.dumps(data), **kwargs)

    def request(
        self, method: str, endpoint: str, data: Optional[dict] = None, **kwargs
    ) -> Union[dict, str, bytes]:
        return self.send_request(method, endpoint, data=json.dumps(data), **kwargs)


@pytest.fixture(scope="session")
@allure.title("Fixture to initialize Web API Client")
def webapi_client(config: Dict[str, Any], auth: Auth) -> WebAPISession:
    return WebAPISession(config, auth)
