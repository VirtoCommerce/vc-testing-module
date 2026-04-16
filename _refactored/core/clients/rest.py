from typing import Any, Literal

import requests

from core.auth.provider import AuthProvider
from core.global_settings import GlobalSettings

_HttpMethod = Literal["GET", "POST", "PUT", "DELETE", "PATCH"]
_ResponseBody = dict[str, Any] | list[Any]


class RestClient:
    def __init__(self, global_settings: GlobalSettings, auth: AuthProvider) -> None:
        self._global_settings = global_settings
        self._auth = auth
        self._session = requests.Session()

    def __enter__(self) -> "RestClient":
        return self

    def __exit__(self, _exc_type: object, _exc_val: object, _exc_tb: object) -> None:
        self.close()

    def _request(
        self,
        method: _HttpMethod,
        url: str,
        json: Any | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> requests.Response:
        merged_headers = {**self._auth.headers, **(headers or {})}
        response = self._session.request(
            method=method,
            url=url,
            json=json,
            params=params,
            headers=merged_headers,
            timeout=self._global_settings.requests_timeout,
            verify=self._global_settings.verify_ssl,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise requests.HTTPError(
                f"{response.status_code} {method} {url}: {response.text}",
                response=response,
            ) from exc
        return response

    def _parse_response(self, response: requests.Response) -> _ResponseBody | None:
        if not response.content:
            return None
        content_type = response.headers.get("Content-Type", "")
        if "application/json" not in content_type:
            raise NotImplementedError(
                f"Unsupported Content-Type: {content_type!r}. Only application/json is currently supported."
            )
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError as exc:
            raise ValueError(
                f"Response has Content-Type: application/json but body is not valid JSON: {exc}"
            ) from exc

    def get(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> _ResponseBody | None:
        response = self._request(method="GET", url=url, params=params, headers=headers)
        return self._parse_response(response=response)

    def post(
        self,
        url: str,
        json: Any,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> _ResponseBody | None:
        response = self._request(
            method="POST", url=url, json=json, params=params, headers=headers
        )
        return self._parse_response(response=response)

    def put(
        self,
        url: str,
        json: Any,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> _ResponseBody | None:
        response = self._request(
            method="PUT", url=url, json=json, params=params, headers=headers
        )
        return self._parse_response(response=response)

    def patch(
        self,
        url: str,
        json: Any,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> _ResponseBody | None:
        response = self._request(
            method="PATCH", url=url, json=json, params=params, headers=headers
        )
        return self._parse_response(response=response)

    def delete(
        self,
        url: str,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> _ResponseBody | None:
        response = self._request(
            method="DELETE", url=url, params=params, headers=headers
        )
        return self._parse_response(response=response)

    def close(self) -> None:
        self._session.close()
