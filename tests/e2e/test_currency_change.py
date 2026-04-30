import allure
import pytest
from core.global_settings import GlobalSettings
from page_objects.pages import HomePage
from playwright.sync_api import Page, expect

_TARGET_CURRENCY_CODE = "EUR"


@pytest.mark.e2e
@allure.feature("Storefront / Currency (E2E)")
@allure.title("Switch currency from the top header selector")
def test_currency_change(global_settings: GlobalSettings, page: Page) -> None:
    home_page = HomePage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the home page"):
        home_page.navigate()
        expect(home_page.top_header.currency_selector.root).to_be_visible()

    with allure.step(f"Select currency '{_TARGET_CURRENCY_CODE}'"):
        home_page.top_header.currency_selector.select(currency_code=_TARGET_CURRENCY_CODE)

    with allure.step(f"Verify current currency is '{_TARGET_CURRENCY_CODE}'"):
        expect(home_page.top_header.currency_selector.current_currency_label).to_have_text(
            _TARGET_CURRENCY_CODE
        )
