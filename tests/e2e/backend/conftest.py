import uuid
from collections.abc import Callable, Generator

import allure
import pytest
from playwright.sync_api import Page

from core.global_settings import GlobalSettings
from page_objects.backend.page_builder import (
    DetailsToolbar,
    PageBuilderShell,
    Route,
)

DEFAULT_LANGUAGE = "en-US"


@pytest.fixture
def page_builder(page: Page, global_settings: GlobalSettings) -> PageBuilderShell:
    return PageBuilderShell(page, global_settings)


@pytest.fixture
def unique_name() -> Callable[[str], str]:
    def _make(prefix: str = "qa-page") -> str:
        return f"{prefix}-{uuid.uuid4().hex[:8]}"

    return _make


@pytest.fixture
def make_page(
    page_builder: PageBuilderShell, unique_name: Callable[[str], str]
) -> Generator[Callable[..., str], None, None]:
    created: list[str] = []

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
        created.append(page_name)
        return page_name

    def _rename(old: str, new: str) -> None:
        if old in created:
            created[created.index(old)] = new

    _make.created = created  # type: ignore[attr-defined]
    _make.rename = _rename  # type: ignore[attr-defined]

    yield _make

    for page_name in reversed(created):
        try:
            with allure.step(f"Teardown: archive page '{page_name}'"):
                _archive(page_builder, page_name)
        except Exception as exc:  # noqa: BLE001
            print(f"Cleanup failed for page {page_name}: {type(exc).__name__}: {exc}")


def _archive(shell: PageBuilderShell, name: str) -> None:
    shell.open(Route.ALL)
    listing = shell.list_blade
    if not listing.has_page(name):
        return
    listing.open_page(name)
    details = shell.details_blade
    details.toolbar.button(DetailsToolbar.ARCHIVE).wait_for(state="visible")
    if details.toolbar.is_disabled(DetailsToolbar.ARCHIVE):
        return
    details.archive()
