import allure
import pytest

from core.clients import GraphQLClient
from gql.operations import QuoteOperations
from gql.types.cart import Cart

_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black"
_USERNAME = "acme_store_employee_1@acme.com"
_UPDATED_QUANTITY = 5
_UPDATED_COMMENT = "Updated comment"


@pytest.mark.optional
@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, 1)])
@allure.feature("Quotes (GraphQL)")
@allure.title("Update a quote line item quantity")
def test_quote_update_items(
    graphql_client: GraphQLClient,
    with_cart: Cart,
) -> None:
    quote_ops = QuoteOperations(client=graphql_client)

    with allure.step(f"Create quote from cart {with_cart.id}"):
        quote = quote_ops.create_quote_from_cart(cart_id=with_cart.id)
        line_item = quote.items[0]

    with allure.step(
        f"Change line item {line_item.id} quantity to {_UPDATED_QUANTITY}"
    ):
        updated_quote = quote_ops.change_quote_item_quantity(
            quote_id=quote.id,
            line_item_id=line_item.id,
            quantity=_UPDATED_QUANTITY,
        )

    with allure.step(f"Verify proposal prices include quantity {_UPDATED_QUANTITY}"):
        updated_item = next(i for i in updated_quote.items if i.id == line_item.id)
        assert any(
            t.quantity == _UPDATED_QUANTITY for t in updated_item.proposal_prices
        )


@pytest.mark.optional
@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, 1)])
@allure.feature("Quotes (GraphQL)")
@allure.title("Update a quote comment")
def test_quote_update_comment(
    graphql_client: GraphQLClient,
    with_cart: Cart,
) -> None:
    quote_ops = QuoteOperations(client=graphql_client)

    with allure.step(f"Create quote from cart {with_cart.id}"):
        quote = quote_ops.create_quote_from_cart(cart_id=with_cart.id)

    with allure.step(f"Change quote comment to '{_UPDATED_COMMENT}'"):
        updated_quote = quote_ops.change_quote_comment(
            quote_id=quote.id,
            comment=_UPDATED_COMMENT,
        )

    with allure.step(f"Verify quote comment is '{_UPDATED_COMMENT}'"):
        assert updated_quote.comment == _UPDATED_COMMENT
