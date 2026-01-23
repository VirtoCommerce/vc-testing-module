import os

import pytest
from playwright.sync_api import Page, expect

from fixtures.config import Config
from tests_e2e.pages.sign_in_page import SignInPage


@pytest.mark.e2e
def test_e2e_change_language(config: Config, page: Page):
    print(f"{os.linesep}Running E2E test to change language...", end=" ")

    target_culture = "de-DE"
    target_language = "de"

    sign_in_page = SignInPage(page, config)
    sign_in_page.navigate()
    sign_in_page.change_language(target_culture)

    expect(
        sign_in_page.top_header_component.language_selector_component.current_language_label
    ).to_have_text(target_language)
