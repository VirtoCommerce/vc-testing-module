import os

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.config import Config
from tests_e2e.pages.sign_in_page import SignInPage


@pytest.mark.e2e
@allure.title("Change currency (E2E)")
def test_e2e_change_currency(config: Config, page: Page):
    print(f"{os.linesep}Running E2E test to change currency...", end=" ")

    target_currency = "EUR"

    sign_in_page = SignInPage(page, config)
    sign_in_page.navigate()
    sign_in_page.change_currency(target_currency)

    expect(
        sign_in_page.top_header_component.currency_selector_component.current_currency_label
    ).to_have_text(target_currency)
