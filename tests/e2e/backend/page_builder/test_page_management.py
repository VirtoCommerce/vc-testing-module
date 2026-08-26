from collections.abc import Callable

import allure
import pytest
from playwright.sync_api import expect

from page_objects.backend.page_builder import (
    DetailsToolbar,
    Menu,
    PageBuilderShell,
    Route,
    Status,
)

pytestmark = [pytest.mark.e2e, pytest.mark.admin_ui]

_DESIGNER_MARKER = "page-builder-designer"


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Page Management")
@allure.title("Create a new page in Page Builder")
@allure.severity(allure.severity_level.CRITICAL)
def test_create_page(page_builder: PageBuilderShell, make_page: Callable[..., str]) -> None:
    page_builder.open(Route.DRAFT)
    draft_before = page_builder.stable_counter(Menu.DRAFT)

    name = make_page()

    with allure.step("Page appears in the Draft list with the values entered"):
        page_builder.open(Route.DRAFT)
        row = page_builder.list_blade.row(name)
        expect(row.root).to_be_visible()
        assert row.permalink == f"/{name}"
        assert row.language == "en-US"
        assert row.status == Status.DRAFT

    with allure.step("Draft counter increased by 1"):
        page_builder.wait_for_counter(Route.DRAFT, Menu.DRAFT, draft_before + 1)


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Page Management")
@allure.title("Edit a created page")
def test_edit_page(page_builder: PageBuilderShell, make_page: Callable[..., str]) -> None:
    name = make_page()
    renamed = f"{name}-edited"

    page_builder.open(Route.DRAFT)
    details = page_builder.open_page(name)
    modified_before = page_builder.list_blade.row(name).modified_date

    with allure.step("Change Name and Permalink, then save"):
        details.fill(name=renamed, permalink=f"/{renamed}")
        details.save()
        page_builder.notifications.wait_for_success()

    with allure.step("Blade reflects the new values"):
        expect(details.name_input).to_have_value(renamed)
        expect(details.permalink_input).to_have_value(f"/{renamed}")

    with allure.step("List reflects the new values and a fresh Modified date"):
        listing = page_builder.wait_until_listed(Route.DRAFT, renamed)
        assert listing.has_page(renamed)
        assert not page_builder.wait_until_absent(Route.DRAFT, name).has_page(name)
        listing = page_builder.wait_until_listed(Route.DRAFT, renamed)
        row = listing.row(renamed)
        assert row.permalink == f"/{renamed}"
        assert row.modified_date != modified_before

    make_page.rename(name, renamed)


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Page Management")
@allure.title("Preview page")
@pytest.mark.skip(
    reason="No Preview control exists in the page-builder shell. The details "
    "toolbar exposes only save/delete/openPageDesigner/downloadContent/"
    "clonePage/publishPage/unpublishPage; preview lives in the designer, "
    "which is out of scope for the shell suite."
)
def test_preview_page(page_builder: PageBuilderShell) -> None:
    raise AssertionError("unreachable")


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Page Management")
@allure.title("Open page in designer opens the designer app in a new tab")
def test_open_designer(page_builder: PageBuilderShell, make_page: Callable[..., str]) -> None:
    name = make_page()
    page_builder.open(Route.DRAFT)
    details = page_builder.open_page(name)

    with allure.step("Open designer button is available"):
        details.toolbar.expect_enabled(DetailsToolbar.OPEN_DESIGNER)

    with allure.step("Clicking it targets the designer app in a new tab"):
        with details.root.page.context.expect_page() as popup_info:
            details.open_designer().click()
        designer = popup_info.value
        designer.wait_for_load_state("domcontentloaded")
        assert _DESIGNER_MARKER in designer.url, designer.url
        designer.close()


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Page Management")
@allure.title("Archive a draft page")
def test_archive_page(page_builder: PageBuilderShell, make_page: Callable[..., str]) -> None:
    name = make_page()
    page_builder.open(Route.DRAFT)
    details = page_builder.open_page(name)

    with allure.step("Archive asks for confirmation"):
        details.toolbar.click(DetailsToolbar.ARCHIVE)
        page_builder.popup.wait_until_open()
        expect(page_builder.popup.content).to_contain_text("archive")
        page_builder.popup.confirm()
        page_builder.wait_settled()

    with allure.step("Page leaves the Draft list"):
        listing = page_builder.wait_until_absent(Route.DRAFT, name)
        assert not listing.has_page(name)

    with allure.step("Page lands in Archived with an Archived badge"):
        listing = page_builder.wait_until_listed(Route.ARCHIVED, name)
        assert listing.has_page(name)
        assert listing.row(name).status == Status.ARCHIVED
