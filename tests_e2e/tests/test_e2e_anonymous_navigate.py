import os

import pytest
from playwright.sync_api import Page, expect

from fixtures import Config
from tests_e2e.pages import HomePage


@pytest.mark.e2e
def test_e2e_navigate_application_as_anonymous_user(
    config: Config,
    page: Page,
):
    print(
        f"{os.linesep}Running E2E test to navigate application as anonymous user...",
        end=" ",
    )

    home_page = HomePage(page, config)
    home_page.navigate()

    expect(page).to_have_url(home_page.url)
