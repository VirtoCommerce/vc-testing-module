from typing import Any, Dict

import allure
import pytest

from fixtures.auth import Auth
from fixtures.graphql_client import GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.fixture(scope="function", autouse=True)
@allure.title("Fixture to clear cart before each test")
def clear_cart(config: Dict[str, Any], auth: Auth, graphql_client: GraphQLClient, dataset: Dict[str, Any]):
    """
    Automatically clears the cart before each test runs.
    Uses GraphQL mutation with authentication to clear the user's cart.
    """
    # Authenticate the user
    auth.authenticate(config["username"], config["password"])
    
    # Get user ID
    user_operations = UserOperations(graphql_client)
    user = user_operations.get_me()
    user_id = user["id"]
    
    # Get cart operations
    cart_operations = CartOperations(graphql_client)
    
    # Get default currency and culture from dataset
    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]
    
    # Clear the cart (no check if empty or not, just clear it)
    cart_operations.clear_cart(
        payload={
            "storeId": config["store_id"],
            "userId": user_id,
            "currencyCode": currency,
            "cultureName": culture,
        }
    )
    
    yield

