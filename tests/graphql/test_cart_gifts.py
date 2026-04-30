import allure
import pytest
from gql.types import Cart

_PRODUCT_ID = "smartphone-samsung-galaxy-a17-5g-black"
_QUANTITY = 20


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_ID, _QUANTITY)])
@allure.feature("Cart / Gifts (GraphQL)")
@allure.title("Gift is granted when quantity threshold is reached")
def test_cart_gifts(with_cart: Cart) -> None:
    cart = with_cart

    with allure.step(f"Verify cart with {_QUANTITY}× {_PRODUCT_ID} has 1 gift"):
        assert cart is not None
        assert cart.gifts is not None and len(cart.gifts) == 1
