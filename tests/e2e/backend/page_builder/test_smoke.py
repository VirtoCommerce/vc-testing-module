import allure
import pytest
from playwright.sync_api import expect

from page_objects.backend.page_builder import (
    ALL_COLUMNS,
    Menu,
    PageBuilderShell,
    Route,
    Section,
)

pytestmark = [pytest.mark.e2e, pytest.mark.admin_ui]

_SEEDED_PAGE = "about-store"


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Smoke")
@allure.title("Shell loads authenticated with menu, grid and blade fields")
def test_shell_smoke(page_builder: PageBuilderShell) -> None:
    page_builder.open(Route.ALL)

    with allure.step("Sidebar renders all page-builder routes"):
        assert page_builder.menu.route_ids == [
            Menu.DRAFT,
            Menu.PENDING,
            Menu.ACTIVE,
            Menu.ARCHIVED,
            Menu.ALL,
            Menu.ASSETS,
        ]

    with allure.step("Grid exposes the documented columns"):
        listing = page_builder.list_blade
        for column in ALL_COLUMNS:
            expect(listing.grid.column_header(column)).to_be_visible()
        assert listing.count > 0

    with allure.step("Open a seeded page and read its details blade"):
        details = page_builder.open_page(_SEEDED_PAGE)
        expect(details.name_input).to_have_value(_SEEDED_PAGE)
        assert details.permalink_input.input_value().startswith("/")

    with allure.step("Collapsible sections expand"):
        assert details.personalization_section.is_collapsible
        details.personalization_section.expand()
        assert details.personalization_section.is_expanded
        details.scheduling_section.expand()
        expect(details.start_date_input).to_be_visible()

    with allure.step("Selects are readable once their section is expanded"):
        assert details.language.value == "en-US"
        assert Section.PERSONALIZATION
        assert details.organization.option_texts()
