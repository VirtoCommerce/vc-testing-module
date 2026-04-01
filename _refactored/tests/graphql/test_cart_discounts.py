import pytest

from gql.types import Cart

_PRODUCT_ITEM_DISCOUNT_ID = "product-acme-laptop-hp-omen-transcend-14"
_PRODUCT_SUBTOTAL_DISCOUNT_ID = "product-acme-laptop-lenovo-legion-9i-gen-10"


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_ITEM_DISCOUNT_ID, 1)])
def test_cart_item_discount(with_cart: Cart) -> None:
    cart = with_cart

    assert cart is not None
    assert len(cart.items) == 1
    item = cart.items[0]
    assert item.product_id == _PRODUCT_ITEM_DISCOUNT_ID
    assert item.discount_amount is not None
    assert item.discount_amount.amount > 0


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_SUBTOTAL_DISCOUNT_ID, 1)])
def test_cart_subtotal_discount(with_cart: Cart) -> None:
    cart = with_cart

    assert cart is not None
    assert cart.sub_total_discount is not None
    assert cart.sub_total_discount.amount > 0
