import allure
import pytest
from core.global_settings import GlobalSettings
from page_objects.pages import CartPage
from playwright.sync_api import Page, Response, expect

_PRODUCT_ID = "smartphone-samsung-galaxy-a57-5g"
_ORIGINAL_QUANTITY = 3
_UPDATED_QUANTITY = 4
_USERNAME = "acme_store_employee_1@acme.com"


def _is_cart_mutation(response: Response) -> bool:
    post = response.request.post_data
    return bool(post and "/graphql" in response.url and "mutation" in post)


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _ORIGINAL_QUANTITY)])
@pytest.mark.quantity_control("stepper")
@allure.feature("Cart / Line items (E2E)")
@allure.title("Update line item quantity using the stepper control")
def test_cart_item_update_stepper(global_settings: GlobalSettings, page: Page) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page"):
        cart_page.navigate()

    with allure.step(f"Verify line item '{_PRODUCT_ID}' shows initial quantity {_ORIGINAL_QUANTITY}"):
        line_item = cart_page.find_line_item(sku=_PRODUCT_ID)
        expect(line_item.root).to_be_visible()
        expect(line_item.quantity_stepper.root).to_be_visible()
        expect(line_item.quantity_stepper.quantity_input).to_have_value(str(_ORIGINAL_QUANTITY))

    with allure.step(f"Increment quantity to {_UPDATED_QUANTITY} and verify cart badge"):
        with page.expect_response(_is_cart_mutation):
            line_item.quantity_stepper.increment_button.click()
        expect(cart_page.cart_quantity_label).to_have_text(str(_UPDATED_QUANTITY))


@pytest.mark.e2e
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _ORIGINAL_QUANTITY)])
@pytest.mark.quantity_control("button")
@allure.feature("Cart / Line items (E2E)")
@allure.title("Update line item quantity using the add-to-cart button input")
def test_cart_item_update_button(global_settings: GlobalSettings, page: Page) -> None:
    cart_page = CartPage(global_settings=global_settings, page=page)

    with allure.step("Navigate to the cart page"):
        cart_page.navigate()

    with allure.step(f"Verify line item '{_PRODUCT_ID}' shows initial quantity {_ORIGINAL_QUANTITY}"):
        line_item = cart_page.find_line_item(sku=_PRODUCT_ID)
        expect(line_item.root).to_be_visible()
        expect(line_item.add_to_cart_button.root).to_be_visible()
        expect(line_item.add_to_cart_button.quantity_input).to_have_value(str(_ORIGINAL_QUANTITY))

    with allure.step(f"Type quantity {_UPDATED_QUANTITY} and verify cart badge"):
        line_item.add_to_cart_button.quantity_input.fill(str(_UPDATED_QUANTITY))
        cart_page.click_outside()
        expect(cart_page.cart_quantity_label).to_have_text(str(_UPDATED_QUANTITY))
