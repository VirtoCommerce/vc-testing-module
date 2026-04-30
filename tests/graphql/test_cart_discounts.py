import allure
import pytest
from gql.types import Cart

_PRODUCT_ITEM_DISCOUNT_ID = "smartphone-samsung-galaxy-a57-5g"
_PRODUCT_SUBTOTAL_DISCOUNT_ID = "smartphone-samsung-galaxy-s26-black"


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_ITEM_DISCOUNT_ID, 1)])
@allure.feature("Cart / Discounts (GraphQL)")
@allure.title("Item-level discount is applied to a discounted product")
def test_cart_item_discount(with_cart: Cart) -> None:
    cart = with_cart

    with allure.step(
        f"Verify item-level discount is applied to {_PRODUCT_ITEM_DISCOUNT_ID}"
    ):
        assert cart is not None
        assert len(cart.items) == 1
        item = cart.items[0]
        assert item.product_id == _PRODUCT_ITEM_DISCOUNT_ID
        assert item.discount_amount is not None
        assert item.discount_amount.amount > 0


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_SUBTOTAL_DISCOUNT_ID, 5)])
@allure.feature("Cart / Discounts (GraphQL)")
@allure.title("Subtotal discount is applied when threshold is reached")
def test_cart_subtotal_discount(with_cart: Cart) -> None:
    cart = with_cart

    with allure.step("Verify subtotal discount is greater than zero"):
        assert cart is not None
        assert cart.sub_total_discount is not None
        assert cart.sub_total_discount.amount > 0
