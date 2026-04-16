import pytest
from playwright.sync_api import Page, expect

from core.global_settings import GlobalSettings
from page_objects.pages.category import CategoryPage

_CATEGORY_PATH = "laptops"
_PRODUCT_SKU = "product-acme-laptop-lenovo-thinkpad-x1-carbon-gen-13-aura"
_VARIATION_1_SKU = "product-acme-laptop-lenovo-thinkpad-x1-carbon-gen-13-aura-var1"
_VARIATION_2_SKU = "product-acme-laptop-lenovo-thinkpad-x1-carbon-gen-13-aura-var2"


@pytest.mark.e2e
@pytest.mark.quantity_control("stepper")
@pytest.mark.delete_cart_after
def test_category_variation_update_cart_stepper(
    global_settings: GlobalSettings, page: Page
) -> None:
    category_page = CategoryPage(
        global_settings=global_settings, page=page, path=_CATEGORY_PATH
    )
    category_page.navigate()

    category_page.view_switcher.list_view_tab.click()
    product_card = category_page.scroll_to_product(sku=_PRODUCT_SKU)
    expect(product_card.root).to_be_visible()
    expect(product_card.variations_button).to_be_visible()

    product_card.variations_button.click()

    variation_1 = product_card.find_variation_item(sku=_VARIATION_1_SKU)
    variation_2 = product_card.find_variation_item(sku=_VARIATION_2_SKU)

    variation_1.quantity_stepper.increment_button.click()
    expect(category_page.cart_quantity_label).to_have_text("1")
    variation_1.quantity_stepper.increment_button.click()
    expect(category_page.cart_quantity_label).to_have_text("2")

    variation_2.quantity_stepper.increment_button.click()
    expect(category_page.cart_quantity_label).to_have_text("3")
    variation_2.quantity_stepper.increment_button.click()
    expect(category_page.cart_quantity_label).to_have_text("4")

    variation_1.quantity_stepper.decrement_button.click()
    expect(category_page.cart_quantity_label).to_have_text("3")
    variation_2.quantity_stepper.decrement_button.click()
    expect(category_page.cart_quantity_label).to_have_text("2")


@pytest.mark.e2e
@pytest.mark.quantity_control("button")
@pytest.mark.delete_cart_after
def test_category_variation_update_cart_button(
    global_settings: GlobalSettings, page: Page
) -> None:
    category_page = CategoryPage(
        global_settings=global_settings, page=page, path=_CATEGORY_PATH
    )
    category_page.navigate()

    category_page.view_switcher.list_view_tab.click()
    product_card = category_page.scroll_to_product(sku=_PRODUCT_SKU)
    expect(product_card.root).to_be_visible()
    expect(product_card.variations_button).to_be_visible()

    product_card.variations_button.click()

    variation_1 = product_card.find_variation_item(sku=_VARIATION_1_SKU)
    variation_2 = product_card.find_variation_item(sku=_VARIATION_2_SKU)

    variation_1.add_to_cart_button.quantity_input.fill("1")
    variation_1.add_to_cart_button.icon_button.click()
    expect(category_page.cart_quantity_label).to_have_text("1")
    variation_1.add_to_cart_button.quantity_input.fill("2")
    variation_1.add_to_cart_button.icon_button.click()
    expect(category_page.cart_quantity_label).to_have_text("2")

    variation_2.add_to_cart_button.quantity_input.fill("1")
    variation_2.add_to_cart_button.icon_button.click()
    expect(category_page.cart_quantity_label).to_have_text("3")
    variation_2.add_to_cart_button.quantity_input.fill("2")
    variation_2.add_to_cart_button.icon_button.click()
    expect(category_page.cart_quantity_label).to_have_text("4")
