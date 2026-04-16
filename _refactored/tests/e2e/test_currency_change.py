import pytest
from playwright.sync_api import Page, expect

from core.global_settings import GlobalSettings
from page_objects.pages import HomePage

_TARGET_CURRENCY_CODE = "EUR"


@pytest.mark.e2e
def test_currency_change(global_settings: GlobalSettings, page: Page) -> None:
    home_page = HomePage(global_settings=global_settings, page=page)
    home_page.navigate()
    expect(home_page.top_header.currency_selector.root).to_be_visible()

    home_page.top_header.currency_selector.select(currency_code=_TARGET_CURRENCY_CODE)
    expect(home_page.top_header.currency_selector.current_currency_label).to_have_text(
        _TARGET_CURRENCY_CODE
    )
