import allure
import pytest
from core.global_settings import GlobalSettings
from page_objects.pages.category import CategoryPage
from playwright.sync_api import Page, Response, expect

_CATEGORY_PATH = "smartphones"
_PRODUCT_SKU = "smartphone-google-pixel-10-frost"
_VARIATION_1_SKU = "smartphone-google-pixel-10-indigo"
_VARIATION_2_SKU = "smartphone-google-pixel-10-lemongrass"


def _is_cart_mutation(response: Response) -> bool:
    post = response.request.post_data
    return bool(post and "/graphql" in response.url and "mutation" in post)


@pytest.mark.e2e
@pytest.mark.quantity_control("stepper")
@pytest.mark.delete_cart_after
@pytest.mark.flaky(retries=3, delay=5)
@allure.feature("Category / Product variations (E2E)")
@allure.title("Update cart from product variations using stepper controls")
def test_category_variation_update_cart_stepper(global_settings: GlobalSettings, page: Page) -> None:
    category_page = CategoryPage(global_settings=global_settings, page=page, path=_CATEGORY_PATH)

    with allure.step(f"Navigate to category '{_CATEGORY_PATH}' and open variations on '{_PRODUCT_SKU}'"):
        category_page.navigate()
        category_page.view_switcher.list_view_tab.click()
        product_card = category_page.scroll_to_product(sku=_PRODUCT_SKU)
        expect(product_card.root).to_be_visible()
        expect(product_card.variations_button).to_be_visible()
        product_card.variations_button.click()

    variation_1 = product_card.find_variation_item(sku=_VARIATION_1_SKU)
    variation_2 = product_card.find_variation_item(sku=_VARIATION_2_SKU)

    with allure.step(f"Increment variation '{_VARIATION_1_SKU}' twice; verify cart counter updates"):
        with page.expect_response(_is_cart_mutation):
            variation_1.quantity_stepper.increment_button.click()
        expect(category_page.cart_quantity_label).to_have_text("1")
        with page.expect_response(_is_cart_mutation):
            variation_1.quantity_stepper.increment_button.click()
        expect(category_page.cart_quantity_label).to_have_text("2")

    with allure.step(f"Increment variation '{_VARIATION_2_SKU}' twice; verify cart counter updates"):
        with page.expect_response(_is_cart_mutation):
            variation_2.quantity_stepper.increment_button.click()
        expect(category_page.cart_quantity_label).to_have_text("3")
        with page.expect_response(_is_cart_mutation):
            variation_2.quantity_stepper.increment_button.click()
        expect(category_page.cart_quantity_label).to_have_text("4")

    with allure.step("Decrement one of each variation; verify cart counter updates"):
        with page.expect_response(_is_cart_mutation):
            variation_1.quantity_stepper.decrement_button.click()
        expect(category_page.cart_quantity_label).to_have_text("3")
        with page.expect_response(_is_cart_mutation):
            variation_2.quantity_stepper.decrement_button.click()
        expect(category_page.cart_quantity_label).to_have_text("2")


@pytest.mark.e2e
@pytest.mark.quantity_control("button")
@pytest.mark.delete_cart_after
@pytest.mark.flaky(retries=3, delay=5)
@allure.feature("Category / Product variations (E2E)")
@allure.title("Update cart from product variations using add-to-cart buttons")
def test_category_variation_update_cart_button(global_settings: GlobalSettings, page: Page) -> None:
    category_page = CategoryPage(global_settings=global_settings, page=page, path=_CATEGORY_PATH)

    with allure.step(f"Navigate to category '{_CATEGORY_PATH}' and open variations on '{_PRODUCT_SKU}'"):
        category_page.navigate()
        category_page.view_switcher.list_view_tab.click()
        product_card = category_page.scroll_to_product(sku=_PRODUCT_SKU)
        expect(product_card.root).to_be_visible()
        expect(product_card.variations_button).to_be_visible()
        product_card.variations_button.click()

    variation_1 = product_card.find_variation_item(sku=_VARIATION_1_SKU)
    variation_2 = product_card.find_variation_item(sku=_VARIATION_2_SKU)

    with allure.step(f"Add 1 then 2 of variation '{_VARIATION_1_SKU}' via the button input"):
        variation_1.add_to_cart_button.quantity_input.fill("1")
        variation_1.add_to_cart_button.icon_button.click()
        expect(category_page.cart_quantity_label).to_have_text("1")
        variation_1.add_to_cart_button.quantity_input.fill("2")
        variation_1.add_to_cart_button.icon_button.click()
        expect(category_page.cart_quantity_label).to_have_text("2")

    with allure.step(f"Add 1 then 2 of variation '{_VARIATION_2_SKU}' via the button input"):
        variation_2.add_to_cart_button.quantity_input.fill("1")
        variation_2.add_to_cart_button.icon_button.click()
        expect(category_page.cart_quantity_label).to_have_text("3")
        variation_2.add_to_cart_button.quantity_input.fill("2")
        variation_2.add_to_cart_button.icon_button.click()
        expect(category_page.cart_quantity_label).to_have_text("4")
