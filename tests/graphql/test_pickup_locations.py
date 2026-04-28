import pytest
from core.clients import GraphQLClient
from core.global_settings import GlobalSettings
from gql.operations import PickupLocationOperations
from tests.context import Context

_KEYWORD = "Berlin"
_PAGE_SIZE = 5
_ADDRESS_FIELDS = ("city", "country_name", "line1")


@pytest.mark.graphql
@pytest.mark.skip
def test_pickup_locations_all(
    graphql_client: GraphQLClient, ctx: Context, global_settings: GlobalSettings
) -> None:
    ops = PickupLocationOperations(client=graphql_client)

    page = ops.get_pickup_locations(store_id=ctx.store_id, first=_PAGE_SIZE)
    assert len(page) == _PAGE_SIZE

    all_locations = ops.get_pickup_locations(
        store_id=ctx.store_id,
        first=global_settings.default_page_size,
    )
    assert len(all_locations) > _PAGE_SIZE

    assert all(loc.address is not None for loc in all_locations)
    assert all(
        getattr(loc.address, field)
        for loc in all_locations
        for field in _ADDRESS_FIELDS
    )


@pytest.mark.graphql
@pytest.mark.skip
def test_pickup_locations_by_keyword(
    graphql_client: GraphQLClient, ctx: Context
) -> None:
    ops = PickupLocationOperations(client=graphql_client)
    locations = ops.get_pickup_locations(store_id=ctx.store_id, keyword=_KEYWORD)

    assert len(locations) > 0
    assert all(_KEYWORD in loc.name for loc in locations)
