import allure
import pytest
from playwright.sync_api import Page, expect

from core.global_settings import GlobalSettings

_PERMALINK = "/about-store"


@pytest.mark.e2e
@allure.feature("Storefront / Content Pages (E2E)")
@allure.title("About Store page is accessible from the frontend")
def test_page_about_store_accessible(global_settings: GlobalSettings, page: Page) -> None:
    url = f"{global_settings.frontend_base_url}{_PERMALINK}"

    with allure.step(f"Navigate to '{_PERMALINK}'"):
        response = page.goto(url=url, wait_until="load")
        assert response is not None, "No response received for the about-store page"
        assert response.ok, f"Expected an OK status, got {response.status}"

    with allure.step("Verify the page content is rendered"):
        expect(page).to_have_url(url)
        expect(page.get_by_text("Welcome to ACME Store")).to_be_visible()
