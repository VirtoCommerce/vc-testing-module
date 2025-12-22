import os
from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.config import Config
from tests_e2e.pages.home_page import HomePage
from tests_e2e.pages.sign_in_page import SignInPage


@pytest.mark.e2e
@allure.feature("Sign in with valid credentials (E2E)")
def test_e2e_valid_sign_in(config: Config, dataset: dict[str, Any], page: Page):
    print(f"{os.linesep}Running E2E test to sign in with valid credentials...", end=" ")

    home_page = HomePage(page, config)
    sign_in_page = SignInPage(page, config)

    dataset_user = dataset["users"][0]

    sign_in_page.navigate()

    sign_in_page.sign_in(dataset_user["userName"], config["USERS_PASSWORD"])

    expect(page).to_have_url(home_page.url)
    expect(home_page.top_header_component.sign_in_link).not_to_be_visible()
    expect(home_page.top_header_component.sign_up_link).not_to_be_visible()
    expect(home_page.top_header_component.dashboard_link).to_be_visible()


@pytest.mark.e2e
@allure.feature("Sign in with invalid credentials (E2E)")
def test_e2e_invalid_sign_in(config: Config, page: Page):
    print(
        f"{os.linesep}Running E2E test to sign in with invalid credentials...", end=" "
    )

    sign_in_page = SignInPage(page, config)

    sign_in_page.navigate()

    sign_in_page.sign_in("fake-username@test.com", "FakePassword1!")

    expect(page).to_have_url(sign_in_page.url)
    expect(sign_in_page.sign_in_error_alert).to_be_visible()
