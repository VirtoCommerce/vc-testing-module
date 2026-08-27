from urllib.parse import urlparse

import allure
import pytest
from playwright.sync_api import expect

from core.global_settings import GlobalSettings
from page_objects.backend.page_builder import PageBuilderShell, Route

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.admin_ui,
    pytest.mark.serial,
    pytest.mark.with_user(app="admin"),
]

_SEEDED_PUBLISHED_PAGE = "about-store"


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Admin Integration")
@allure.title("Page blade shows the storefront URL next to the permalink")
def test_frontend_url_displayed(page_builder: PageBuilderShell, global_settings: GlobalSettings) -> None:
    page_builder.open(Route.ACTIVE)
    details = page_builder.open_page(_SEEDED_PUBLISHED_PAGE)

    with allure.step("A storefront URL prefix is rendered with the permalink field"):
        expect(details.permalink_prefix).to_be_visible()
        prefix = details.permalink_prefix.inner_text().strip()

    with allure.step(f"Prefix '{prefix}' points at the configured storefront host"):
        assert urlparse(prefix).hostname == urlparse(global_settings.frontend_base_url).hostname

    with allure.step("Prefix and permalink compose the public page URL"):
        permalink = details.permalink_input.input_value()
        assert permalink.startswith("/")
        assert f"{prefix}{permalink}".endswith(permalink)


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Authentication")
@allure.title("Shell shows the signed-in user, their role, and the logo")
def test_user_profile_and_logo(page_builder: PageBuilderShell, global_settings: GlobalSettings) -> None:
    page_builder.open(Route.ALL)

    with allure.step("User profile shows the signed-in account and its role"):
        expect(page_builder.user_name).to_be_visible()
        expect(page_builder.user_name).to_have_text(global_settings.admin_username)
        expect(page_builder.user_role).to_be_visible()
        expect(page_builder.user_role).to_have_text("Administrator")

    with allure.step("Virto Commerce logo is displayed"):
        expect(page_builder.logo).to_be_visible()
        assert page_builder.logo.get_attribute("alt") == "logo"
