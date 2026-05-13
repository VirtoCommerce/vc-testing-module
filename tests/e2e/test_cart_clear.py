import allure
import pytest
from core.global_settings import GlobalSettings
from page_objects.components import ClearCartModal
from page_objects.pages import CartPage
from playwright.sync_api import Page, Response, expect

_PRODUCT_ID = "smartphone-samsung-galaxy-a57-5g"
_QUANTITY = 3


def _is_full_cart_query(response: Response) -> bool:
    post = response.request.post_data
    return bool(post and "/graphql" in response.url and "GetFullCart" in post)


def _is_clear_cart_mutation(response: Response) -> bool:
    post = response.request.post_data
    return bool(post and "/graphql" in response.url and "ClearCart" in post)


@pytest.mark.e2e
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@pytest.mark.flaky(retries=2, delay=3)
@allure.feature("Cart / Lifecycle (E2E)")
@allure.title("Clear all items from cart via the clear-cart modal")
def test_cart_clear(page: Page, global_settings: GlobalSettings) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Open cart page and verify the seeded line item is shown"):
        with page.expect_response(_is_full_cart_query):
            cart_page.navigate()
        expect(cart_page.line_items).to_be_visible()
        expect(cart_page.line_items).to_have_count(1)
        expect(cart_page.clear_cart_button).to_be_visible()
        expect(cart_page.clear_cart_button).to_be_enabled()

    with allure.step("Open clear-cart confirmation modal"):
        cart_page.clear_cart_button.click()
        clear_cart_modal = ClearCartModal(root=page.locator("[data-test-id='clear-cart-modal']"))
        expect(clear_cart_modal.root).to_be_visible()
        expect(clear_cart_modal.yes_button).to_be_visible()
        expect(clear_cart_modal.yes_button).to_be_enabled()

    with allure.step("Confirm clear cart and verify line items are gone"):
        with page.expect_response(_is_clear_cart_mutation):
            clear_cart_modal.yes_button.click()
        expect(clear_cart_modal.root).not_to_be_visible()
        expect(cart_page.line_items).to_have_count(0, timeout=15000)
