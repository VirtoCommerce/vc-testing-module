import allure
import pytest
from core.global_settings import GlobalSettings
from page_objects.pages import CategoryPage
from playwright.sync_api import Page, expect

_CATEGORY_PATH = "smartphones"
_PRODUCT_SKU = "smartphone-samsung-galaxy-a57-5g"


@pytest.mark.e2e
@pytest.mark.quantity_control("stepper")
@pytest.mark.flaky(retries=2, delay=3)
@allure.feature("Category / Add-to-cart viewport (E2E)")
@allure.title("Stepper add-to-cart control stays visible in narrow viewport")
def test_category_add_to_cart_viewport_stepper(global_settings: GlobalSettings, page: Page) -> None:
    category_page = CategoryPage(global_settings=global_settings, page=page, path=_CATEGORY_PATH)

    with allure.step(f"Navigate to category '{_CATEGORY_PATH}' and locate product card"):
        category_page.navigate()
        product_card = category_page.scroll_to_product(sku=_PRODUCT_SKU)
        expect(product_card.root).to_be_visible()
        expect(product_card.quantity_stepper.root).to_be_visible()

    with allure.step("Resize viewport to 800x600 and verify stepper still visible"):
        page.set_viewport_size({"width": 800, "height": 600})
        expect(product_card.quantity_stepper.root).to_be_visible()


@pytest.mark.e2e
@pytest.mark.quantity_control("button")
@pytest.mark.flaky(retries=2, delay=3)
@allure.feature("Category / Add-to-cart viewport (E2E)")
@allure.title("Add-to-cart button collapses to icon button in narrow viewport")
def test_category_add_to_cart_viewport_button(global_settings: GlobalSettings, page: Page) -> None:
    category_page = CategoryPage(global_settings=global_settings, page=page, path=_CATEGORY_PATH)

    with allure.step(f"Navigate to category '{_CATEGORY_PATH}' and locate product card"):
        category_page.navigate()
        product_card = category_page.scroll_to_product(sku=_PRODUCT_SKU)
        expect(product_card.root).to_be_visible()
        expect(product_card.add_to_cart_button.root).to_be_visible()
        expect(product_card.add_to_cart_button.text_button).to_be_visible()

    with allure.step("Resize viewport to 800x600 and verify icon button is shown"):
        page.set_viewport_size({"width": 800, "height": 600})
        expect(product_card.add_to_cart_button.icon_button).to_be_visible()
