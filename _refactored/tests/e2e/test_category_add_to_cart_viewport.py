import pytest
from playwright.sync_api import Page, expect

from core.global_settings import GlobalSettings
from page_objects.pages import CategoryPage

_CATEGORY_PATH = "laptops"
_PRODUCT_SKU = "product-acme-laptop-asus-zenbook-a14-ux3407"


@pytest.mark.e2e
@pytest.mark.quantity_control("stepper")
def test_category_add_to_cart_viewport_stepper(
    global_settings: GlobalSettings, page: Page
) -> None:
    category_page = CategoryPage(
        global_settings=global_settings, page=page, path=_CATEGORY_PATH
    )
    category_page.navigate()

    product_card = category_page.scroll_to_product(sku=_PRODUCT_SKU)
    expect(product_card.root).to_be_visible()
    expect(product_card.quantity_stepper.root).to_be_visible()

    page.set_viewport_size({"width": 800, "height": 600})

    expect(product_card.quantity_stepper.root).to_be_visible()


@pytest.mark.e2e
@pytest.mark.quantity_control("button")
def test_category_add_to_cart_viewport_button(
    global_settings: GlobalSettings, page: Page
) -> None:
    category_page = CategoryPage(
        global_settings=global_settings, page=page, path=_CATEGORY_PATH
    )
    category_page.navigate()

    product_card = category_page.scroll_to_product(sku=_PRODUCT_SKU)
    expect(product_card.root).to_be_visible()
    expect(product_card.add_to_cart_button.root).to_be_visible()
    expect(product_card.add_to_cart_button.text_button).to_be_visible()

    page.set_viewport_size({"width": 800, "height": 600})

    expect(product_card.add_to_cart_button.icon_button).to_be_visible()
