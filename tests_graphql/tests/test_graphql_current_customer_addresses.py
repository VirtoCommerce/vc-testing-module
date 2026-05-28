import logging
import uuid
from typing import Any

import allure
import pytest

from fixtures.auth import Auth
from fixtures.config import Config
from fixtures.graphql_client import GraphQLClient
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations

logger = logging.getLogger(__name__)

_AUTH_ERROR_TOKENS = ("unauthor", "authentic", "permission", "forbidden")


def _build_address(
    line1: str,
    *,
    city: str = "Austin",
    country_code: str = "USA",
    country_name: str = "United States of America",
    region_id: str = "TX",
    region_name: str = "Texas",
    postal_code: str = "78704",
) -> dict[str, Any]:
    return {
        "addressType": 3,
        "city": city,
        "countryCode": country_code,
        "countryName": country_name,
        "line1": line1,
        "postalCode": postal_code,
        "regionId": region_id,
        "regionName": region_name,
    }


def _seed_contact_addresses(
    contact_operations: ContactOperations,
    member_id: str,
    addresses: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Seed addresses onto a member (contact or organization) and return the
    persisted representations matched by line1 (which we make unique per test)."""
    result = contact_operations.update_contact_addresses(payload={"memberId": member_id, "addresses": addresses})
    seeded_line1 = {addr["line1"] for addr in addresses}
    return [item for item in result["addresses"]["items"] if item["line1"] in seeded_line1]


def _safe_delete_addresses(
    contact_operations: ContactOperations,
    member_id: str,
    addresses: list[dict[str, Any]],
) -> None:
    for address in addresses:
        try:
            contact_operations.delete_contact_address(payload={"memberId": member_id, "addresses": [address]})
        except Exception as exc:
            logger.warning("Cleanup failed for address %s on member %s: %s", address.get("line1"), member_id, exc)


@pytest.mark.graphql
@allure.title("currentCustomerAddresses returns the contact address list (GraphQL)")
def test_current_customer_addresses_returns_list(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
) -> None:
    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"])
    contact_id = user_operations.get_me()["contact"]["id"]

    seeded: list[dict[str, Any]] = []
    try:
        line1 = f"addr-A1-{uuid.uuid4().hex[:8]}"
        seeded = _seed_contact_addresses(contact_operations, contact_id, [_build_address(line1)])

        result = contact_operations.fetch_current_customer_addresses()

        assert result["totalCount"] >= 1, "Expected at least one address"
        assert any(
            item["line1"] == line1 for item in result["items"]
        ), "Seeded address not returned by currentCustomerAddresses"
    finally:
        _safe_delete_addresses(contact_operations, contact_id, seeded)
        auth.clear_token()


@pytest.mark.graphql
@allure.title("currentCustomerAddresses first argument limits page size (GraphQL)")
def test_current_customer_addresses_first_limits_page_size(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
) -> None:
    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"])
    contact_id = user_operations.get_me()["contact"]["id"]

    seeded: list[dict[str, Any]] = []
    try:
        line1_a = f"addr-A2-A-{uuid.uuid4().hex[:8]}"
        line1_b = f"addr-A2-B-{uuid.uuid4().hex[:8]}"
        seeded = _seed_contact_addresses(
            contact_operations,
            contact_id,
            [_build_address(line1_a), _build_address(line1_b)],
        )

        result = contact_operations.fetch_current_customer_addresses(first=1)

        assert len(result["items"]) == 1, "Expected exactly one item when first=1"
    finally:
        _safe_delete_addresses(contact_operations, contact_id, seeded)
        auth.clear_token()


@pytest.mark.graphql
@allure.title("currentCustomerAddresses after cursor paginates (GraphQL)")
@pytest.mark.xfail(
    reason="VCST-5001: currentCustomerAddresses 'after' cursor semantics differ from "
    "integer index; second page returns empty with after='1'. Confirm opaque cursor "
    "format with backend.",
    strict=True,
)
def test_current_customer_addresses_after_paginates(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
) -> None:
    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"])
    contact_id = user_operations.get_me()["contact"]["id"]

    seeded: list[dict[str, Any]] = []
    try:
        line1_a = f"addr-A3-A-{uuid.uuid4().hex[:8]}"
        line1_b = f"addr-A3-B-{uuid.uuid4().hex[:8]}"
        seeded = _seed_contact_addresses(
            contact_operations,
            contact_id,
            [_build_address(line1_a), _build_address(line1_b)],
        )

        page_one = contact_operations.fetch_current_customer_addresses(after="0", first=1)
        page_two = contact_operations.fetch_current_customer_addresses(after="1", first=1)

        assert len(page_one["items"]) == 1, "First page should contain 1 item"
        assert len(page_two["items"]) == 1, "Second page should contain 1 item"
        assert page_one["items"][0]["id"] != page_two["items"][0]["id"], "Pagination returned the same item twice"
    finally:
        _safe_delete_addresses(contact_operations, contact_id, seeded)
        auth.clear_token()


@pytest.mark.graphql
@allure.title("currentCustomerAddresses filters by countryCodes (GraphQL)")
@pytest.mark.xfail(
    reason="VCST-5001: currentCustomerAddresses countryCodes filter returns empty for "
    "freshly seeded contact addresses on vcptcore-demo. Confirm filter semantics / "
    "index refresh delay with backend.",
    strict=True,
)
def test_current_customer_addresses_filter_by_country_code(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
) -> None:
    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"])
    contact_id = user_operations.get_me()["contact"]["id"]

    seeded: list[dict[str, Any]] = []
    try:
        usa_line1 = f"addr-A4-USA-{uuid.uuid4().hex[:8]}"
        gbr_line1 = f"addr-A4-GBR-{uuid.uuid4().hex[:8]}"
        seeded = _seed_contact_addresses(
            contact_operations,
            contact_id,
            [
                _build_address(usa_line1),
                _build_address(
                    gbr_line1,
                    city="London",
                    country_code="GBR",
                    country_name="United Kingdom",
                    region_id="ENG",
                    region_name="England",
                    postal_code="SW1A 1AA",
                ),
            ],
        )

        result = contact_operations.fetch_current_customer_addresses(country_codes=["USA"])

        assert len(result["items"]) >= 1, "Expected at least one USA address"
        assert all(item["countryCode"] == "USA" for item in result["items"]), "Filter returned non-USA addresses"
        assert not any(item["line1"] == gbr_line1 for item in result["items"]), "Filter leaked the GBR address"
    finally:
        _safe_delete_addresses(contact_operations, contact_id, seeded)
        auth.clear_token()


@pytest.mark.graphql
@allure.title("currentCustomerAddresses filters by regionIds (GraphQL)")
@pytest.mark.xfail(
    reason="VCST-5001: currentCustomerAddresses regionIds filter returns empty for "
    "regionId values like 'TX'. Confirm expected regionId format with backend.",
    strict=True,
)
def test_current_customer_addresses_filter_by_region_id(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
) -> None:
    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"])
    contact_id = user_operations.get_me()["contact"]["id"]

    seeded: list[dict[str, Any]] = []
    try:
        tx_line1 = f"addr-A5-TX-{uuid.uuid4().hex[:8]}"
        ca_line1 = f"addr-A5-CA-{uuid.uuid4().hex[:8]}"
        seeded = _seed_contact_addresses(
            contact_operations,
            contact_id,
            [
                _build_address(tx_line1),
                _build_address(
                    ca_line1,
                    city="Los Angeles",
                    region_id="CA",
                    region_name="California",
                    postal_code="90001",
                ),
            ],
        )

        result = contact_operations.fetch_current_customer_addresses(region_ids=["TX"])

        assert len(result["items"]) >= 1, "Expected at least one TX address"
        assert all(item["regionId"] == "TX" for item in result["items"]), "Filter returned non-TX addresses"
        assert not any(item["line1"] == ca_line1 for item in result["items"]), "Filter leaked the CA address"
    finally:
        _safe_delete_addresses(contact_operations, contact_id, seeded)
        auth.clear_token()


@pytest.mark.graphql
@allure.title("currentCustomerAddresses filters by cities (GraphQL)")
@pytest.mark.xfail(
    reason="VCST-5001: currentCustomerAddresses cities filter returns empty for exact "
    "city values like 'Austin'. Confirm case-sensitivity / match semantics with backend.",
    strict=True,
)
def test_current_customer_addresses_filter_by_city(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
) -> None:
    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"])
    contact_id = user_operations.get_me()["contact"]["id"]

    seeded: list[dict[str, Any]] = []
    try:
        austin_line1 = f"addr-A6-AUS-{uuid.uuid4().hex[:8]}"
        dallas_line1 = f"addr-A6-DAL-{uuid.uuid4().hex[:8]}"
        seeded = _seed_contact_addresses(
            contact_operations,
            contact_id,
            [
                _build_address(austin_line1, city="Austin"),
                _build_address(dallas_line1, city="Dallas", postal_code="75201"),
            ],
        )

        result = contact_operations.fetch_current_customer_addresses(cities=["Austin"])

        assert len(result["items"]) >= 1, "Expected at least one Austin address"
        assert all(item["city"] == "Austin" for item in result["items"]), "Filter returned non-Austin addresses"
        assert not any(item["line1"] == dallas_line1 for item in result["items"]), "Filter leaked the Dallas address"
    finally:
        _safe_delete_addresses(contact_operations, contact_id, seeded)
        auth.clear_token()


@pytest.mark.graphql
@allure.title("currentCustomerAddresses keyword matches address tokens (GraphQL)")
def test_current_customer_addresses_keyword_matches(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
) -> None:
    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"])
    contact_id = user_operations.get_me()["contact"]["id"]

    seeded: list[dict[str, Any]] = []
    try:
        unique_token = f"kw-a7-{uuid.uuid4().hex[:8]}"
        line1 = f"addr-A7-{unique_token}"
        seeded = _seed_contact_addresses(
            contact_operations,
            contact_id,
            [_build_address(line1, city=f"City{unique_token}")],
        )

        result = contact_operations.fetch_current_customer_addresses(keyword=unique_token)

        assert result["items"], "Expected keyword to match seeded address"
        assert any(
            item["line1"] == line1 for item in result["items"]
        ), "Keyword search did not return the seeded address"
    finally:
        _safe_delete_addresses(contact_operations, contact_id, seeded)
        auth.clear_token()


@pytest.mark.graphql
@allure.title("currentCustomerAddresses sort by city ascending (GraphQL)")
def test_current_customer_addresses_sort_by_city_asc(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
) -> None:
    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"])
    contact_id = user_operations.get_me()["contact"]["id"]

    seeded: list[dict[str, Any]] = []
    try:
        suffix = uuid.uuid4().hex[:6]
        # Insertion order is intentionally non-ascending (Zephyr, Aurora, Maple) so a
        # backend that ignored `sort` would return them in insertion order and fail.
        cities = [
            (f"Zephyr-{suffix}", f"addr-A8-Z-{suffix}"),
            (f"Aurora-{suffix}", f"addr-A8-A-{suffix}"),
            (f"Maple-{suffix}", f"addr-A8-M-{suffix}"),
        ]
        seeded = _seed_contact_addresses(
            contact_operations,
            contact_id,
            [_build_address(line1, city=city) for city, line1 in cities],
        )

        result = contact_operations.fetch_current_customer_addresses(sort="city:asc")

        seeded_cities = {city for city, _ in cities}
        returned = [item["city"] for item in result["items"] if item["city"] in seeded_cities]

        assert returned == sorted(returned), f"Expected ascending order, got {returned}"
    finally:
        _safe_delete_addresses(contact_operations, contact_id, seeded)
        auth.clear_token()


@pytest.mark.graphql
@allure.title("currentCustomerAddresses unauthorized for anonymous caller (GraphQL)")
def test_current_customer_addresses_anonymous_is_unauthorized(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
) -> None:
    contact_operations = ContactOperations(graphql_client)

    # Intentionally NOT calling auth.authenticate — caller is anonymous.
    # Accept either an auth-flavoured GraphQL error or an empty connection;
    # reject any other failure mode (e.g. a 500 or an unrelated exception).
    try:
        result = contact_operations.fetch_current_customer_addresses()
    except Exception as exc:
        message = str(exc).lower()
        assert any(token in message for token in _AUTH_ERROR_TOKENS), f"Expected an auth-related error, got: {exc!r}"
        return

    assert not result.get("items"), "Anonymous caller should not receive any customer addresses"


@pytest.mark.graphql
@allure.title("currentCustomerAddresses returns contact-scoped, not organization-scoped, addresses (GraphQL)")
def test_current_customer_addresses_returns_contact_not_org_addresses(
    config: Config,
    dataset: dict[str, Any],
    auth: Auth,
    graphql_client: GraphQLClient,
) -> None:
    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(dataset["users"][0]["userName"], config["USERS_PASSWORD"])
    user = user_operations.get_me()
    contact_id = user["contact"]["id"]
    organization_id = user["contact"]["organizationId"]

    seeded_contact: list[dict[str, Any]] = []
    seeded_org: list[dict[str, Any]] = []
    try:
        contact_line1 = f"addr-B11-CONTACT-{uuid.uuid4().hex[:8]}"
        org_line1 = f"addr-B11-ORG-{uuid.uuid4().hex[:8]}"

        seeded_contact = _seed_contact_addresses(contact_operations, contact_id, [_build_address(contact_line1)])
        seeded_org = _seed_contact_addresses(contact_operations, organization_id, [_build_address(org_line1)])

        result = contact_operations.fetch_current_customer_addresses()

        line1s = [item["line1"] for item in result["items"]]
        assert contact_line1 in line1s, "Contact-scoped address missing from currentCustomerAddresses"
        assert org_line1 not in line1s, "Organization-scoped address leaked into currentCustomerAddresses"
    finally:
        _safe_delete_addresses(contact_operations, contact_id, seeded_contact)
        _safe_delete_addresses(contact_operations, organization_id, seeded_org)
        auth.clear_token()
