import pytest
from core.clients import GraphQLClient
from core.global_settings import GlobalSettings
from gql.operations import PickupLocationOperations
from gql.types import Cart
from tests.context import Context

_TRANSFER_PRODUCT_ID = "product-acme-product5-transfer-b2b"
_IN_STOCK_PRODUCT_ID = "product-acme-product2-main1-stock"
_MULTIREGION_PRODUCT_ID = "product-acme-product4-main-transfer"
_TRANSFER_TYPE = "Transfer"
_GLOBAL_TRANSFER_TYPE = "GlobalTransfer"
_TODAY_TYPE = "Today"


@pytest.mark.graphql
@pytest.mark.skip
@pytest.mark.with_cart([(_TRANSFER_PRODUCT_ID, 1)])
def test_cart_pickup_locations_product_transfer(
    graphql_client: GraphQLClient,
    ctx: Context,
    with_cart: Cart,
    global_settings: GlobalSettings,
) -> None:
    pickup_location_ops = PickupLocationOperations(client=graphql_client)

    locations = pickup_location_ops.get_cart_pickup_locations(
        cart_id=with_cart.id,
        store_id=ctx.store_id,
        culture_name=ctx.culture_name,
        first=global_settings.default_page_size,
    )

    assert len(locations) > 0
    assert all(
        loc.availability_type in [_TRANSFER_TYPE, _GLOBAL_TRANSFER_TYPE]
        for loc in locations
    )


@pytest.mark.graphql
@pytest.mark.skip
@pytest.mark.with_cart([(_IN_STOCK_PRODUCT_ID, 1)])
def test_cart_pickup_locations_product_is_stock(
    graphql_client: GraphQLClient,
    ctx: Context,
    with_cart: Cart,
    global_settings: GlobalSettings,
) -> None:
    pickup_location_ops = PickupLocationOperations(client=graphql_client)

    locations = pickup_location_ops.get_cart_pickup_locations(
        cart_id=with_cart.id,
        store_id=ctx.store_id,
        culture_name=ctx.culture_name,
        first=global_settings.default_page_size,
    )

    assert len(locations) > 0
    assert any(loc.availability_type == _TODAY_TYPE for loc in locations)

    first_transfer_idx = next(
        (i for i, loc in enumerate(locations) if loc.availability_type != _TODAY_TYPE),
        len(locations),
    )
    assert all(
        loc.availability_type == _TODAY_TYPE for loc in locations[:first_transfer_idx]
    )
    assert all(
        loc.availability_type != _TODAY_TYPE for loc in locations[first_transfer_idx:]
    )


@pytest.mark.graphql
@pytest.mark.skip
@pytest.mark.with_cart([(_TRANSFER_PRODUCT_ID, 1), (_IN_STOCK_PRODUCT_ID, 1)])
def test_cart_pickup_locations_products_mixed(
    graphql_client: GraphQLClient,
    ctx: Context,
    with_cart: Cart,
    global_settings: GlobalSettings,
) -> None:
    pickup_location_ops = PickupLocationOperations(client=graphql_client)

    locations = pickup_location_ops.get_cart_pickup_locations(
        cart_id=with_cart.id,
        store_id=ctx.store_id,
        culture_name=ctx.culture_name,
        first=global_settings.default_page_size,
    )

    assert len(locations) > 0
    assert all(
        loc.availability_type in [_TRANSFER_TYPE, _GLOBAL_TRANSFER_TYPE]
        for loc in locations
    )
    assert not any(loc.availability_type == _TODAY_TYPE for loc in locations)


@pytest.mark.graphql
@pytest.mark.skip
@pytest.mark.with_cart([(_MULTIREGION_PRODUCT_ID, 1)])
def test_cart_pickup_locations_product_multiregion(
    graphql_client: GraphQLClient,
    ctx: Context,
    with_cart: Cart,
    global_settings: GlobalSettings,
) -> None:
    pickup_location_ops = PickupLocationOperations(client=graphql_client)

    locations = pickup_location_ops.get_cart_pickup_locations(
        cart_id=with_cart.id,
        store_id=ctx.store_id,
        culture_name=ctx.culture_name,
        first=global_settings.default_page_size,
    )

    availability_types = {loc.availability_type for loc in locations}
    assert len(locations) > 0
    assert _TODAY_TYPE in availability_types
    assert (
        _TRANSFER_TYPE in availability_types
        or _GLOBAL_TRANSFER_TYPE in availability_types
    )
