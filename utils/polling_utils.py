import time
from typing import Callable, TypeVar

from core.global_settings import global_settings
from gql.types import MemberAddress

T = TypeVar("T")

AddressesResult = tuple[int, list[MemberAddress]]


def poll_until(
    fetch: Callable[[], T | None],
    predicate: Callable[[T], bool],
    attempts: int,
    interval: int,
) -> T | None:
    """Poll *fetch* up to *attempts* times, sleeping *interval* seconds between tries.

    Returns the first result for which *predicate* is ``True``,
    or ``None`` if all attempts are exhausted or *fetch* keeps returning ``None``.
    """
    for _ in range(attempts):
        result = fetch()
        if result is not None and predicate(result):
            return result
        time.sleep(interval)
    return None


def wait_addresses_visible(
    fetch: Callable[[], AddressesResult],
    seeded_descriptions: set[str],
) -> AddressesResult:
    """Poll *fetch* until every description in *seeded_descriptions* is present.

    The xAPI ``currentCustomerAddresses`` / ``currentOrganizationAddresses``
    queries are backed by an index that updates asynchronously after
    ``updateMemberAddresses``; without polling, freshly seeded addresses may
    not be visible yet. Mirrors the pattern documented in
    ``project_personalization_search_async.md``.

    If the polling budget is exhausted, returns the last fetched result so
    the caller's assertions surface a meaningful diff rather than ``None``.
    """

    def has_all(result: AddressesResult) -> bool:
        _, items = result
        present = {a.description for a in items if a.description}
        return seeded_descriptions.issubset(present)

    result = poll_until(
        fetch=fetch,
        predicate=has_all,
        attempts=global_settings.poll_attempts,
        interval=global_settings.poll_interval,
    )
    if result is None:
        return fetch()
    return result
