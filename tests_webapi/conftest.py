"""Shared fixtures for the WebAPI test suite.

Currently:
- `har_recorder` (autouse): captures every HTTP request/response during a test;
  on failure, attaches a HAR 1.2 file to the Allure report for debugging. Auth
  headers and cookies are redacted before serialization.
"""

import allure
import pytest

from fixtures.har_recorder import HARRecorder
from fixtures.webapi_client import WebAPISession


@pytest.fixture(autouse=True)
def har_recorder(request, webapi_client: WebAPISession):
    """Record every webapi_client HTTP call for the duration of a test.

    On failure, serialize to HAR 1.2 and attach to Allure. On pass, discard
    silently to keep the report clean.
    """
    recorder = HARRecorder()
    webapi_client.hooks["response"].append(recorder.hook)
    try:
        yield recorder
    finally:
        try:
            webapi_client.hooks["response"].remove(recorder.hook)
        except ValueError:
            pass  # hook already gone — don't fail teardown

        rep_call = getattr(request.node, "rep_call", None)
        if rep_call and rep_call.failed and recorder.has_entries():
            allure.attach(
                recorder.serialize(),
                name=f"{request.node.name}.har",
                attachment_type=allure.attachment_type.JSON,
                extension="har",
            )
