import pytest
from playwright.sync_api import Page, expect

from core.global_settings import GlobalSettings
from page_objects.pages import CartPage

_PRODUCT_ID = "product-acme-laptop-asus-zenbook-a14-ux3407"
_ORIGINAL_QUANTITY = 3
_UPDATED_QUANTITY = 4


@pytest.mark.e2e
@pytest.mark.with_user("acme_store_employee_1@acme.com")
@pytest.mark.with_cart([(_PRODUCT_ID, _ORIGINAL_QUANTITY)])
@pytest.mark.quantity_control("stepper")
def test_cart_item_update_stepper(global_settings: GlobalSettings, page: Page) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()

    line_item = cart_page.find_line_item(sku=_PRODUCT_ID)
    expect(line_item.root).to_be_visible()
    expect(line_item.quantity_stepper.root).to_be_visible()
    expect(line_item.quantity_stepper.quantity_input).to_have_value(
        str(_ORIGINAL_QUANTITY)
    )

    line_item.quantity_stepper.increment_button.click()
    expect(cart_page.cart_quantity_label).to_have_text(str(_UPDATED_QUANTITY))


@pytest.mark.e2e
@pytest.mark.with_user("acme_store_employee_1@acme.com")
@pytest.mark.with_cart([(_PRODUCT_ID, _ORIGINAL_QUANTITY)])
@pytest.mark.quantity_control("button")
def test_cart_item_update_button(global_settings: GlobalSettings, page: Page) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()

    line_item = cart_page.find_line_item(sku=_PRODUCT_ID)
    expect(line_item.root).to_be_visible()
    expect(line_item.add_to_cart_button.root).to_be_visible()
    expect(line_item.add_to_cart_button.quantity_input).to_have_value(
        str(_ORIGINAL_QUANTITY)
    )

    line_item.add_to_cart_button.quantity_input.fill(str(_UPDATED_QUANTITY))
    cart_page.click_outside()
    expect(cart_page.cart_quantity_label).to_have_text(str(_UPDATED_QUANTITY))
