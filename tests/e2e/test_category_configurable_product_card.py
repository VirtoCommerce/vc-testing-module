import re

import allure
import pytest
from playwright.sync_api import Page, expect
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from core.global_settings import GlobalSettings
from page_objects.pages import CategoryPage, ProductPage

_CATEGORY_PATH = "laptops"
_CONFIGURABLE_PRODUCT_CODE = "laptop-acer-predator-helios-neo-16-ai"
_CONFIGURABLE_PRODUCT_SEMANTIC_URL = "acer-predator-helios-neo-16-ai"
_PRODUCT_URL_PATTERN = re.compile(
    rf".*/{re.escape(_CONFIGURABLE_PRODUCT_SEMANTIC_URL)}(\?.*)?$"
)


@pytest.mark.e2e
@allure.feature("Category / Configurable product (E2E)")
@allure.title("Configurable product card exposes a customize action")
def test_category_configurable_product_card(
    global_settings: GlobalSettings, page: Page
) -> None:
    category_page = CategoryPage(
        global_settings=global_settings, page=page, path=_CATEGORY_PATH
    )

    with allure.step(
        f"Navigate to category '{_CATEGORY_PATH}' and find a product card "
        f"'{_CONFIGURABLE_PRODUCT_CODE}'"
    ):
        category_page.navigate()
        product_card = category_page.scroll_to_product(sku=_CONFIGURABLE_PRODUCT_CODE)
        expect(product_card.root).to_be_visible()

    with allure.step("Verify the card offers a customize action for the configurable product"):
        expect(product_card.configurations_button).to_be_visible()


@pytest.mark.e2e
@allure.feature("Category / Configurable product (E2E)")
@allure.title("Customize action navigates to the configurable product page")
def test_category_configurable_product_navigation(
    global_settings: GlobalSettings, page: Page
) -> None:
    category_page = CategoryPage(
        global_settings=global_settings, page=page, path=_CATEGORY_PATH
    )

    with allure.step(f"Navigate to category '{_CATEGORY_PATH}'"):
        category_page.navigate()

    with allure.step(
        f"Open the customize action on card '{_CONFIGURABLE_PRODUCT_CODE}'"
    ):
        product_card = category_page.scroll_to_product(sku=_CONFIGURABLE_PRODUCT_CODE)
        customize_action = product_card.configurations_button
        expect(customize_action).to_be_visible()
        # The customize action is a router link. Until the SPA finishes
        # hydrating, the first click can be swallowed (the anchor's default
        # navigation is prevented before the client-side router is wired up),
        # so retry the click until the URL actually changes.
        for _ in range(3):
            if _PRODUCT_URL_PATTERN.search(page.url):
                break
            customize_action.click()
            try:
                page.wait_for_url(_PRODUCT_URL_PATTERN, timeout=7000)
                break
            except PlaywrightTimeoutError:
                continue

    with allure.step(
        "Verify the configurable product page opened with its configuration area"
    ):
        expect(page).to_have_url(_PRODUCT_URL_PATTERN)
        product_page = ProductPage(
            global_settings=global_settings,
            page=page,
            path=f"{_CATEGORY_PATH}/{_CONFIGURABLE_PRODUCT_SEMANTIC_URL}",
        )
        expect(product_page.product_configuration_area.root).to_be_visible()
