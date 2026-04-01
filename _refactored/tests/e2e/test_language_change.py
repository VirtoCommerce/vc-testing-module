import pytest
from playwright.sync_api import Page, expect

from core.global_settings import GlobalSettings
from page_objects.pages import HomePage

_TARGET_CULTURE_NAME_FULL = "de-DE"
_TARGET_CULTURE_NAME_SHORT = "de"


@pytest.mark.e2e
def test_language_change(global_settings: GlobalSettings, page: Page) -> None:
    home_page = HomePage(global_settings=global_settings, page=page)
    home_page.navigate()
    expect(home_page.top_header.language_selector.root).to_be_visible()

    home_page.top_header.language_selector.select(
        culture_name=_TARGET_CULTURE_NAME_FULL
    )
    expect(home_page.top_header.language_selector.current_language_label).to_have_text(
        _TARGET_CULTURE_NAME_SHORT
    )
