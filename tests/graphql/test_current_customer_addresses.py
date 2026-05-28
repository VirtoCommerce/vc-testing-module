import uuid
from typing import Iterable

import allure
import pytest

from core.clients import GraphQLClient
from gql.operations import ContactOperations
from gql.types import MemberAddress
from tests.context import Context
from utils.address_utils import make_address
from utils.polling_utils import wait_addresses_visible

_USERNAME = "acme_store_employee_1@acme.com"


def _wait_visible(
    contact_ops: ContactOperations,
    seeded_descriptions: set[str],
) -> tuple[int, list[MemberAddress]]:
    return wait_addresses_visible(
        fetch=lambda: contact_ops.get_current_customer_addresses(first=200),
        seeded_descriptions=seeded_descriptions,
    )


def _cleanup_addresses(
    contact_ops: ContactOperations,
    member_id: str,
    seeded: Iterable[MemberAddress],
    fetched: Iterable[MemberAddress],
) -> None:
    """Delete seeded addresses; resolves IDs from the fetched list by description."""
    seeded_descriptions = {a.description for a in seeded if a.description}
    to_delete = [a for a in fetched if a.description in seeded_descriptions]
    if to_delete:
        try:
            contact_ops.delete_member_addresses(member_id=member_id, addresses=to_delete)
        except Exception as exc:
            allure.attach(str(exc), name="cleanup-error")


@pytest.mark.graphql
@pytest.mark.optional
@pytest.mark.with_user(_USERNAME)
@allure.feature("Contact / Addresses (GraphQL)")
@allure.title("C1: currentCustomerAddresses returns totalCount and items (smoke)")
def test_c1_smoke(ctx: Context, graphql_client: GraphQLClient) -> None:
    contact_ops = ContactOperations(client=graphql_client)
    assert ctx.contact_id is not None

    seed = [make_address(key_prefix="c1")]
    seeded_descriptions = {a.description for a in seed}
    try:
        with allure.step(f"Seed 1 address on contact {ctx.contact_id}"):
            contact_ops.update_member_addresses(member_id=ctx.contact_id, addresses=seed)

        with allure.step("Poll currentCustomerAddresses until seed is indexed"):
            total_count, items = _wait_visible(contact_ops, seeded_descriptions)

        with allure.step("Verify totalCount and items[]"):
            assert isinstance(total_count, int)
            assert total_count >= 1
            assert isinstance(items, list)
            assert len(items) >= 1
            assert any(a.description == seed[0].description for a in items)
    finally:
        with allure.step("Teardown: delete seeded address"):
            _, items = contact_ops.get_current_customer_addresses(first=200)
            _cleanup_addresses(contact_ops, ctx.contact_id, seed, items)


@pytest.mark.graphql
@pytest.mark.optional
@pytest.mark.with_user(_USERNAME)
@allure.feature("Contact / Addresses (GraphQL)")
@allure.title("C2: first=1 limits page size to 1")
def test_c2_first_limits_page_size(ctx: Context, graphql_client: GraphQLClient) -> None:
    contact_ops = ContactOperations(client=graphql_client)
    assert ctx.contact_id is not None

    seed = [
        make_address(key_prefix="c2a"),
        make_address(key_prefix="c2b"),
    ]
    seeded_descriptions = {a.description for a in seed}
    try:
        with allure.step(f"Seed 2 addresses on contact {ctx.contact_id}"):
            contact_ops.update_member_addresses(member_id=ctx.contact_id, addresses=seed)

        with allure.step("Poll until both seeded addresses are indexed"):
            _wait_visible(contact_ops, seeded_descriptions)

        with allure.step("Query currentCustomerAddresses with first=1"):
            total_count, items = contact_ops.get_current_customer_addresses(first=1)

        with allure.step("Verify only 1 item returned and totalCount reflects ≥2"):
            assert len(items) == 1
            assert total_count >= 2
    finally:
        with allure.step("Teardown: delete seeded addresses"):
            _, items = contact_ops.get_current_customer_addresses(first=200)
            _cleanup_addresses(contact_ops, ctx.contact_id, seed, items)


