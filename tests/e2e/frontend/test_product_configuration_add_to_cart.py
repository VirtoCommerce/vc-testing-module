import re

import allure
import pytest
from playwright.sync_api import Page, expect

from core.global_settings import GlobalSettings
from page_objects.frontend.pages import CartPage, ProductPage

_PRODUCT_ID = "laptop-acer-predator-helios-neo-16-ai"
_PATH = f"laptops/{_PRODUCT_ID.replace('laptop-', '')}"
_CONFIGURED_SKU = f"Configuration-{_PRODUCT_ID}"
_MEMORY_SECTION_NAME = "Memory"
_STORAGE_SECTION_NAME = "Storage"
_MEMORY_OPTION_NAME = "Samsung DDR5-4800 8GB"
_STORAGE_OPTION_NAME = "Kingston FURY Renegade G5 PCIe 5.0 NVMe M.2 SSD 1024GB"


@pytest.mark.e2e
@pytest.mark.delete_cart_after
@allure.feature("Product / Configuration (E2E)")
@allure.title("Configure a configurable product and add it to the cart")
def test_product_configuration_add_to_cart(global_settings: GlobalSettings, page: Page) -> None:
    product_page = ProductPage(global_settings=global_settings, page=page, path=_PATH)

    with allure.step("Open the configurable product page"):
        product_page.navigate()
        expect(product_page.product_configuration_area.root).to_be_visible()

    with allure.step("Verify the required configuration sections are present"):
        memory_section = product_page.product_configuration_area.find_section_by_name(name=_MEMORY_SECTION_NAME)
        expect(memory_section.root).to_be_visible()
        assert memory_section.is_required

        storage_section = product_page.product_configuration_area.find_section_by_name(name=_STORAGE_SECTION_NAME)
        expect(storage_section.root).to_be_visible()
        assert storage_section.is_required

    with allure.step(f"Select memory option '{_MEMORY_OPTION_NAME}'"):
        memory_section.select_option(name=_MEMORY_OPTION_NAME)
        expect(memory_section.root).to_contain_text(_MEMORY_OPTION_NAME)
        assert memory_section.selected_option_name == _MEMORY_OPTION_NAME

    with allure.step(f"Select storage option '{_STORAGE_OPTION_NAME}'"):
        storage_section.select_option(name=_STORAGE_OPTION_NAME)
        expect(storage_section.root).to_contain_text(_STORAGE_OPTION_NAME)
        assert storage_section.selected_option_name == _STORAGE_OPTION_NAME

    with allure.step("Verify the configuration total price is shown"):
        # Assert a real monetary total is rendered rather than comparing against
        # the default: the default-selected options (and therefore the default
        # total) are data-dependent across DB providers, so a before/after
        # comparison is not reliable when the chosen options match the defaults.
        expect(product_page.total_price).to_be_visible()
        expect(product_page.total_price).to_have_text(re.compile(r"\d"))

    with allure.step("Add the configured product to the cart"):
        expect(product_page.add_to_cart_button).to_be_enabled()
        product_page.add_to_cart()
        expect(product_page.cart_quantity_label).to_have_text("1")

    with allure.step("Open the cart and verify the configured line item is present"):
        cart_page = CartPage(global_settings=global_settings, page=page)
        cart_page.navigate()
        configured_item = cart_page.find_line_item(sku=_CONFIGURED_SKU)
        expect(configured_item.root).to_be_visible()
        expect(cart_page.line_items).to_have_count(1)
