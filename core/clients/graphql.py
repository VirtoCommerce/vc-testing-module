import json
from typing import Any, Final

import requests

from core.auth.provider import AuthProvider
from core.global_settings import GlobalSettings


class GraphQLClient:
    _GRAPHQL_PATH: Final = "/graphql"

    def __init__(self, global_settings: GlobalSettings, auth: AuthProvider) -> None:
        self._global_settings = global_settings
        self._auth = auth
        self._session = requests.Session()

    def execute(self, query: str, variables: dict[str, Any] | None = None) -> dict[str, Any]:
        response = self._session.post(
            url=f"{self._global_settings.backend_base_url}{self._GRAPHQL_PATH}",
            headers=self._auth.headers,
            json={"query": query, "variables": variables or {}},
            timeout=self._global_settings.requests_timeout,
            verify=self._global_settings.verify_ssl,
        )
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            raise requests.HTTPError(
                f"{response.status_code} POST {self._GRAPHQL_PATH}: {response.text}",
                response=response,
            ) from e
        body: dict[str, Any] = response.json()
        if errors := body.get("errors"):
            formatted = json.dumps(errors, indent=2, ensure_ascii=False)
            raise ValueError(f"GraphQL errors:\n{formatted}")
        return body

    def __enter__(self) -> "GraphQLClient":
        return self

    def __exit__(self, _exc_type: object, _exc_val: object, _exc_tb: object) -> None:
        self.close()

    def close(self) -> None:
        self._session.close()
