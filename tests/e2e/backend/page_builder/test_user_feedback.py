from collections.abc import Callable

import allure
import pytest
from playwright.sync_api import expect

from page_objects.backend.page_builder import (
    DetailsToolbar,
    PageBuilderShell,
    Route,
    Status,
)

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.admin_ui,
    pytest.mark.serial,
    pytest.mark.with_user(app="admin"),
]

_SAVE_TOAST = "Page saved successfully"
_NO_UNPUBLISH_TOAST = (
    "PageBuilderModule emits no vc-notification on unpublish. Verified with a "
    "MutationObserver over a 4s window: only Save produces a toast."
)


@allure.feature("Page Builder Shell (E2E)")
@allure.story("User Feedback")
@allure.title("Saving a page shows a success toast and disables Save")
def test_save_success_toast(page_builder: PageBuilderShell, make_page: Callable[..., str]) -> None:
    name = make_page()
    page_builder.open(Route.DRAFT)
    details = page_builder.open_page(name)

    with allure.step("Save is disabled while the blade is unmodified"):
        details.toolbar.expect_disabled(DetailsToolbar.SAVE)

    with allure.step("Editing a field enables Save"):
        details.fill(name=f"{name}-toast")
        details.toolbar.expect_enabled(DetailsToolbar.SAVE)

    with allure.step("Saving raises a green success toast"):
        details.save()
        toast = page_builder.notifications.wait_for_success(_SAVE_TOAST)
        expect(toast).to_contain_text(_SAVE_TOAST)

    with allure.step("Save returns to disabled once the blade is unmodified again"):
        details.toolbar.expect_disabled(DetailsToolbar.SAVE)

    with allure.step("The toast auto-dismisses"):
        page_builder.notifications.all.first.wait_for(state="detached", timeout=15000)


@allure.feature("Page Builder Shell (E2E)")
@allure.story("User Feedback")
@allure.title("Unpublishing moves the page back to Draft")
def test_unpublish_moves_to_draft(page_builder: PageBuilderShell, make_page: Callable[..., str]) -> None:
    name = make_page()

    with allure.step("Publish the page so it appears under Active"):
        page_builder.open(Route.DRAFT)
        details = page_builder.open_page(name)
        details.publish()
        details.wait_settled()
        page_builder.wait_until_listed(Route.ACTIVE, name)

    with allure.step("Unpublish it from the Active list"):
        details = page_builder.open_page(name)
        details.toolbar.expect_enabled(DetailsToolbar.UNPUBLISH)
        details.unpublish()
        details.wait_settled()

    with allure.step("Page returns to the Draft list"):
        listing = page_builder.wait_until_listed(Route.DRAFT, name)
        assert listing.row(name).status == Status.DRAFT


@allure.feature("Page Builder Shell (E2E)")
@allure.story("User Feedback")
@allure.title("Unpublishing a page shows a success toast")
@pytest.mark.xfail(reason=_NO_UNPUBLISH_TOAST, strict=True)
def test_unpublish_success_toast(page_builder: PageBuilderShell, make_page: Callable[..., str]) -> None:
    name = make_page()
    page_builder.open(Route.DRAFT)
    details = page_builder.open_page(name)
    details.publish()
    details.wait_settled()
    page_builder.wait_until_listed(Route.ACTIVE, name)

    details = page_builder.open_page(name)
    details.unpublish()
    page_builder.notifications.wait_for_success("unpublished")
