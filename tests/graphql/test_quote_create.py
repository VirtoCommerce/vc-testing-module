import allure
import pytest

from core.clients import GraphQLClient
from gql.operations import QuoteOperations
from gql.types import Cart
from tests.context import Context

_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black"
_QUANTITY = 2
_USERNAME = "acme_store_employee_1@acme.com"


@pytest.mark.optional
@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
@allure.feature("Quotes (GraphQL)")
@allure.title("Create an empty quote")
def test_quote_create_empty(graphql_client: GraphQLClient, ctx: Context) -> None:
    quote_ops = QuoteOperations(client=graphql_client)

    with allure.step(f"Create empty quote in store {ctx.store_id}"):
        quote = quote_ops.create_quote(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
        )

    with allure.step("Verify quote is created and has no items"):
        assert quote is not None
        assert quote.id is not None
        assert quote.store_id == ctx.store_id
        assert quote.items == []


@pytest.mark.optional
@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Quotes (GraphQL)")
@allure.title("Create a quote from an existing cart")
def test_quote_create_from_cart(
    graphql_client: GraphQLClient, ctx: Context, with_cart: Cart
) -> None:
    quote_ops = QuoteOperations(client=graphql_client)

    with allure.step(f"Create quote from cart {with_cart.id}"):
        quote = quote_ops.create_quote_from_cart(cart_id=with_cart.id)

    with allure.step(
        f"Verify quote contains {_PRODUCT_ID}×{_QUANTITY} carried over from cart"
    ):
        assert quote is not None
        assert quote.id is not None
        assert quote.store_id == ctx.store_id
        assert len(quote.items) == 1
        assert quote.items[0].product_id == _PRODUCT_ID
        assert quote.items[0].quantity == _QUANTITY
