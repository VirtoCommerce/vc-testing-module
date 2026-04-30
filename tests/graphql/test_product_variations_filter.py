import allure
import pytest
from core.clients import GraphQLClient
from core.global_settings import GlobalSettings
from gql.operations import ProductOperations
from tests.context import Context

_PRODUCT_ID = "smartphone-google-pixel-10-frost"


def _base_filter(ctx: Context) -> str:
    return (
        f"category.subtree:{ctx.catalog_id}"
        f" price.{ctx.currency_code}:(0 TO)"
        f" productfamilyid:{_PRODUCT_ID}"
        f" is:product,variation"
    )


@pytest.mark.graphql
@allure.feature("Product / Variations (GraphQL)")
@allure.title("Filter product variations by inStock")
def test_variations_filter_by_stock(
    graphql_client: GraphQLClient, ctx: Context, global_settings: GlobalSettings
) -> None:
    product_ops = ProductOperations(client=graphql_client)
    base = _base_filter(ctx)

    with allure.step("Get all variations matching base filter"):
        all_results = product_ops.get_products(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            culture_name=ctx.culture_name,
            currency_code=ctx.currency_code,
            filter=base,
            first=global_settings.default_page_size,
        )
        all_results_count = len(all_results)

    with allure.step("Get variations filtered by inStock:true"):
        in_stock_results = product_ops.get_products(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            culture_name=ctx.culture_name,
            currency_code=ctx.currency_code,
            filter=f"{base} inStock:true",
            first=global_settings.default_page_size,
        )
        in_stock_results_count = len(in_stock_results)

    with allure.step("Verify in-stock count is non-zero and at most the total count"):
        assert all_results_count > 0
        assert in_stock_results_count > 0
        assert all_results_count >= in_stock_results_count


@pytest.mark.graphql
@pytest.mark.parametrize(
    "price_range",
    [
        '\\"price\\":[TO 1000]',  # fmt: skip
        '\\"price\\":[1000 TO 1200]',  # fmt: skip
        '\\"price\\":[1400 TO]',  # fmt: skip
    ],
)
@allure.feature("Product / Variations (GraphQL)")
@allure.title("Filter product variations by price range")
def test_variations_filter_by_price(
    graphql_client: GraphQLClient,
    ctx: Context,
    global_settings: GlobalSettings,
    price_range: str,
) -> None:
    product_ops = ProductOperations(client=graphql_client)
    base = _base_filter(ctx)

    with allure.step("Get all variations matching base filter"):
        all_results = product_ops.get_products(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            culture_name=ctx.culture_name,
            currency_code=ctx.currency_code,
            filter=base,
            first=global_settings.default_page_size,
        )
        all_results_count = len(all_results)

    with allure.step(f"Get variations filtered by price range '{price_range}'"):
        filtered_results = product_ops.get_products(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            culture_name=ctx.culture_name,
            currency_code=ctx.currency_code,
            filter=f"{base} {price_range}",
            first=global_settings.default_page_size,
        )
        filtered_results_count = len(filtered_results)

    with allure.step("Verify filtered count is non-zero and at most the total count"):
        assert filtered_results_count > 0
        assert filtered_results_count <= all_results_count


@pytest.mark.graphql
@pytest.mark.parametrize("ram_size", ["8", "16", "32"])
@allure.feature("Product / Variations (GraphQL)")
@allure.title("Filter product variations by RamSize property")
def test_variations_filter_by_property(
    graphql_client: GraphQLClient,
    ctx: Context,
    global_settings: GlobalSettings,
    ram_size: str,
) -> None:
    product_ops = ProductOperations(client=graphql_client)

    with allure.step(f"Get variations filtered by RamSize='{ram_size}'"):
        products = product_ops.get_products(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            culture_name=ctx.culture_name,
            currency_code=ctx.currency_code,
            filter=f'{_base_filter(ctx)} \\"RamSize\\":\\"{ram_size}\\"',  # fmt: skip
            first=global_settings.default_page_size,
        )

    with allure.step(f"Verify variations are returned for RamSize='{ram_size}'"):
        assert len(products) > 0
