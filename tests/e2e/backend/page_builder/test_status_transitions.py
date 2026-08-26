from collections.abc import Callable

import allure
import pytest

from page_objects.backend.page_builder import (
    DetailsToolbar,
    Menu,
    PageBuilderShell,
    Route,
    Status,
)

pytestmark = [pytest.mark.e2e, pytest.mark.admin_ui, pytest.mark.serial]

_NO_TOAST_REASON = (
    "PageBuilderModule emits no vc-notification for publish/unpublish/archive. "
    "Verified with a MutationObserver over a 4s window: only Save produces a "
    "toast. The suite documents this as a product gap."
)


def _publish(page_builder: PageBuilderShell, name: str) -> None:
    details = page_builder.open_page(name)
    details.toolbar.expect_enabled(DetailsToolbar.PUBLISH)
    details.publish()
    details.wait_settled()


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Status Transitions")
@allure.title("Publish a draft page moves it from Draft to Active")
@allure.severity(allure.severity_level.CRITICAL)
def test_publish_draft_page(page_builder: PageBuilderShell, make_page: Callable[..., str]) -> None:
    name = make_page()

    with allure.step("Publish the draft"):
        _publish(page_builder, name)

    with allure.step("Page leaves Draft"):
        assert not page_builder.wait_until_absent(Route.DRAFT, name).has_page(name)

    with allure.step("Page appears in Active with a Published badge"):
        listing = page_builder.wait_until_listed(Route.ACTIVE, name)
        assert listing.row(name).status == Status.PUBLISHED

    with allure.step("Both counters stay in step with their lists"):
        page_builder.wait_for_counter_sync(Route.DRAFT, Menu.DRAFT)
        page_builder.wait_for_counter_sync(Route.ACTIVE, Menu.ACTIVE)


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Status Transitions")
@allure.title("Published page can be archived")
def test_publish_to_archive(page_builder: PageBuilderShell, make_page: Callable[..., str]) -> None:
    name = make_page()
    _publish(page_builder, name)
    page_builder.wait_until_listed(Route.ACTIVE, name)

    with allure.step("Archive the published page"):
        details = page_builder.open_page(name)
        details.archive()

    with allure.step("Page leaves Active and lands in Archived"):
        assert not page_builder.wait_until_absent(Route.ACTIVE, name).has_page(name)
        listing = page_builder.wait_until_listed(Route.ARCHIVED, name)
        assert listing.row(name).status == Status.ARCHIVED


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Status Transitions")
@allure.title("Draft page can be archived")
def test_draft_to_archive(page_builder: PageBuilderShell, make_page: Callable[..., str]) -> None:
    name = make_page()

    with allure.step("Archive the draft page"):
        page_builder.open(Route.DRAFT)
        page_builder.open_page(name).archive()

    with allure.step("Page leaves Draft and lands in Archived"):
        assert not page_builder.wait_until_absent(Route.DRAFT, name).has_page(name)
        listing = page_builder.wait_until_listed(Route.ARCHIVED, name)
        assert listing.row(name).status == Status.ARCHIVED


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Status Transitions")
@allure.title("Unpublish reverts a published page to Draft")
def test_unpublish_reverts_to_draft(page_builder: PageBuilderShell, make_page: Callable[..., str]) -> None:
    name = make_page()
    _publish(page_builder, name)
    page_builder.wait_until_listed(Route.ACTIVE, name)

    with allure.step("Unpublish is offered on a published page"):
        details = page_builder.open_page(name)
        details.toolbar.expect_enabled(DetailsToolbar.UNPUBLISH)
        details.unpublish()
        details.wait_settled()

    with allure.step("Page returns to Draft and leaves Active"):
        assert not page_builder.wait_until_absent(Route.ACTIVE, name).has_page(name)
        listing = page_builder.wait_until_listed(Route.DRAFT, name)
        assert listing.row(name).status == Status.DRAFT

    with allure.step("Content is preserved for re-publishing"):
        details = page_builder.open_page(name)
        details.toolbar.expect_enabled(DetailsToolbar.PUBLISH)


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Status Transitions")
@allure.title("Publishing a page shows a success toast")
@pytest.mark.xfail(reason=_NO_TOAST_REASON, strict=True)
def test_publish_emits_toast(page_builder: PageBuilderShell, make_page: Callable[..., str]) -> None:
    name = make_page()
    _publish(page_builder, name)
    page_builder.notifications.wait_for_success("published")
