import allure
import pytest
from core.clients import GraphQLClient
from core.global_settings import GlobalSettings
from gql.operations import ProductOperations
from tests.context import Context

_CATEGORY_ID = "category-acme-electronics-smartphones"
_PRODUCT_VENDOR = "Google"
_PRODUCT_NAME = "Google Pixel 10 Pro Jade"
_PRODUCT_CODE = "smartphone-google-pixel-10-pro-jade"


@pytest.mark.graphql
@allure.feature("Catalog / Search (GraphQL)")
@allure.title("Search products by full product name")
def test_catalog_search_full_product_name(
    graphql_client: GraphQLClient, ctx: Context, global_settings: GlobalSettings
) -> None:
    product_ops = ProductOperations(client=graphql_client)

    with allure.step(f"Search products by full name '{_PRODUCT_NAME}'"):
        products = product_ops.get_products(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            culture_name=ctx.culture_name,
            currency_code=ctx.currency_code,
            query=_PRODUCT_NAME,
            first=global_settings.default_page_size,
        )

    with allure.step(f"Verify results contain product '{_PRODUCT_NAME}'"):
        assert products is not None and len(products) > 0
        assert any(p for p in products if p.name == _PRODUCT_NAME)


@pytest.mark.graphql
@allure.feature("Catalog / Search (GraphQL)")
@allure.title("Search products by product name fragment")
def test_catalog_search_product_name_fragment(
    graphql_client: GraphQLClient, ctx: Context, global_settings: GlobalSettings
) -> None:
    product_ops = ProductOperations(client=graphql_client)

    fragment = _PRODUCT_NAME[:4]
    with allure.step(f"Search products by name fragment '{fragment}'"):
        products = product_ops.get_products(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            culture_name=ctx.culture_name,
            currency_code=ctx.currency_code,
            query=fragment,
            first=global_settings.default_page_size,
        )

    with allure.step(f"Verify results contain product '{_PRODUCT_NAME}'"):
        assert products is not None and len(products) > 0
        assert any(p for p in products if p.name == _PRODUCT_NAME)


@pytest.mark.graphql
@allure.feature("Catalog / Search (GraphQL)")
@allure.title("Search products by product code")
def test_catalog_search_product_code(
    graphql_client: GraphQLClient, ctx: Context, global_settings: GlobalSettings
) -> None:
    product_ops = ProductOperations(client=graphql_client)

    with allure.step(f"Search products by code '{_PRODUCT_CODE}'"):
        products = product_ops.get_products(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            culture_name=ctx.culture_name,
            currency_code=ctx.currency_code,
            query=_PRODUCT_CODE,
            first=global_settings.default_page_size,
        )

    with allure.step(f"Verify results contain product with code '{_PRODUCT_CODE}'"):
        assert products is not None and len(products) > 0
        assert any(p for p in products if p.code == _PRODUCT_CODE)


@pytest.mark.graphql
@allure.feature("Catalog / Search (GraphQL)")
@allure.title("Filter catalog products by InStock availability")
def test_catalog_search_product_availability(
    graphql_client: GraphQLClient, ctx: Context, global_settings: GlobalSettings
) -> None:
    product_ops = ProductOperations(client=graphql_client)

    with allure.step(f"Get all products in category {_CATEGORY_ID}"):
        products = product_ops.get_products(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            culture_name=ctx.culture_name,
            currency_code=ctx.currency_code,
            filter=f"category.subtree:{ctx.catalog_id}/{_CATEGORY_ID}",
            first=global_settings.default_page_size,
        )
        products_count = len(products)

    with allure.step(
        f"Get InStock products in category {_CATEGORY_ID}"
    ):
        products_in_stock = product_ops.get_products(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            culture_name=ctx.culture_name,
            currency_code=ctx.currency_code,
            filter=f"category.subtree:{ctx.catalog_id}/{_CATEGORY_ID} availability:InStock",
        )
        products_in_stock_count = len(products_in_stock)

    with allure.step("Verify InStock count is non-zero and less than the full count"):
        assert products_count > 0
        assert products_in_stock_count > 0
        assert products_count > products_in_stock_count


@pytest.mark.graphql
@allure.feature("Catalog / Search (GraphQL)")
@allure.title("Filter catalog products by brand")
def test_catalog_search_product_brand(
    graphql_client: GraphQLClient, ctx: Context, global_settings: GlobalSettings
) -> None:
    product_ops = ProductOperations(client=graphql_client)

    with allure.step(f"Search products by brand '{_PRODUCT_VENDOR}'"):
        products = product_ops.get_products(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            culture_name=ctx.culture_name,
            currency_code=ctx.currency_code,
            filter=f'category.subtree:{ctx.catalog_id}/{_CATEGORY_ID} \\"BRAND\\":\\"{_PRODUCT_VENDOR}\\"',  # fmt: skip
            first=global_settings.default_page_size,
        )

    with allure.step(f"Verify all returned products have vendor '{_PRODUCT_VENDOR}'"):
        assert products is not None and len(products) > 0
        assert all(p for p in products if p.vendor == _PRODUCT_VENDOR)
