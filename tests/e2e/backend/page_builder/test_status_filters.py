from collections.abc import Callable
from datetime import date, timedelta

import allure
import pytest
from playwright.sync_api import expect

from page_objects.backend.page_builder import (
    ALL_COLUMNS,
    DetailsToolbar,
    Menu,
    PageBuilderShell,
    Route,
    Status,
)

pytestmark = [pytest.mark.e2e, pytest.mark.admin_ui]


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Status Filters")
@allure.title("Draft filter lists only Draft pages")
def test_draft_filter(page_builder: PageBuilderShell) -> None:
    page_builder.open(Route.DRAFT)
    listing = page_builder.list_blade

    with allure.step("Grid exposes the documented columns"):
        for column in ALL_COLUMNS:
            expect(listing.grid.column_header(column)).to_be_visible()

    with allure.step("Every listed page carries a Draft badge"):
        statuses = listing.statuses
        assert statuses, "Expected at least one seeded draft page"
        assert all(Status.DRAFT in status for status in statuses), statuses

    with allure.step("Draft counter matches the number of rows"):
        assert page_builder.counter(Menu.DRAFT) == listing.count


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Status Filters")
@allure.title("Active filter lists only Published pages")
def test_active_filter(page_builder: PageBuilderShell) -> None:
    page_builder.open(Route.ACTIVE)
    listing = page_builder.list_blade

    statuses = listing.statuses
    assert statuses, "Expected at least one seeded published page"
    assert all(Status.PUBLISHED in status for status in statuses), statuses
    assert page_builder.counter(Menu.ACTIVE) == listing.count


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Status Filters")
@allure.title("Pending filter lists Published pages with a future start date")
def test_pending_filter(page_builder: PageBuilderShell, make_page: Callable[..., str]) -> None:
    name = make_page()
    start = date.today() + timedelta(days=7)

    with allure.step(f"Schedule the page to start on {start.isoformat()}"):
        page_builder.open(Route.DRAFT)
        details = page_builder.open_page(name)
        details.scheduling_section.expand()
        details.start_date.select(start)
        expect(details.start_date_input).not_to_have_value("")
        details.save()
        page_builder.notifications.wait_for_success()

    with allure.step("Publish the scheduled page"):
        details.toolbar.expect_enabled(DetailsToolbar.PUBLISH)
        details.publish()
        details.wait_settled()

    with allure.step("Page appears under Pending with a Scheduled badge"):
        listing = page_builder.wait_until_listed(Route.PENDING, name)
        assert listing.has_page(name)
        badges = listing.row(name).status_badges
        assert Status.PUBLISHED in badges, badges
        assert Status.SCHEDULED in badges, badges

    with allure.step("Pending lists only Published pages awaiting their start date"):
        statuses = listing.statuses
        assert all(Status.PUBLISHED in status for status in statuses), statuses


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Status Filters")
@allure.title("Archived filter lists only Archived pages")
def test_archived_filter(page_builder: PageBuilderShell, make_page: Callable[..., str]) -> None:
    name = make_page()
    page_builder.open(Route.DRAFT)
    page_builder.open_page(name).archive()

    listing = page_builder.wait_until_listed(Route.ARCHIVED, name)

    with allure.step("Every listed page carries an Archived badge"):
        statuses = listing.statuses
        assert statuses, "Expected at least one archived page"
        assert all(Status.ARCHIVED in status for status in statuses), statuses

    with allure.step("The archived page is listed under the Archived filter"):
        assert listing.has_page(name)
        assert listing.row(name).status == Status.ARCHIVED


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Status Filters")
@allure.title("Counters update when a page changes status")
def test_counters_update(page_builder: PageBuilderShell, make_page: Callable[..., str]) -> None:
    name = make_page()
    page_builder.open(Route.DRAFT)
    draft_before = page_builder.counter(Menu.DRAFT)
    active_before = page_builder.counter(Menu.ACTIVE)

    with allure.step("Publish the draft"):
        details = page_builder.open_page(name)
        details.publish()
        details.wait_settled()

    with allure.step("Draft counter decreases by one"):
        page_builder.wait_until_absent(Route.DRAFT, name)
        page_builder.wait_for_counter(Route.DRAFT, Menu.DRAFT, draft_before - 1)

    with allure.step("Active counter increases by one"):
        listing = page_builder.wait_until_listed(Route.ACTIVE, name)
        page_builder.wait_for_counter(Route.ACTIVE, Menu.ACTIVE, active_before + 1)
        assert listing.row(name).status == Status.PUBLISHED
