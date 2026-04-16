import pytest

from core.clients import GraphQLClient
from core.global_settings import GlobalSettings
from gql.operations import ProductOperations
from tests.context import Context

_CATEGORY_ID = "category-acme-laptops"
_PRODUCT_VENDOR = "Asus"
_PRODUCT_NAME = "Asus Zenbook A14 (UX3407)"
_PRODUCT_CODE = "product-acme-laptop-asus-zenbook-a14-ux3407"


@pytest.mark.graphql
def test_catalog_search_full_product_name(
    graphql_client: GraphQLClient, ctx: Context, global_settings: GlobalSettings
) -> None:
    product_ops = ProductOperations(client=graphql_client)

    products = product_ops.get_products(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        culture_name=ctx.culture_name,
        currency_code=ctx.currency_code,
        query=_PRODUCT_NAME,
        first=global_settings.default_page_size,
    )

    assert products is not None and len(products) > 0
    assert any(p for p in products if p.name == _PRODUCT_NAME)


@pytest.mark.graphql
def test_catalog_search_product_name_fragment(
    graphql_client: GraphQLClient, ctx: Context, global_settings: GlobalSettings
) -> None:
    product_ops = ProductOperations(client=graphql_client)

    products = product_ops.get_products(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        culture_name=ctx.culture_name,
        currency_code=ctx.currency_code,
        query=_PRODUCT_NAME[:4],
        first=global_settings.default_page_size,
    )

    assert products is not None and len(products) > 0
    assert any(p for p in products if p.name == _PRODUCT_NAME)


@pytest.mark.graphql
def test_catalog_search_product_code(
    graphql_client: GraphQLClient, ctx: Context, global_settings: GlobalSettings
) -> None:
    product_ops = ProductOperations(client=graphql_client)

    products = product_ops.get_products(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        culture_name=ctx.culture_name,
        currency_code=ctx.currency_code,
        query=_PRODUCT_CODE,
        first=global_settings.default_page_size,
    )

    assert products is not None and len(products) > 0
    assert any(p for p in products if p.code == _PRODUCT_CODE)


@pytest.mark.graphql
def test_catalog_search_product_availability(
    graphql_client: GraphQLClient, ctx: Context, global_settings: GlobalSettings
) -> None:
    product_ops = ProductOperations(client=graphql_client)

    products = product_ops.get_products(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        culture_name=ctx.culture_name,
        currency_code=ctx.currency_code,
        filter=f"category.subtree:{ctx.catalog_id}/{_CATEGORY_ID}",
        first=global_settings.default_page_size,
    )
    products_count = len(products)

    products_in_stock = product_ops.get_products(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        culture_name=ctx.culture_name,
        currency_code=ctx.currency_code,
        filter=f"category.subtree:{ctx.catalog_id}/{_CATEGORY_ID} availability:InStock",
    )
    products_in_stock_count = len(products_in_stock)

    assert products_count > 0
    assert products_in_stock_count > 0
    assert products_count > products_in_stock_count


@pytest.mark.graphql
def test_catalog_search_product_brand(
    graphql_client: GraphQLClient, ctx: Context, global_settings: GlobalSettings
) -> None:
    product_ops = ProductOperations(client=graphql_client)

    products = product_ops.get_products(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        culture_name=ctx.culture_name,
        currency_code=ctx.currency_code,
        filter=f'category.subtree:{ctx.catalog_id}/{_CATEGORY_ID} \\"BRAND\\":\\"{_PRODUCT_VENDOR}\\"',  # fmt: skip
        first=global_settings.default_page_size,
    )

    assert products is not None and len(products) > 0
    assert all(p for p in products if p.vendor == _PRODUCT_VENDOR)
