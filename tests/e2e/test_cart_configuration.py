import allure
import pytest
from playwright.sync_api import Page, expect

from core.global_settings import GlobalSettings
from page_objects.pages import CartPage, ProductPage

_PRODUCT_ID = "laptop-acer-predator-helios-neo-16-ai"
_PATH = "laptops/acer-predator-helios-neo-16-ai"
_CONFIGURED_SKU = f"Configuration-{_PRODUCT_ID}"
_MEMORY_SECTION_NAME = "Memory"
_MEMORY_OPTION_A = "Samsung DDR5-4800 8GB"
_MEMORY_OPTION_B = "Crucial DDR5-4800 16GB"


def _add_configuration(product_page: ProductPage, memory_option: str) -> None:
    """Configure the product with a memory option and add it to the cart."""
    product_page.navigate()
    expect(product_page.product_configuration_area.root).to_be_visible()
    product_page.product_configuration_area.select_option(
        section_name=_MEMORY_SECTION_NAME, option_name=memory_option
    )
    product_page.add_to_cart()


@pytest.mark.e2e
@pytest.mark.delete_cart_after
@allure.feature("Cart / Configurable product (E2E)")
@allure.title("Save two different configurations of the same product as separate cart line items")
def test_cart_configuration_save_multiple(
    global_settings: GlobalSettings, page: Page
) -> None:
    product_page = ProductPage(global_settings=global_settings, page=page, path=_PATH)
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step(f"Configure with '{_MEMORY_OPTION_A}' and add to cart"):
        _add_configuration(product_page, _MEMORY_OPTION_A)
        expect(product_page.cart_quantity_label).to_have_text("1")

    with allure.step(f"Create a new configuration with '{_MEMORY_OPTION_B}' and add to cart"):
        _add_configuration(product_page, _MEMORY_OPTION_B)
        expect(product_page.cart_quantity_label).to_have_text("2")

    with allure.step("Open the cart and verify both configurations exist as separate line items"):
        cart_page.navigate()
        configured_items = cart_page.configured_line_items(_PRODUCT_ID)
        expect(configured_items).to_have_count(2)

    with allure.step("Expand each components list and verify the distinct memory options"):
        configured_items.nth(0).locator("button.configuration-items__toggle").click()
        configured_items.nth(1).locator("button.configuration-items__toggle").click()
        expect(
            cart_page.find_configured_line_item(_PRODUCT_ID, _MEMORY_OPTION_A).root
        ).to_be_visible()
        expect(
            cart_page.find_configured_line_item(_PRODUCT_ID, _MEMORY_OPTION_B).root
        ).to_be_visible()


@pytest.mark.e2e
@pytest.mark.delete_cart_after
@allure.feature("Cart / Configurable product (E2E)")
@allure.title("Remove a configured product line item from the cart")
def test_cart_configuration_remove(
    global_settings: GlobalSettings, page: Page
) -> None:
    product_page = ProductPage(global_settings=global_settings, page=page, path=_PATH)
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Configure a product and add it to the cart"):
        _add_configuration(product_page, _MEMORY_OPTION_A)
        expect(product_page.cart_quantity_label).to_have_text("1")

    with allure.step("Open the cart and locate the configured line item"):
        cart_page.navigate()
        line_item = cart_page.find_line_item(sku=_CONFIGURED_SKU)
        expect(line_item.root).to_be_visible()
        expect(line_item.remove_button).to_be_visible()

    with allure.step("Remove the configured line item and verify the cart is empty"):
        line_item.remove_button.click()
        expect(cart_page.line_items).to_have_count(0)


@pytest.mark.e2e
@pytest.mark.delete_cart_after
@allure.feature("Cart / Configurable product (E2E)")
@allure.title("Edit a configured product from the cart and see the updated configuration")
def test_cart_configuration_change_in_cart(
    global_settings: GlobalSettings, page: Page
) -> None:
    product_page = ProductPage(global_settings=global_settings, page=page, path=_PATH)
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step(f"Configure with '{_MEMORY_OPTION_A}' and add to cart"):
        _add_configuration(product_page, _MEMORY_OPTION_A)
        expect(product_page.cart_quantity_label).to_have_text("1")

    with allure.step("Open the cart and start editing the configuration"):
        cart_page.navigate()
        line_item = cart_page.find_line_item(sku=_CONFIGURED_SKU)
        expect(line_item.root).to_be_visible()
        expect(line_item.root).to_contain_text(_MEMORY_OPTION_A)
        line_item.expand_components_list()
        expect(line_item.edit_configuration_link).to_be_visible()
        line_item.edit_configuration_link.click()

    with allure.step(f"Change the memory option to '{_MEMORY_OPTION_B}' and update the cart"):
        expect(product_page.product_configuration_area.root).to_be_visible()
        product_page.product_configuration_area.select_option(
            section_name=_MEMORY_SECTION_NAME, option_name=_MEMORY_OPTION_B
        )
        expect(product_page.update_cart_button).to_be_enabled()
        product_page.update_cart()

    with allure.step("Verify the cart still has one configured item with the new configuration"):
        cart_page.navigate()
        expect(cart_page.configured_line_items(_PRODUCT_ID)).to_have_count(1)
        line_item = cart_page.find_line_item(sku=_CONFIGURED_SKU)
        line_item.expand_components_list()
        expect(line_item.root).to_contain_text(_MEMORY_OPTION_B)
        expect(line_item.root).not_to_contain_text(_MEMORY_OPTION_A)
