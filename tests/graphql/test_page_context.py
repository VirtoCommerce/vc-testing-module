import pytest
from core.clients import GraphQLClient
from gql.operations import PageContextOperations
from tests.context import Context

_REGISTERED_USER = "acme_store_maintainer_1@acme.com"
_CATEGORY_PERMALINK = "smartphones"
_CATEGORY_OBJECT_TYPE = "Category"


@pytest.mark.graphql
def test_page_context_store_info(graphql_client: GraphQLClient, ctx: Context) -> None:
    pc = PageContextOperations(client=graphql_client).get_page_context(
        store_id=ctx.store_id,
        culture_name=ctx.culture_name,
    )

    assert pc is not None
    assert pc.store is not None
    assert pc.store.store_id == ctx.store_id
    assert pc.store.catalog_id == ctx.catalog_id
    assert pc.store.default_language.culture_name == ctx.culture_name
    assert pc.store.default_currency.code == ctx.currency_code
    assert len(pc.store.available_languages) > 0
    assert len(pc.store.available_currencies) > 0


@pytest.mark.graphql
def test_page_context_slug_info(graphql_client: GraphQLClient, ctx: Context) -> None:
    pc = PageContextOperations(client=graphql_client).get_page_context(
        store_id=ctx.store_id,
        culture_name=ctx.culture_name,
        permalink=_CATEGORY_PERMALINK,
    )

    assert pc is not None
    assert pc.slug_info is not None
    assert pc.slug_info.entity_info is not None


@pytest.mark.graphql
def test_page_context_category_slug_info(graphql_client: GraphQLClient, ctx: Context) -> None:
    pc = PageContextOperations(client=graphql_client).get_page_context(
        store_id=ctx.store_id,
        culture_name=ctx.culture_name,
        permalink=_CATEGORY_PERMALINK,
    )

    assert pc is not None
    assert pc.slug_info is not None
    assert pc.slug_info.entity_info is not None
    assert pc.slug_info.entity_info.object_type == _CATEGORY_OBJECT_TYPE
    assert pc.slug_info.entity_info.semantic_url == _CATEGORY_PERMALINK


@pytest.mark.graphql
def test_page_context_slug_info_anonymous(graphql_client: GraphQLClient, ctx: Context) -> None:
    pc = PageContextOperations(client=graphql_client).get_page_context(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        culture_name=ctx.culture_name,
        permalink=_CATEGORY_PERMALINK,
    )

    assert pc is not None
    assert pc.slug_info is not None
    assert pc.slug_info.entity_info is not None
    assert pc.slug_info.entity_info.semantic_url == _CATEGORY_PERMALINK


@pytest.mark.graphql
@pytest.mark.with_user(_REGISTERED_USER)
def test_page_context_slug_info_registered(graphql_client: GraphQLClient, ctx: Context) -> None:
    pc = PageContextOperations(client=graphql_client).get_page_context(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        culture_name=ctx.culture_name,
        permalink=_CATEGORY_PERMALINK,
    )

    assert pc is not None
    assert pc.slug_info is not None
    assert pc.slug_info.entity_info is not None
    assert pc.slug_info.entity_info.semantic_url == _CATEGORY_PERMALINK


@pytest.mark.graphql
def test_page_context_user_anonymous(graphql_client: GraphQLClient, ctx: Context) -> None:
    pc = PageContextOperations(client=graphql_client).get_page_context(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        culture_name=ctx.culture_name,
    )

    assert pc is not None
    assert pc.user is not None
    assert pc.user.user_name == "Anonymous"


@pytest.mark.graphql
@pytest.mark.with_user(_REGISTERED_USER)
def test_page_context_user_registered(graphql_client: GraphQLClient, ctx: Context) -> None:
    pc = PageContextOperations(client=graphql_client).get_page_context(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        culture_name=ctx.culture_name,
    )

    assert pc is not None
    assert pc.user is not None
    assert pc.user.user_name == _REGISTERED_USER


@pytest.mark.graphql
def test_page_context_white_labeling(graphql_client: GraphQLClient, ctx: Context) -> None:
    pc = PageContextOperations(client=graphql_client).get_page_context(
        store_id=ctx.store_id,
        culture_name=ctx.culture_name,
    )

    assert pc is not None
    # white_labeling_settings may be null when no custom branding is configured
    if pc.white_labeling_settings is not None:
        wls = pc.white_labeling_settings
        assert isinstance(wls.footer_links, list)
        assert isinstance(wls.main_menu_links, list)


@pytest.mark.graphql
def test_page_context_full(graphql_client: GraphQLClient, ctx: Context) -> None:
    pc = PageContextOperations(client=graphql_client).get_page_context(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        culture_name=ctx.culture_name,
        permalink=_CATEGORY_PERMALINK,
    )

    assert pc is not None
    assert pc.store is not None
    assert pc.user is not None
    assert pc.slug_info is not None
    assert pc.slug_info.entity_info is not None
    assert pc.store.store_id == ctx.store_id
    assert pc.user.user_name == "Anonymous"
    assert pc.slug_info.entity_info.object_type == _CATEGORY_OBJECT_TYPE
