import pytest
from core.clients import GraphQLClient
from gql.operations import SeoOperations
from tests.context import Context

_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black"
_PRODUCT_PERMALINK = "smartphones/apple-iphone-17-256gb-black"
_PRODUCT_SEMANTIC_URL = "apple-iphone-17-256gb-black"
_OBJECT_TYPE = "CatalogProduct"


@pytest.mark.graphql
def test_product_slug_info(graphql_client: GraphQLClient, ctx: Context) -> None:
    slug_info = SeoOperations(client=graphql_client).get_slug_info(
        store_id=ctx.store_id,
        culture_name=ctx.culture_name,
        permalink=_PRODUCT_PERMALINK,
    )

    assert slug_info is not None
    assert slug_info.entity_info is not None

    entity = slug_info.entity_info
    assert entity.object_id == _PRODUCT_ID
    assert entity.object_type == _OBJECT_TYPE
    assert entity.semantic_url == _PRODUCT_SEMANTIC_URL
    assert entity.store_id == ctx.store_id
    assert entity.is_active is True
    assert entity.language_code == ctx.culture_name
    assert entity.page_title is not None
