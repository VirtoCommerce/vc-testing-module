"""Base class for REST API operation builders."""

from typing import Any

from core.clients.rest import RestClient


class RestBaseOperations:
    """Thin wrapper around RestClient that prepends the backend base URL."""

    def __init__(self, client: RestClient, backend_base_url: str) -> None:
        self._client = client
        self._backend_base_url = backend_base_url.rstrip("/")

    def _url(self, path: str) -> str:
        return f"{self._backend_base_url}{path}"
