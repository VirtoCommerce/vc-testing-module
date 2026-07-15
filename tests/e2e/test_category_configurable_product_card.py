import re

import allure
import pytest
from playwright.sync_api import Page, expect

from core.global_settings import GlobalSettings
from page_objects.pages import CategoryPage, ProductPage

_CATEGORY_PATH = "laptops"
_CONFIGURABLE_PRODUCT_CODE = "laptop-acer-predator-helios-neo-16-ai"
_CONFIGURABLE_PRODUCT_SEMANTIC_URL = "acer-predator-helios-neo-16-ai"


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
        expect(product_card.configurations_button).to_be_visible()
        product_card.configurations_button.click()

    with allure.step(
        "Verify the configurable product page opened with its configuration area"
    ):
        expect(page).to_have_url(
            re.compile(rf".*/{re.escape(_CONFIGURABLE_PRODUCT_SEMANTIC_URL)}(\?.*)?$")
        )
        product_page = ProductPage(
            global_settings=global_settings,
            page=page,
            path=f"{_CATEGORY_PATH}/{_CONFIGURABLE_PRODUCT_SEMANTIC_URL}",
        )
        expect(product_page.product_configuration_area.root).to_be_visible()
