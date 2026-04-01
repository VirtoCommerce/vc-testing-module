import pytest

from gql.types.cart import Cart

_REGISTERED_USER = "acme_store_maintainer_1@acme.com"
_PRODUCT_ID = "product-acme-laptop-asus-zenbook-a14-ux3407"


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_ID, 1)])
def test_cart_anonymous(with_cart: Cart) -> None:
    assert with_cart is not None
    assert with_cart.is_anonymous is True


@pytest.mark.graphql
@pytest.mark.with_user(_REGISTERED_USER)
@pytest.mark.with_cart([(_PRODUCT_ID, 1)])
def test_cart_registered_user(with_cart: Cart) -> None:
    assert with_cart is not None
    assert with_cart.is_anonymous is False
