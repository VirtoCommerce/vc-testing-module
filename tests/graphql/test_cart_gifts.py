import pytest
from gql.types import Cart

_PRODUCT_ID = "smartphone-samsung-galaxy-a17-5g-black"
_QUANTITY = 20


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
def test_cart_gifts(with_cart: Cart) -> None:
    cart = with_cart

    assert cart is not None
    assert cart.gifts is not None and len(cart.gifts) == 1