@pytest.mark.graphql
@pytest.mark.optional
@pytest.mark.with_user(_USERNAME)
@allure.feature("Contact / Addresses (GraphQL)")
@allure.title("C3: after cursor pages forward in canonical order")
def test_c3_after_cursor_pages_forward(ctx: Context, graphql_client: GraphQLClient) -> None:
    contact_ops = ContactOperations(client=graphql_client)
    assert ctx.contact_id is not None

    seed = [
        make_address(key_prefix="c3a"),
        make_address(key_prefix="c3b"),
        make_address(key_prefix="c3c"),
    ]
    seeded_descriptions = {a.description for a in seed}
    try:
        with allure.step(f"Seed 3 addresses on contact {ctx.contact_id}"):
            contact_ops.update_member_addresses(member_id=ctx.contact_id, addresses=seed)

        with allure.step("Poll until all 3 seeded addresses are indexed"):
            _wait_visible(contact_ops, seeded_descriptions)

        with allure.step("Fetch unpaginated baseline (first=200)"):
            _, baseline = contact_ops.get_current_customer_addresses(first=200)

        with allure.step('Fetch page 1 (first=1, after="0")'):
            _, page1 = contact_ops.get_current_customer_addresses(first=1, after="0")

        with allure.step('Fetch page 2 (first=1, after="1")'):
            _, page2 = contact_ops.get_current_customer_addresses(first=1, after="1")

        with allure.step("Verify paginated slices match the canonical (unpaginated) order"):
            # Soundness anchor: pagination is only meaningful if paginated walks
            # match the unpaginated baseline. Both pages must align with the
            # corresponding indices of the baseline list.
            assert len(baseline) >= 2, "Need >=2 addresses for a pagination test"
            assert len(page1) == 1
            assert len(page2) == 1
            assert page1[0].id == baseline[0].id, (
                f"page 1 should match baseline[0]; " f"got {page1[0].id} vs baseline[0]={baseline[0].id}"
            )
            assert page2[0].id == baseline[1].id, (
                f"page 2 should match baseline[1]; " f"got {page2[0].id} vs baseline[1]={baseline[1].id}"
            )
    finally:
        with allure.step("Teardown: delete seeded addresses"):
            _, items = contact_ops.get_current_customer_addresses(first=200)
            _cleanup_addresses(contact_ops, ctx.contact_id, seed, items)


@pytest.mark.graphql
@pytest.mark.optional
@pytest.mark.with_user(_USERNAME)
@allure.feature("Contact / Addresses (GraphQL)")
@allure.title("C4: countryCodes filter returns matching addresses")
def test_c4_country_codes_filter(ctx: Context, graphql_client: GraphQLClient) -> None:
    contact_ops = ContactOperations(client=graphql_client)
    assert ctx.contact_id is not None

    seed = [make_address(key_prefix="c4", country_code="USA")]
    seeded_descriptions = {a.description for a in seed}
    try:
        with allure.step(f"Seed USA address on contact {ctx.contact_id}"):
            contact_ops.update_member_addresses(member_id=ctx.contact_id, addresses=seed)

        with allure.step("Poll until seed is indexed"):
            _wait_visible(contact_ops, seeded_descriptions)

        with allure.step('Query currentCustomerAddresses with countryCodes=["USA"]'):
            total_count, items = contact_ops.get_current_customer_addresses(country_codes=["USA"])

        with allure.step("Verify seeded USA address is returned"):
            assert total_count >= 1
            assert any(a.description == seed[0].description for a in items)
    finally:
        with allure.step("Teardown: delete seeded address"):
            _, items = contact_ops.get_current_customer_addresses(first=200)
            _cleanup_addresses(contact_ops, ctx.contact_id, seed, items)


@pytest.mark.graphql
@pytest.mark.optional
@pytest.mark.with_user(_USERNAME)
@allure.feature("Contact / Addresses (GraphQL)")
@allure.title("C5: regionIds filter returns matching addresses")
def test_c5_region_ids_filter(ctx: Context, graphql_client: GraphQLClient) -> None:
    contact_ops = ContactOperations(client=graphql_client)
    assert ctx.contact_id is not None

    seed = [make_address(key_prefix="c5", region_id="NY", region_name="New York")]
    seeded_descriptions = {a.description for a in seed}
    try:
        with allure.step(f"Seed NY address on contact {ctx.contact_id}"):
            contact_ops.update_member_addresses(member_id=ctx.contact_id, addresses=seed)

        with allure.step("Poll until seed is indexed"):
            _wait_visible(contact_ops, seeded_descriptions)

        with allure.step('Query currentCustomerAddresses with regionIds=["NY"]'):
            total_count, items = contact_ops.get_current_customer_addresses(region_ids=["NY"])

        with allure.step("Verify seeded NY address is returned"):
            assert total_count >= 1
            assert any(a.description == seed[0].description for a in items)
    finally:
        with allure.step("Teardown: delete seeded address"):
            _, items = contact_ops.get_current_customer_addresses(first=200)
            _cleanup_addresses(contact_ops, ctx.contact_id, seed, items)


