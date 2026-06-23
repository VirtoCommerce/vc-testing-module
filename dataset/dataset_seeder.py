import time

import requests

from core.clients.rest import RestClient
from core.logger import Logger

from dataset.request_builder import PreparedRequest


class EndpointNotAvailable(Exception):
    """An optional entity's endpoint is absent on the target backend (HTTP 404).

    Signals to the caller that the entity was skipped — not failed — because the installed
    module version predates this endpoint (e.g. running edge-aware tests against stable).
    """


def _is_not_found(exc: Exception) -> bool:
    response = getattr(exc, "response", None)
    return isinstance(exc, requests.HTTPError) and response is not None and response.status_code == 404


def fetch_installed_modules(rest_client: RestClient, base_url: str, logger: Logger) -> set[str]:
    """Return ids of installed modules.

    Returns an empty set if the response shape is unexpected — the caller treats an empty set
    as "module info unavailable" (i.e. no module-based filtering).
    """
    response = rest_client.get(url=f"{base_url}/api/platform/modules")
    if not isinstance(response, list):
        logger.warning("Unexpected modules response format")
        return set()
    module_ids = {m["id"] for m in response if "id" in m and m.get("isInstalled") is True}
    logger.info(f"Fetched {len(module_ids)} installed module(s)")
    return module_ids


class DatasetSeeder:
    def __init__(self, rest_client: RestClient, logger: Logger) -> None:
        self._rest_client = rest_client
        self._logger = logger

    def seed(self, requests: list[PreparedRequest], optional: bool = False) -> None:
        """Send all requests in order. Aborts on the first failure (raises the underlying error).

        When `optional` is True, a 404 raises `EndpointNotAvailable` instead of a generic error,
        so the caller can treat the entity as skipped rather than failed.
        """
        for request in requests:
            self._send(request, optional=optional)

    def _send(self, request: PreparedRequest, optional: bool = False) -> None:
        prefix = f"Seeding \\[{request.label}]"
        start = time.perf_counter()
        try:
            self._dispatch(request)
        except Exception as e:
            elapsed = time.perf_counter() - start
            if optional and _is_not_found(e):
                self._logger.warning(
                    f"{prefix} {request.method} {request.url} [yellow]SKIPPED[/yellow] "
                    f"\\[{elapsed:.2f}s]: endpoint not available on this backend (HTTP 404)"
                )
                raise EndpointNotAvailable(str(e)) from e
            self._logger.error(
                f"{prefix} {request.method} {request.url} [red]FAILED[/red] "
                f"\\[{elapsed:.2f}s]: {type(e).__name__}: {e}"
            )
            raise
        elapsed = time.perf_counter() - start
        self._logger.info(f"{prefix} {request.method} {request.url} [green]DONE[/green] \\[{elapsed:.2f}s]")

    def _dispatch(self, request: PreparedRequest) -> None:
        match request.method:
            case "POST":
                self._rest_client.post(url=request.url, json=request.payload)
            case "PUT":
                self._rest_client.put(url=request.url, json=request.payload)
            case "PATCH":
                self._rest_client.patch(url=request.url, json=request.payload)
            case "DELETE":
                self._rest_client.delete(url=request.url)
            case "GET":
                self._rest_client.get(url=request.url)
            case _:
                raise ValueError(f"Unsupported HTTP method: {request.method}")
