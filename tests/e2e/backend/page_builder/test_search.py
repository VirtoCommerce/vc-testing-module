import allure
import pytest

from page_objects.backend.page_builder import (
    Column,
    PageBuilderShell,
    PagesListBlade,
    Route,
)

pytestmark = [pytest.mark.e2e, pytest.mark.admin_ui]

_SEEDED_PAGE = "about-store"
_PARTIAL = "about"
_SPECIAL = "&"


def _every_result_matches(listing: PagesListBlade, term: str) -> bool:
    names = listing.names
    permalinks = listing.grid.values(Column.PERMALINK)
    needle = term.lower()
    return all(needle in name.lower() or needle in permalink.lower() for name, permalink in zip(names, permalinks))


@allure.feature("Page Builder Shell (E2E)")
@allure.story("Search")
@allure.title("Search matches partially and ignores case")
def test_partial_and_case_insensitive_search(
    page_builder: PageBuilderShell,
) -> None:
    page_builder.open(Route.ALL)
    listing = page_builder.list_blade
    full_list = listing.names

    with allure.step(f"Partial search for '{_PARTIAL}' narrows the list"):
        listing.search(_PARTIAL)
        lowercase_names = listing.names
        assert _SEEDED_PAGE in lowercase_names, lowercase_names
        assert len(lowercase_names) < len(full_list), lowercase_names
        assert _every_result_matches(listing, _PARTIAL), lowercase_names

    with allure.step(f"Upper-case '{_PARTIAL.upper()}' returns identical results"):
        listing.clear_search()
        listing.search(_PARTIAL.upper())
        assert listing.names == lowercase_names

    with allure.step(f"Special character '{_SPECIAL}' is handled without an error"):
        listing.clear_search()
        listing.search(_SPECIAL)
        assert page_builder.notifications.error.count() == 0
        assert _SEEDED_PAGE not in listing.names

    with allure.step("Clearing the search restores the full list"):
        listing.clear_search()
        assert listing.names == full_list
