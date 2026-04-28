import pytest
from core.clients import GraphQLClient
from gql.operations import PickupLocationOperations
from tests.context import Context

_PRODUCT_ALL_TYPES = "product-acme-product2-main1-stock"
_PRODUCT_TODAY = "product-acme-product2-main2-stock"
_PRODUCT_MULTIPLE_FFC = "product-acme-product4-main-transfer"
_PRODUCT_NO_TRACK_INVENTORY = "product-acme-product1-track-inventory-false"
_PRODUCT_BERLIN_BILLUND = "product-acme-product7-berlin"
_PRODUCT_MULTIPLE_FFCS = "product-acme-product5-transfer123"

_AVAILABILITY_TODAY = "Today"
_AVAILABILITY_TRANSFER = "Transfer"
_ADDRESS_FIELDS = ("city", "country_name", "line1")


def _get_locations(ops: PickupLocationOperations, product_id: str, ctx: Context):
    return ops.get_product_pickup_locations(
        product_id=product_id,
        store_id=ctx.store_id,
        culture_name=ctx.culture_name,
    )


def _assert_addresses(locations) -> None:
    assert all(loc.address is not None for loc in locations)
    assert all(
        getattr(loc.address, field) for loc in locations for field in _ADDRESS_FIELDS
    )


@pytest.mark.graphql
@pytest.mark.skip
def test_product_pickup_locations_all_types(
    graphql_client: GraphQLClient, ctx: Context
) -> None:
    ops = PickupLocationOperations(client=graphql_client)
    locations = _get_locations(ops, _PRODUCT_ALL_TYPES, ctx)

    assert len(locations) > 0
    _assert_addresses(locations)

    found_types = {loc.availability_type for loc in locations}
    assert {_AVAILABILITY_TODAY, _AVAILABILITY_TRANSFER} == found_types


@pytest.mark.graphql
@pytest.mark.skip
def test_product_pickup_locations_today(
    graphql_client: GraphQLClient, ctx: Context
) -> None:
    ops = PickupLocationOperations(client=graphql_client)
    locations = _get_locations(ops, _PRODUCT_TODAY, ctx)

    today_locations = [
        loc for loc in locations if loc.availability_type == _AVAILABILITY_TODAY
    ]
    assert len(today_locations) > 0
    assert all(
        loc.available_quantity is not None and loc.available_quantity > 0
        for loc in today_locations
    )
    _assert_addresses(locations)


@pytest.mark.graphql
@pytest.mark.skip
def test_product_pickup_locations_multiple_ffc(
    graphql_client: GraphQLClient, ctx: Context
) -> None:
    ops = PickupLocationOperations(client=graphql_client)
    locations = _get_locations(ops, _PRODUCT_MULTIPLE_FFC, ctx)

    assert len(locations) > 0
    _assert_addresses(locations)

    transfer_locations = [
        loc for loc in locations if loc.availability_type == _AVAILABILITY_TRANSFER
    ]
    cities = {loc.address.city for loc in transfer_locations if loc.address}
    assert len(cities) > 1


@pytest.mark.graphql
@pytest.mark.skip
def test_product_pickup_locations_no_track_inventory(
    graphql_client: GraphQLClient, ctx: Context
) -> None:
    ops = PickupLocationOperations(client=graphql_client)
    locations = _get_locations(ops, _PRODUCT_NO_TRACK_INVENTORY, ctx)

    assert len(locations) > 0
    assert all(loc.availability_type == _AVAILABILITY_TODAY for loc in locations)
    assert all(loc.available_quantity is None for loc in locations)
    _assert_addresses(locations)


@pytest.mark.graphql
@pytest.mark.skip
def test_product_pickup_locations_defined_ffc_berlin_billund(
    graphql_client: GraphQLClient, ctx: Context
) -> None:
    ops = PickupLocationOperations(client=graphql_client)
    locations = _get_locations(ops, _PRODUCT_BERLIN_BILLUND, ctx)

    assert len(locations) > 0
    assert all(loc.availability_type == _AVAILABILITY_TRANSFER for loc in locations)
    _assert_addresses(locations)

    cities = {loc.address.city for loc in locations if loc.address}
    assert "Berlin" in cities
    assert "Billund" in cities


@pytest.mark.graphql
@pytest.mark.skip
def test_product_pickup_locations_multiple_ffcs(
    graphql_client: GraphQLClient, ctx: Context
) -> None:
    ops = PickupLocationOperations(client=graphql_client)
    locations = _get_locations(ops, _PRODUCT_MULTIPLE_FFCS, ctx)

    assert len(locations) > 0
    _assert_addresses(locations)

    transfer_locations = [
        loc for loc in locations if loc.availability_type == _AVAILABILITY_TRANSFER
    ]
    assert len(transfer_locations) > 0

    ffc_cities = {loc.address.city for loc in transfer_locations if loc.address}
    assert len(ffc_cities) > 2


@pytest.mark.graphql
@pytest.mark.skip
def test_product_pickup_locations_all_availability_types(
    graphql_client: GraphQLClient, ctx: Context
) -> None:
    ops = PickupLocationOperations(client=graphql_client)
    locations = _get_locations(ops, _PRODUCT_MULTIPLE_FFC, ctx)

    assert len(locations) > 0
    assert all(loc.availability_type is not None for loc in locations)
    assert all(loc.available_quantity is not None for loc in locations)
    _assert_addresses(locations)

    found_types = {loc.availability_type for loc in locations}
    assert {_AVAILABILITY_TODAY, _AVAILABILITY_TRANSFER} == found_types
