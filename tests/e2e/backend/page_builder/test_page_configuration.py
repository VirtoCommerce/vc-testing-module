from collections.abc import Callable
from datetime import date, timedelta

import allure
import pytest
from playwright.sync_api import expect

from page_objects.backend.page_builder import PageBuilderShell, Route

pytestmark = [pytest.mark.e2e, pytest.mark.admin_ui, pytest.mark.serial]

_USER_GROUP = "Wholesaler"
_ORGANIZATION = "ACME Store"


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Page Configuration")
@allure.title("Basic information section exposes Name, Permalink and Language")
def test_basic_information_fields(page_builder: PageBuilderShell, make_page: Callable[..., str]) -> None:
    name = make_page()
    page_builder.open(Route.DRAFT)
    details = page_builder.open_page(name)

    with allure.step("Basic information is present and populated"):
        expect(details.basic_section.root).to_be_visible()
        expect(details.name_input).to_have_value(name)
        expect(details.permalink_input).to_have_value(f"/{name}")
        assert details.language.value == "en-US"

    with allure.step("Name and Permalink are editable"):
        assert details.name_input.is_editable()
        assert details.permalink_input.is_editable()


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Page Configuration")
@allure.title("Scheduling section persists start and end dates")
def test_scheduling_dates(page_builder: PageBuilderShell, make_page: Callable[..., str]) -> None:
    name = make_page()
    start = date.today() + timedelta(days=3)
    end = date.today() + timedelta(days=30)

    page_builder.open(Route.DRAFT)
    details = page_builder.open_page(name)
    details.scheduling_section.expand()

    with allure.step(f"Pick start {start.isoformat()} and end {end.isoformat()}"):
        details.start_date.select(start)
        expect(details.start_date_input).not_to_have_value("")
        details.end_date.select(end)
        expect(details.end_date_input).not_to_have_value("")
        picked_start = details.start_date_input.input_value()
        picked_end = details.end_date_input.input_value()

    with allure.step("Save persists both dates"):
        details.save()
        page_builder.notifications.wait_for_success()

    with allure.step("Reopening the page shows the same scheduling values"):
        page_builder.open(Route.DRAFT)
        reopened = page_builder.open_page(name)
        reopened.scheduling_section.expand()
        expect(reopened.start_date_input).to_have_value(picked_start)
        expect(reopened.end_date_input).to_have_value(picked_end)


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Page Configuration")
@allure.title("Personalization visibility toggle persists")
def test_visibility_toggle(page_builder: PageBuilderShell, make_page: Callable[..., str]) -> None:
    name = make_page()
    page_builder.open(Route.DRAFT)
    details = page_builder.open_page(name)
    details.personalization_section.expand()

    with allure.step("Visibility defaults to on for a new page"):
        assert details.is_visible_to_all is True

    with allure.step("Turn visibility off and save"):
        details.set_visibility(False)
        assert details.is_visible_to_all is False
        details.save()
        page_builder.notifications.wait_for_success()

    with allure.step("Reopening the page keeps visibility off"):
        page_builder.open(Route.DRAFT)
        reopened = page_builder.open_page(name)
        reopened.personalization_section.expand()
        assert reopened.is_visible_to_all is False


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Page Configuration")
@allure.title("Personalization restricts the page to a user group")
def test_user_group_restriction(page_builder: PageBuilderShell, make_page: Callable[..., str]) -> None:
    name = make_page()
    page_builder.open(Route.DRAFT)
    details = page_builder.open_page(name)
    details.personalization_section.expand()

    with allure.step("The user-group dropdown offers the seeded groups"):
        options = details.user_groups.option_texts()
        assert _USER_GROUP in options, options

    with allure.step(f"Select '{_USER_GROUP}' and save"):
        details.user_groups.select(_USER_GROUP)
        assert _USER_GROUP in details.user_groups.value
        details.save()
        page_builder.notifications.wait_for_success()

    with allure.step("Reopening the page keeps the restriction"):
        page_builder.open(Route.DRAFT)
        reopened = page_builder.open_page(name)
        reopened.personalization_section.expand()
        assert _USER_GROUP in reopened.user_groups.value


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Page Configuration")
@allure.title("Personalization restricts the page to an organization")
def test_organization_restriction(page_builder: PageBuilderShell, make_page: Callable[..., str]) -> None:
    name = make_page()
    page_builder.open(Route.DRAFT)
    details = page_builder.open_page(name)
    details.personalization_section.expand()

    with allure.step("The organization dropdown offers the seeded organizations"):
        options = details.organization.option_texts()
        assert _ORGANIZATION in options, options[:10]

    with allure.step(f"Select '{_ORGANIZATION}' and save"):
        details.organization.select(_ORGANIZATION)
        assert _ORGANIZATION in details.organization.value
        details.save()
        page_builder.notifications.wait_for_success()

    with allure.step("Reopening the page keeps the restriction"):
        page_builder.open(Route.DRAFT)
        reopened = page_builder.open_page(name)
        reopened.personalization_section.expand()
        assert _ORGANIZATION in reopened.organization.value


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Page Configuration")
@allure.title("Page blade exposes every configuration field")
def test_all_configuration_fields(page_builder: PageBuilderShell, make_page: Callable[..., str]) -> None:
    name = make_page()
    page_builder.open(Route.DRAFT)
    details = page_builder.open_page(name)

    with allure.step("Basic information: Name, Permalink, Language"):
        expect(details.name_input).to_be_visible()
        expect(details.permalink_input).to_be_visible()
        expect(details.language.toggle).to_be_visible()

    with allure.step("Personalization: Visibility, User groups, Organization"):
        details.personalization_section.expand()
        expect(details.visibility_toggle).to_be_attached()
        expect(details.user_groups.toggle).to_be_visible()
        expect(details.organization.toggle).to_be_visible()

    with allure.step("Scheduling: Start date and End date"):
        details.scheduling_section.expand()
        expect(details.start_date_input).to_be_visible()
        expect(details.end_date_input).to_be_visible()

    with allure.step("Editing Name and Permalink persists to the list"):
        renamed = f"{name}-cfg"
        details.fill(name=renamed, permalink=f"/{renamed}")
        details.save()
        page_builder.notifications.wait_for_success()
        make_page.rename(name, renamed)

        listing = page_builder.wait_until_listed(Route.DRAFT, renamed)
        assert listing.has_page(renamed)
        assert listing.row(renamed).permalink == f"/{renamed}"
