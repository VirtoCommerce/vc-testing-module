import pytest
from core.clients import GraphQLClient
from gql.operations import SeoOperations
from tests.context import Context

_CATEGORY_SLUG = "smartphones"


@pytest.mark.graphql
def test_category_seo(graphql_client: GraphQLClient, ctx: Context) -> None:
    seo_ops = SeoOperations(client=graphql_client)

    seo_info = seo_ops.get_slug_info(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        culture_name=ctx.culture_name,
        slug=_CATEGORY_SLUG,
    )

    assert seo_info is not None
    assert seo_info.entity_info is not None
    assert seo_info.entity_info.semantic_url == _CATEGORY_SLUG
