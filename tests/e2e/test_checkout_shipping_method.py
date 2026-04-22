import pytest
from core.global_settings import GlobalSettings
from page_objects.pages import CartPage, CheckoutShippingPage
from playwright.sync_api import Page, expect

from dataset.dataset_manager import DatasetManager

_PRODUCT_ID = "smartphone-google-pixel-10-lemongrass"
_QUANTITY = 3
_FIXED_RATE = "FixedRate"
_GROUND = "Ground"
_AIR = "Air"
_FIXED_RATE_GROUND = f"{_FIXED_RATE}_{_GROUND}"
_FIXED_RATE_AIR = f"{_FIXED_RATE}_{_AIR}"


@pytest.mark.e2e
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("single-page")
def test_checkout_shipping_method_single_page(
    global_settings: GlobalSettings, page: Page, dataset_manager: DatasetManager
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()
    expect(cart_page.shipping_details_section.root).to_be_visible()

    cart_page.shipping_details_section.shipping_switcher.click()
    expect(cart_page.shipping_details_section.shipping_method_selector).to_be_visible()

    fixed_rate_ground = dataset_manager.find_shipping_method(code=_FIXED_RATE, option="Ground")
    fixed_rate_air = dataset_manager.find_shipping_method(code=_FIXED_RATE, option="Air")

    cart_page.shipping_details_section.select_shipping_method(_FIXED_RATE_GROUND)
    selected_shipping_method = cart_page.shipping_details_section.find_selected_shipping_method(code=_FIXED_RATE_GROUND)
    expect(selected_shipping_method).to_be_visible()
    expect(cart_page.shipping_cost_label).to_contain_text(str(fixed_rate_ground["option"]["price"]))

    cart_page.shipping_details_section.select_shipping_method(_FIXED_RATE_AIR)
    selected_shipping_method = cart_page.shipping_details_section.find_selected_shipping_method(code=_FIXED_RATE_AIR)
    expect(selected_shipping_method).to_be_visible()
    expect(cart_page.shipping_cost_label).to_contain_text(str(fixed_rate_air["option"]["price"]))


@pytest.mark.e2e
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.checkout_mode("multi-step")
def test_checkout_shipping_method_multi_step(
    global_settings: GlobalSettings, page: Page, dataset_manager: DatasetManager
) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)
    cart_page.navigate()
    expect(cart_page.checkout_button).to_be_visible()
    expect(cart_page.checkout_button).to_be_enabled()

    cart_page.checkout_button.click()
    shipping_page = CheckoutShippingPage(global_settings=global_settings, page=page)
    expect(shipping_page.shipping_details_section.root).to_be_visible()
    expect(shipping_page.shipping_details_section.shipping_method_selector).to_be_visible()

    fixed_rate_ground = dataset_manager.find_shipping_method(code=_FIXED_RATE, option="Ground")
    fixed_rate_air = dataset_manager.find_shipping_method(code=_FIXED_RATE, option="Air")

    shipping_page.shipping_details_section.select_shipping_method(_FIXED_RATE_GROUND)
    expect(shipping_page.shipping_cost_label).to_contain_text(str(fixed_rate_ground["option"]["price"]))

    shipping_page.shipping_details_section.select_shipping_method(_FIXED_RATE_AIR)
    expect(shipping_page.shipping_cost_label).to_contain_text(str(fixed_rate_air["option"]["price"]))
