from collections.abc import Callable

import allure
import pytest
from playwright.sync_api import expect

from page_objects.backend.page_builder import Column, PageBuilderShell, Route

pytestmark = [
    pytest.mark.e2e,
    pytest.mark.admin_ui,
    pytest.mark.serial,
    pytest.mark.with_user(app="admin"),
]

_MARKER = "searchable"
_SEEDED_PAGE = "our-team"
_NO_MATCH = "&"

_SORT_WINDOW_BUG = (
    "POST /api/page-builder-pages/search applies the keyword filter only to the "
    "sorted page window instead of the whole set. With the shell's default "
    "sort=modifiedDate:DESC and take=20, keyword='team' returns totalCount 0, "
    "while the same query without sort, or with take=100, or with "
    "sort=modifiedDate:ASC, returns the page. Search therefore stops finding "
    "anything outside the newest 20 rows as the store grows."
)


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Search")
@allure.title("Search matches partially and ignores case")
def test_partial_and_case_insensitive_search(
    page_builder: PageBuilderShell,
    make_page: Callable[..., str],
    unique_name: Callable[[str], str],
) -> None:
    name = make_page(name=unique_name(f"qa-{_MARKER}"))
    page_builder.open(Route.ALL)
    listing = page_builder.list_blade
    row = listing.grid.row_locator(Column.NAME, name)

    with allure.step(f"Partial lower-case search for '{_MARKER}' finds the page"):
        listing.search(_MARKER)
        expect(row).to_have_count(1)
        lowercase_names = listing.names

    with allure.step(f"Upper-case '{_MARKER.upper()}' returns identical results"):
        listing.search(_MARKER.upper())
        expect(row).to_have_count(1)
        assert listing.names == lowercase_names

    with allure.step(f"'{_NO_MATCH}' is handled without an error and excludes the page"):
        listing.search(_NO_MATCH)
        expect(row).to_have_count(0)
        assert page_builder.notifications.error.count() == 0

    with allure.step("Clearing the search restores the unfiltered list"):
        listing.clear_search()
        expect(row).to_have_count(1)


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Search")
@allure.title("Search finds a page beyond the first page of the default sort")
@pytest.mark.xfail(reason=_SORT_WINDOW_BUG, strict=False)
def test_search_reaches_beyond_the_first_sort_page(
    page_builder: PageBuilderShell,
) -> None:
    page_builder.open(Route.ALL)
    listing = page_builder.list_blade
    listing.grid.rows.first.wait_for(state="visible")

    info = listing.grid.pagination_info
    if info is None or info[2] <= info[1]:
        pytest.skip("Store holds a single page of results; the defect cannot manifest")

    listing.search(_SEEDED_PAGE)
    expect(listing.grid.row_locator(Column.NAME, _SEEDED_PAGE)).to_have_count(1, timeout=10000)
