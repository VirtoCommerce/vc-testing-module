import pytest
from core.global_settings import GlobalSettings
from page_objects.pages import CategoryPage
from playwright.sync_api import Page, expect

_CATEGORY_PATH = "smartphones"
_PRODUCT_SKU = "smartphone-samsung-galaxy-a57-5g"


@pytest.mark.e2e
@pytest.mark.quantity_control("stepper")
def test_category_product_update_cart_stepper(global_settings: GlobalSettings, page: Page) -> None:
    category_page = CategoryPage(global_settings=global_settings, page=page, path=_CATEGORY_PATH)
    category_page.navigate()

    product_card = category_page.scroll_to_product(sku=_PRODUCT_SKU)
    expect(product_card.root).to_be_visible()
    expect(product_card.quantity_stepper.root).to_be_visible()

    product_card.quantity_stepper.increment_button.click()
    expect(category_page.cart_quantity_label).to_have_text("1")
    product_card.quantity_stepper.increment_button.click()
    expect(category_page.cart_quantity_label).to_have_text("2")
    product_card.quantity_stepper.decrement_button.click()
    expect(category_page.cart_quantity_label).to_have_text("1")


@pytest.mark.e2e
@pytest.mark.quantity_control("button")
def test_category_product_update_cart_button(global_settings: GlobalSettings, page: Page) -> None:
    category_page = CategoryPage(global_settings=global_settings, page=page, path=_CATEGORY_PATH)
    category_page.navigate()

    product_card = category_page.scroll_to_product(sku=_PRODUCT_SKU)
    expect(product_card.root).to_be_visible()
    expect(product_card.add_to_cart_button.root).to_be_visible()

    product_card.add_to_cart_button.quantity_input.fill("1")
    product_card.add_to_cart_button.text_button.click()
    expect(category_page.cart_quantity_label).to_have_text("1")

    product_card.add_to_cart_button.quantity_input.fill("2")
    product_card.add_to_cart_button.text_button.click()
    expect(category_page.cart_quantity_label).to_have_text("2")
