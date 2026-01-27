import os
from typing import Any

import pytest
from playwright.sync_api import Page, expect

from fixtures import Auth, Config
from tests_e2e.pages import HomePage


@pytest.mark.e2e
def test_e2e_main_layout_top_header_anonymous_user_elements_presence(
    config: Config,
    page: Page,
):
    print(
        f"{os.linesep}Running E2E test to check main layout top header anonymous user elements presence...",
        end=" ",
    )

    home_page = HomePage(page, config)
    home_page.navigate()

    expect(
        home_page.top_header_component.language_selector_component.element
    ).to_be_visible(), "Language selector is not visible"
    expect(
        home_page.top_header_component.currency_selector_component.element
    ).to_be_visible(), "Currency selector is not visible"
    expect(
        home_page.top_header_component.sign_in_link
    ).to_be_visible(), "Sign in link is not visible"
    expect(
        home_page.top_header_component.sign_up_link
    ).to_be_visible(), "Sign up link is not visible"


@pytest.mark.e2e
def test_e2e_main_layout_top_header_registered_user_elements_presence(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    page: Page,
):
    print(
        f"{os.linesep}Running E2E test to check main layout top header registered user elements presence...",
        end=" ",
    )

    dataset_user = dataset["users"][0]

    auth.authenticate(dataset_user["userName"], config["USERS_PASSWORD"], page)

    home_page = HomePage(page, config)
    home_page.navigate()

    expect(
        home_page.top_header_component.language_selector_component.element
    ).to_be_visible(), "Language selector is not visible"
    expect(
        home_page.top_header_component.currency_selector_component.element
    ).to_be_visible(), "Currency selector is not visible"
    expect(
        home_page.top_header_component.sign_in_link
    ).not_to_be_visible(), "Sign in link is visible"
    expect(
        home_page.top_header_component.sign_up_link
    ).not_to_be_visible(), "Sign up link is visible"
