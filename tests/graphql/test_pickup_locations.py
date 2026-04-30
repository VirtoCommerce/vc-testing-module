import allure
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
@allure.feature("Pickup Locations (GraphQL)")
@allure.title("List all pickup locations with paging")
def test_pickup_locations_all(
    graphql_client: GraphQLClient, ctx: Context, global_settings: GlobalSettings
) -> None:
    ops = PickupLocationOperations(client=graphql_client)

    with allure.step(f"Get first {_PAGE_SIZE} pickup locations"):
        page = ops.get_pickup_locations(store_id=ctx.store_id, first=_PAGE_SIZE)
        assert len(page) == _PAGE_SIZE

    with allure.step("Get all pickup locations using default page size"):
        all_locations = ops.get_pickup_locations(
            store_id=ctx.store_id,
            first=global_settings.default_page_size,
        )

    with allure.step("Verify all locations have populated address fields"):
        assert len(all_locations) > _PAGE_SIZE
        assert all(loc.address is not None for loc in all_locations)
        assert all(
            getattr(loc.address, field)
            for loc in all_locations
            for field in _ADDRESS_FIELDS
        )


@pytest.mark.graphql
@pytest.mark.skip
@allure.feature("Pickup Locations (GraphQL)")
@allure.title("Filter pickup locations by keyword")
def test_pickup_locations_by_keyword(
    graphql_client: GraphQLClient, ctx: Context
) -> None:
    ops = PickupLocationOperations(client=graphql_client)

    with allure.step(f"Get pickup locations matching keyword '{_KEYWORD}'"):
        locations = ops.get_pickup_locations(store_id=ctx.store_id, keyword=_KEYWORD)

    with allure.step(f"Verify all locations contain '{_KEYWORD}' in their name"):
        assert len(locations) > 0
        assert all(_KEYWORD in loc.name for loc in locations)