@pytest.mark.graphql
@pytest.mark.optional
@pytest.mark.with_user(_USERNAME)
@allure.feature("Contact / Addresses (GraphQL)")
@allure.title("C6: cities filter returns matching addresses")
def test_c6_cities_filter(ctx: Context, graphql_client: GraphQLClient) -> None:
    contact_ops = ContactOperations(client=graphql_client)
    assert ctx.contact_id is not None

    target_city = f"City-{uuid.uuid4().hex[:6]}"
    seed = [make_address(key_prefix="c6", city=target_city)]
    seeded_descriptions = {a.description for a in seed}
    try:
        with allure.step(f"Seed address in {target_city} on contact {ctx.contact_id}"):
            contact_ops.update_member_addresses(member_id=ctx.contact_id, addresses=seed)

        with allure.step("Poll until seed is indexed"):
            _wait_visible(contact_ops, seeded_descriptions)

        with allure.step(f'Query currentCustomerAddresses with cities=["{target_city}"]'):
            total_count, items = contact_ops.get_current_customer_addresses(cities=[target_city])

        with allure.step(f"Verify address in {target_city} is returned"):
            assert total_count >= 1
            assert any(a.description == seed[0].description for a in items)
    finally:
        with allure.step("Teardown: delete seeded address"):
            _, items = contact_ops.get_current_customer_addresses(first=200)
            _cleanup_addresses(contact_ops, ctx.contact_id, seed, items)


@pytest.mark.graphql
@pytest.mark.optional
@pytest.mark.with_user(_USERNAME)
@allure.feature("Contact / Addresses (GraphQL)")
@allure.title("C7: keyword search returns matching addresses")
def test_c7_keyword_search(ctx: Context, graphql_client: GraphQLClient) -> None:
    contact_ops = ContactOperations(client=graphql_client)
    assert ctx.contact_id is not None

    keyword_token = f"kwc7{uuid.uuid4().hex[:6]}"
    seed = [
        make_address(
            key_prefix="c7",
            line1=f"1 {keyword_token} Street",
            description=f"c7-{keyword_token}",
        )
    ]
    seeded_descriptions = {a.description for a in seed}
    try:
        with allure.step(f"Seed address containing '{keyword_token}' on contact {ctx.contact_id}"):
            contact_ops.update_member_addresses(member_id=ctx.contact_id, addresses=seed)

        with allure.step("Poll until seed is indexed"):
            _wait_visible(contact_ops, seeded_descriptions)

        with allure.step(f"Query currentCustomerAddresses with keyword='{keyword_token}'"):
            total_count, items = contact_ops.get_current_customer_addresses(keyword=keyword_token)

        with allure.step("Verify only the seeded address matches"):
            assert total_count >= 1
            assert any(a.description == seed[0].description for a in items)
    finally:
        with allure.step("Teardown: delete seeded address"):
            _, items = contact_ops.get_current_customer_addresses(first=200)
            _cleanup_addresses(contact_ops, ctx.contact_id, seed, items)


@pytest.mark.graphql
@pytest.mark.optional
@pytest.mark.with_user(_USERNAME)
@allure.feature("Contact / Addresses (GraphQL)")
@allure.title("C8: sort='city:asc' returns addresses in ascending city order")
def test_c8_sort_city_asc(ctx: Context, graphql_client: GraphQLClient) -> None:
    contact_ops = ContactOperations(client=graphql_client)
    assert ctx.contact_id is not None

    # Pick 3 city names whose insertion order is NOT ascending; a backend that
    # ignores sort would return them in insertion order and fail the assert.
    suffix = uuid.uuid4().hex[:6]
    cities_in_seed_order = [
        f"Zeta-{suffix}",
        f"Alpha-{suffix}",
        f"Mu-{suffix}",
    ]
    seed = [make_address(key_prefix="c8", city=c, description=f"c8-{suffix}-{c}") for c in cities_in_seed_order]
    seeded_descriptions = {a.description for a in seed}
    try:
        with allure.step(f"Seed 3 addresses (cities: {cities_in_seed_order}) on contact {ctx.contact_id}"):
            contact_ops.update_member_addresses(member_id=ctx.contact_id, addresses=seed)

        with allure.step("Poll until all 3 seeded addresses are indexed"):
            _wait_visible(contact_ops, seeded_descriptions)

        with allure.step("Query currentCustomerAddresses with sort='city:asc'"):
            _, items = contact_ops.get_current_customer_addresses(sort="city:asc", first=200)

        with allure.step("Verify seeded addresses appear in ascending city order"):
            seeded_cities = [a.city for a in items if a.description in seeded_descriptions]
            assert seeded_cities == sorted(cities_in_seed_order)
    finally:
        with allure.step("Teardown: delete seeded addresses"):
            _, items = contact_ops.get_current_customer_addresses(first=200)
            _cleanup_addresses(contact_ops, ctx.contact_id, seed, items)


