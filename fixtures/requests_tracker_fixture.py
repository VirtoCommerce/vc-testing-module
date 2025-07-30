from playwright.sync_api import Page
from typing import Set
from playwright.async_api import Request
import pytest


class RequestsTracker:
    def __init__(self, page: Page):
        self._page = page
        self._requests: Set = set()
        page.on("request", self._on_request)
        page.on("requestfinished", self._on_done)
        page.on("requestfailed", self._on_done)

    def _on_request(self, request: Request):
        self._requests.add(request)

    def _on_done(self, request: Request):
        self._requests.discard(request)

    def requests_count(self) -> int:
        return len(self._requests)

    def wait_for_all_requests(self, timeout: float = 5.0, interval: float = 0.1) -> None:
        import time
        start = time.time()
        while time.time() - start < timeout:
            if self.requests_count() == 0:
                return
            time.sleep(interval)

@pytest.fixture
def requests_tracker(page: Page) -> RequestsTracker:
    tracker = RequestsTracker(page)
    yield tracker
