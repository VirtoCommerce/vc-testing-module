import pytest

from core.clients import GraphQLClient
from gql.operations import QuoteOperations
from gql.types.cart import Cart
from gql.types.quote import Quote

_PRODUCT_ID = "product-acme-laptop-asus-zenbook-a14-ux3407"
_USERNAME = "acme_store_employee_1@acme.com"
_UPDATED_QUANTITY = 5
_UPDATED_COMMENT = "Updated comment"


@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, 1)])
def test_quote_update_items(
    graphql_client: GraphQLClient,
    with_cart: Cart,
) -> None:
    quote_ops = QuoteOperations(client=graphql_client)

    quote = quote_ops.create_quote_from_cart(cart_id=with_cart.id)
    line_item = quote.items[0]

    updated_quote = quote_ops.change_quote_item_quantity(
        quote_id=quote.id,
        line_item_id=line_item.id,
        quantity=_UPDATED_QUANTITY,
    )

    updated_item = next(i for i in updated_quote.items if i.id == line_item.id)
    assert any(t.quantity == _UPDATED_QUANTITY for t in updated_item.proposal_prices)


@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
@pytest.mark.with_cart([(_PRODUCT_ID, 1)])
def test_quote_update_comment(
    graphql_client: GraphQLClient,
    with_cart: Cart,
) -> None:
    quote_ops = QuoteOperations(client=graphql_client)
    quote = quote_ops.create_quote_from_cart(cart_id=with_cart.id)

    updated_quote = quote_ops.change_quote_comment(
        quote_id=quote.id,
        comment=_UPDATED_COMMENT,
    )

    assert updated_quote.comment == _UPDATED_COMMENT
