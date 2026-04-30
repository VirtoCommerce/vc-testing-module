import allure
import pytest
from core.global_settings import GlobalSettings
from page_objects.pages import HomePage
from playwright.sync_api import Page, expect

_TARGET_CULTURE_NAME_FULL = "de-DE"
_TARGET_CULTURE_NAME_SHORT = "de"


@pytest.mark.e2e
@allure.feature("Storefront / Language (E2E)")
@allure.title("Switch language from the top header selector")
def test_language_change(global_settings: GlobalSettings, page: Page) -> None:
    home_page = HomePage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the home page"):
        home_page.navigate()
        expect(home_page.top_header.language_selector.root).to_be_visible()

    with allure.step(f"Select language '{_TARGET_CULTURE_NAME_FULL}'"):
        home_page.top_header.language_selector.select(
            culture_name=_TARGET_CULTURE_NAME_FULL
        )

    with allure.step(f"Verify current language is '{_TARGET_CULTURE_NAME_SHORT}'"):
        expect(home_page.top_header.language_selector.current_language_label).to_have_text(
            _TARGET_CULTURE_NAME_SHORT
        )