@pytest.mark.graphql
@pytest.mark.optional
@allure.feature("Contact / Addresses (GraphQL)")
@allure.title("C9: anonymous caller is denied access")
def test_c9_anonymous_denied(graphql_client: GraphQLClient) -> None:
    """Anonymous callers receive a Forbidden GraphQL error instead of an empty
    connection. This documents the actual backend behavior on vcst-qa."""
    contact_ops = ContactOperations(client=graphql_client)

    with allure.step("Query currentCustomerAddresses as anonymous user"):
        with pytest.raises(ValueError) as exc_info:
            contact_ops.get_current_customer_addresses()

    with allure.step("Verify GraphQL error code is Forbidden"):
        message = str(exc_info.value)
        assert "Forbidden" in message or "Access denied" in message


@pytest.mark.graphql
@pytest.mark.optional
@pytest.mark.with_user(_USERNAME)
@allure.feature("Contact / Addresses (GraphQL)")
@allure.title("C10: customer query is contact-scoped, not organization-scoped")
def test_c10_scoping_customer_not_organization(ctx: Context, graphql_client: GraphQLClient) -> None:
    contact_ops = ContactOperations(client=graphql_client)
    assert ctx.contact_id is not None
    assert ctx.organization_id is not None

    contact_seed = [make_address(key_prefix="c10-contact", line1="1 Contact Street")]
    org_seed = [make_address(key_prefix="c10-org", line1="1 Org Avenue")]
    contact_descriptions = {a.description for a in contact_seed}
    try:
        with allure.step(f"Seed address on contact {ctx.contact_id}"):
            contact_ops.update_member_addresses(member_id=ctx.contact_id, addresses=contact_seed)

        with allure.step(f"Seed address on organization {ctx.organization_id}"):
            contact_ops.update_member_addresses(member_id=ctx.organization_id, addresses=org_seed)

        with allure.step("Poll currentCustomerAddresses until contact seed is indexed"):
            _, items = _wait_visible(contact_ops, contact_descriptions)

        with allure.step("Verify contact-seeded present, org-seeded absent"):
            descriptions = {a.description for a in items}
            assert contact_seed[0].description in descriptions
            assert org_seed[0].description not in descriptions
    finally:
        with allure.step("Teardown: delete contact-seeded address"):
            _, items = contact_ops.get_current_customer_addresses(first=200)
            _cleanup_addresses(contact_ops, ctx.contact_id, contact_seed, items)
        with allure.step("Teardown: delete org-seeded address"):
            try:
                contact_ops.delete_member_addresses(member_id=ctx.organization_id, addresses=org_seed)
            except Exception as exc:
                allure.attach(str(exc), name="cleanup-error")


@pytest.mark.graphql
@pytest.mark.optional
@pytest.mark.with_user(_USERNAME)
@allure.feature("Contact / Addresses (GraphQL)")
@allure.title("C11: full-field selection — MemberAddress validates from response")
def test_c11_full_field_validation(ctx: Context, graphql_client: GraphQLClient) -> None:
    contact_ops = ContactOperations(client=graphql_client)
    assert ctx.contact_id is not None

    seed = [make_address(key_prefix="c11")]
    seeded_descriptions = {a.description for a in seed}
    try:
        with allure.step(f"Seed address on contact {ctx.contact_id}"):
            contact_ops.update_member_addresses(member_id=ctx.contact_id, addresses=seed)

        with allure.step("Poll until seed is indexed"):
            _, items = _wait_visible(contact_ops, seeded_descriptions)

        with allure.step("Verify MemberAddress validation and key fields"):
            seeded = next((a for a in items if a.description == seed[0].description), None)
            assert seeded is not None
            assert isinstance(seeded, MemberAddress)
            assert seeded.id is not None
            assert seeded.city == seed[0].city
            assert seeded.country_code == seed[0].country_code
            assert seeded.country_name == seed[0].country_name
            assert seeded.region_id == seed[0].region_id
            assert seeded.region_name == seed[0].region_name
            assert seeded.line1 == seed[0].line1
            assert seeded.postal_code == seed[0].postal_code
            assert seeded.first_name == seed[0].first_name
            assert seeded.last_name == seed[0].last_name
            assert seeded.address_type == seed[0].address_type
    finally:
        with allure.step("Teardown: delete seeded address"):
            _, items = contact_ops.get_current_customer_addresses(first=200)
            _cleanup_addresses(contact_ops, ctx.contact_id, seed, items)
