import pytest
from core.clients import GraphQLClient
from gql.operations import QuoteOperations
from gql.types import Cart
from tests.context import Context

_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black"
_QUANTITY = 2
_USERNAME = "acme_store_employee_1@acme.com"


@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
def test_quote_create_empty(graphql_client: GraphQLClient, ctx: Context) -> None:
    quote_ops = QuoteOperations(client=graphql_client)

    quote = quote_ops.create_quote(
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        currency_code=ctx.currency_code,
        culture_name=ctx.culture_name,
    )

    assert quote is not None
    assert quote.id is not None
    assert quote.store_id == ctx.store_id
    assert quote.items == []


@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
def test_quote_create_from_cart(graphql_client: GraphQLClient, ctx: Context, with_cart: Cart) -> None:
    quote_ops = QuoteOperations(client=graphql_client)

    quote = quote_ops.create_quote_from_cart(cart_id=with_cart.id)

    assert quote is not None
    assert quote.id is not None
    assert quote.store_id == ctx.store_id
    assert len(quote.items) == 1
    assert quote.items[0].product_id == _PRODUCT_ID
    assert quote.items[0].quantity == _QUANTITY
