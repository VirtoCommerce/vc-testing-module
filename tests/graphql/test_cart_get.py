import allure
import pytest
from gql.types.cart import Cart

_REGISTERED_USER = "acme_store_maintainer_1@acme.com"
_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-mist-blue"


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_ID, 1)])
@allure.feature("Cart / Lifecycle (GraphQL)")
@allure.title("Get cart for an anonymous user")
def test_cart_get_anonymous(with_cart: Cart) -> None:
    with allure.step("Verify cart exists and is marked anonymous"):
        assert with_cart is not None
        assert with_cart.is_anonymous is True


@pytest.mark.graphql
@pytest.mark.with_user(_REGISTERED_USER)
@pytest.mark.with_cart([(_PRODUCT_ID, 1)])
@allure.feature("Cart / Lifecycle (GraphQL)")
@allure.title("Get cart for a registered user")
def test_cart_get_registered_user(with_cart: Cart) -> None:
    with allure.step("Verify cart exists and is not marked anonymous"):
        assert with_cart is not None
        assert with_cart.is_anonymous is False
