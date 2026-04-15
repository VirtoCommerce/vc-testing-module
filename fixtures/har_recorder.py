"""HAR 1.2 recorder for WebAPI tests.

Captures every HTTP request/response that flows through `WebAPISession` into a
HAR 1.2-compliant JSON document. Intended to be installed as a `requests`
response hook and serialized on test failure for attachment to Allure.

HAR 1.2 spec: http://www.softwareishard.com/blog/har-12-spec/

Usage (from a pytest fixture):

    recorder = HARRecorder()
    session.hooks["response"].append(recorder.hook)
    try:
        yield recorder
    finally:
        session.hooks["response"].remove(recorder.hook)
        if test_failed and recorder.has_entries():
            allure.attach(recorder.serialize(), name="...har",
                          attachment_type=allure.attachment_type.JSON,
                          extension="har")
"""

import json
from datetime import datetime, timezone
from typing import Any
from urllib.parse import parse_qsl, urlsplit

import requests

# Header names that may contain secrets. Case-insensitive match.
REDACTED_HEADERS = frozenset({"authorization", "api_key", "cookie", "set-cookie", "x-api-key"})
REDACTED_VALUE = "***REDACTED***"

CREATOR_NAME = "vc-testing-module"
CREATOR_VERSION = "1.0"


def _headers_to_har(headers: Any) -> list[dict[str, str]]:
    """Convert a requests headers mapping into the HAR headers list form."""
    result: list[dict[str, str]] = []
    for name, value in headers.items():
        redacted = REDACTED_VALUE if name.lower() in REDACTED_HEADERS else value
        result.append({"name": str(name), "value": str(redacted)})
    return result


def _query_to_har(url: str) -> list[dict[str, str]]:
    query = urlsplit(url).query
    return [{"name": k, "value": v} for k, v in parse_qsl(query, keep_blank_values=True)]


def _body_text(body: Any) -> str:
    """requests stores request bodies as str or bytes; normalize to str for HAR."""
    if body is None:
        return ""
    if isinstance(body, bytes):
        try:
            return body.decode("utf-8")
        except UnicodeDecodeError:
            return body.decode("utf-8", errors="replace")
    return str(body)


def _mime_type(headers: Any, default: str = "application/json") -> str:
    value = headers.get("Content-Type") or headers.get("content-type") or default
    return str(value)


class HARRecorder:
    """Collects HAR entries from a `requests.Session` response hook."""

    def __init__(self) -> None:
        self._entries: list[dict[str, Any]] = []

    # ------------------------------------------------------------------ hook

    def hook(self, response: requests.Response, *args: Any, **kwargs: Any) -> None:
        """Install as `session.hooks['response'].append(recorder.hook)`."""
        try:
            self._entries.append(self._entry_from(response))
        except Exception:
            # Never let recording failures break a test.
            pass

    # ------------------------------------------------------------------ entry build

    def _entry_from(self, response: requests.Response) -> dict[str, Any]:
        req = response.request
        elapsed_ms = int(response.elapsed.total_seconds() * 1000)
        # HAR wants ISO 8601 for the moment the request *started* — subtract elapsed.
        started_at = (
            (datetime.now(timezone.utc) - response.elapsed).isoformat(timespec="milliseconds").replace("+00:00", "Z")
        )

        req_body = _body_text(req.body)
        req_headers = _headers_to_har(req.headers)
        resp_text = response.text or ""
        resp_headers = _headers_to_har(response.headers)

        entry: dict[str, Any] = {
            "startedDateTime": started_at,
            "time": elapsed_ms,
            "request": {
                "method": req.method or "",
                "url": req.url or "",
                "httpVersion": "HTTP/1.1",
                "cookies": [],
                "headers": req_headers,
                "queryString": _query_to_har(req.url or ""),
                "headersSize": -1,
                "bodySize": len(req_body.encode("utf-8")) if req_body else 0,
            },
            "response": {
                "status": response.status_code,
                "statusText": response.reason or "",
                "httpVersion": "HTTP/1.1",
                "cookies": [],
                "headers": resp_headers,
                "content": {
                    "size": len(resp_text.encode("utf-8")),
                    "mimeType": _mime_type(response.headers),
                    "text": resp_text,
                },
                "redirectURL": response.headers.get("Location", ""),
                "headersSize": -1,
                "bodySize": len(resp_text.encode("utf-8")),
            },
            "cache": {},
            "timings": {"send": 0, "wait": elapsed_ms, "receive": 0},
        }

        if req_body:
            entry["request"]["postData"] = {
                "mimeType": _mime_type(req.headers),
                "text": req_body,
            }

        return entry

    # ------------------------------------------------------------------ accessors

    def has_entries(self) -> bool:
        return bool(self._entries)

    def serialize(self) -> str:
        return json.dumps(
            {
                "log": {
                    "version": "1.2",
                    "creator": {"name": CREATOR_NAME, "version": CREATOR_VERSION},
                    "entries": self._entries,
                }
            },
            indent=2,
        )
