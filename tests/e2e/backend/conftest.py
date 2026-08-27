import uuid
from collections.abc import Callable
from typing import Generator

import allure
import pytest
from playwright.sync_api import Page

from core.auth import AuthProvider
from core.clients.rest import RestClient
from core.global_settings import GlobalSettings
from page_objects.backend.page_builder import PageBuilderShell, Route
from restapi.operations import PageBuilderOperations

DEFAULT_LANGUAGE = "en-US"
QA_PAGE_PREFIX = "qa-"


@pytest.fixture(scope="session")
def admin_auth(global_settings: GlobalSettings) -> Generator[AuthProvider, None, None]:
    """Bearer-token admin auth for the REST calls that support admin-UI tests.

    Distinct from `admin_ui_session`, which holds the identity *cookie* the
    browser context needs; RestClient authenticates with an OAuth header.
    """
    provider = AuthProvider(global_settings.backend_base_url)
    provider.sign_in(global_settings.admin_username, global_settings.admin_password)
    yield provider
    provider.sign_out()


@pytest.fixture
def rest_client(global_settings: GlobalSettings, admin_auth: AuthProvider) -> Generator[RestClient, None, None]:
    with RestClient(global_settings=global_settings, auth=admin_auth) as client:
        yield client


@pytest.fixture
def page_builder_api(rest_client: RestClient, global_settings: GlobalSettings) -> PageBuilderOperations:
    return PageBuilderOperations(rest_client, global_settings.backend_base_url)


@pytest.fixture(autouse=True)
def purge_qa_pages(
    page_builder_api: PageBuilderOperations, global_settings: GlobalSettings
) -> Generator[None, None, None]:
    """Hard-delete every `qa-` page the test leaves behind.

    The shell's only destructive action is Archive, which keeps the row, so
    without an API teardown each run grows the store and drifts the counters,
    status filters and search-window behaviour the tests assert on.

    Diffing group ids around the test — rather than tracking what `make_page`
    returns — also catches pages created directly through the blade and clones.
    """

    def qa_group_ids() -> set[str]:
        pages = page_builder_api.search(store_id=global_settings.store_id, keyword=QA_PAGE_PREFIX)
        return {p.id for p in pages if p.name.startswith(QA_PAGE_PREFIX)}

    before = qa_group_ids()
    yield
    leaked = qa_group_ids() - before
    if not leaked:
        return
    with allure.step(f"Teardown: delete {len(leaked)} page(s) created by this test"):
        for group_id in leaked:
            page_builder_api.delete(group_id)


@pytest.fixture
def page_builder(page: Page, global_settings: GlobalSettings) -> PageBuilderShell:
    return PageBuilderShell(page, global_settings)


@pytest.fixture
def unique_name() -> Callable[[str], str]:
    def _make(prefix: str = "qa-page") -> str:
        return f"{prefix}-{uuid.uuid4().hex[:8]}"

    return _make


@pytest.fixture
def make_page(page_builder: PageBuilderShell, unique_name: Callable[[str], str]) -> Callable[..., str]:
    def _make(
        name: str | None = None,
        permalink: str | None = None,
        language: str | None = DEFAULT_LANGUAGE,
    ) -> str:
        page_name = name or unique_name("qa-page")
        with allure.step(f"Create draft page '{page_name}'"):
            page_builder.open(Route.DRAFT)
            details = page_builder.add_page()
            details.fill(name=page_name, permalink=permalink or f"/{page_name}")
            if language:
                details.language.select(language)
            details.save()
            page_builder.notifications.wait_for_success()
        return page_name

    return _make
