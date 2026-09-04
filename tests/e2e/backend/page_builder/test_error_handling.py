from collections.abc import Callable

import allure
import pytest

from page_objects.backend.page_builder import (
    DetailsToolbar,
    PageBuilderShell,
    Route,
)

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.admin_ui,
    pytest.mark.serial,
    pytest.mark.with_user(app="admin"),
]

_EXISTING_PERMALINK = "/about-store"

_DUPLICATE_ALLOWED = (
    "PageBuilderModule accepts a second page with an existing permalink in the "
    "same language: the save succeeds, no error notification is raised and the "
    "page is created. The suite expects the duplicate to be rejected."
)
_NO_SANITISATION = (
    "PageBuilderModule stores the permalink verbatim: neither sanitised nor "
    "rejected. The suite expects one or the other."
)

_PERMALINKS = [
    pytest.param(
        "spaces",
        "/my page test",
        marks=pytest.mark.xfail(reason=_NO_SANITISATION, strict=True),
        id="spaces",
    ),
    pytest.param(
        "reserved characters",
        "/page&test?q=1#anchor",
        marks=pytest.mark.xfail(reason=_NO_SANITISATION, strict=True),
        id="reserved-characters",
    ),
    pytest.param("unicode", "/страница-тест", id="unicode"),
]


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Error Handling")
@allure.title("A duplicate permalink is rejected")
@pytest.mark.xfail(reason=_DUPLICATE_ALLOWED, strict=True)
def test_duplicate_permalink(
    page_builder: PageBuilderShell,
    unique_name: Callable[[str], str],
) -> None:
    name = unique_name("qa-dup")
    page_builder.open(Route.DRAFT)
    details = page_builder.add_page()

    with allure.step(f"Create a page reusing the permalink {_EXISTING_PERMALINK}"):
        details.fill(name=name, permalink=_EXISTING_PERMALINK)
        details.language.select("en-US")
        details.toolbar.expect_enabled(DetailsToolbar.SAVE)
        details.save()
        details.wait_settled()

    with allure.step("The save is refused and the page is not created"):
        errored = page_builder.notifications.error.count() > 0
        listing = page_builder.wait_until_listed(Route.DRAFT, name)
        created = listing.has_page(name)
        assert errored or not created, (
            "Expected a duplicate permalink to be rejected, but the page was " "created without any error notification"
        )


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Error Handling")
@allure.title("Save stays disabled while required fields are empty")
def test_empty_required_fields(page_builder: PageBuilderShell) -> None:
    page_builder.open(Route.DRAFT)
    details = page_builder.add_page()

    with allure.step("A brand-new page blade cannot be saved"):
        details.toolbar.expect_disabled(DetailsToolbar.SAVE)

    with allure.step("Filling only the Name leaves Save disabled"):
        details.fill(name="qa-missing-permalink")
        details.toolbar.expect_disabled(DetailsToolbar.SAVE)

    with allure.step("Clearing the Name and filling only the Permalink also blocks Save"):
        details.fill(name="", permalink="/qa-missing-name")
        details.toolbar.expect_disabled(DetailsToolbar.SAVE)

    with allure.step("Both required fields together enable Save"):
        details.fill(name="qa-both-fields")
        details.toolbar.expect_enabled(DetailsToolbar.SAVE)


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Error Handling")
@allure.title("Special characters in a permalink are sanitised or rejected")
@pytest.mark.parametrize("label,permalink", _PERMALINKS)
def test_special_characters_in_permalink(
    page_builder: PageBuilderShell,
    unique_name: Callable[[str], str],
    label: str,
    permalink: str,
) -> None:
    name = unique_name("qa-chars")
    page_builder.open(Route.DRAFT)
    details = page_builder.add_page()

    with allure.step(f"Create a page with a permalink containing {label}"):
        details.fill(name=name, permalink=permalink)
        details.language.select("en-US")
        details.save()
        details.wait_settled()

    with allure.step("No server error is surfaced"):
        assert page_builder.notifications.error.count() == 0

    with allure.step("The shell either rejects the permalink or stores a safe form"):
        listing = page_builder.wait_until_listed(Route.DRAFT, name)
        if not listing.has_page(name):
            return

        stored = listing.row(name).permalink
        assert " " not in stored, f"Stored permalink still contains spaces: {stored!r}"
        assert "#" not in stored, f"Stored permalink keeps a fragment: {stored!r}"
        assert "?" not in stored, f"Stored permalink keeps a query string: {stored!r}"
