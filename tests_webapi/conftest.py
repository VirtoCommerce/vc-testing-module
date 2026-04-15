"""Shared fixtures for the WebAPI test suite.

Currently:
- `har_recorder` (autouse): captures every HTTP request/response during a test
  and attaches a HAR 1.2 file to the Allure report for every test (passed or
  failed). Auth headers and cookies are redacted before serialization.
"""

import allure
import pytest

from fixtures.har_recorder import HARRecorder
from fixtures.webapi_client import WebAPISession


@pytest.fixture(autouse=True)
def har_recorder(request, webapi_client: WebAPISession):
    """Record every webapi_client HTTP call for the duration of a test and
    attach the HAR 1.2 file to Allure.

    Attaches on both pass and fail so the Allure report has a full network
    trace for every test — useful for auditing happy-path traffic and for
    debugging tests that pass but behave unexpectedly.
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

        if recorder.has_entries():
            allure.attach(
                recorder.serialize(),
                name=f"{request.node.name}.har",
                attachment_type=allure.attachment_type.JSON,
                extension="har",
            )
