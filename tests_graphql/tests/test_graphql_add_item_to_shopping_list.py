import allure, os, pytest
from graphql_operations.shopping_lists.shopping_lists_operations import ShoppingListsOperations
from graphql_operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_product import TEST_PRODUCT_1
from tests_graphql.test_data.test_user import TEST_PERMANENT_USER


@pytest.mark.graphql
@allure.title("Add item to shopping list (GraphQL)")
def test_add_item_to_shopping_list(config, auth, graphql_client):
    print(f"{os.linesep}Running test to add item to shopping list...", end=" ")

    user_operations = UserOperations(graphql_client)
    shopping_lists_operations = ShoppingListsOperations(graphql_client)

    auth.authenticate(TEST_PERMANENT_USER["username"], TEST_PERMANENT_USER["password"])

    user = user_operations.get_user()

    shopping_list = shopping_lists_operations.create_shopping_list(
        payload={
            "userId": user["id"],
            "storeId": config["store_id"],
            "listName": "[E2E test] Test shopping list",
            "cultureName": TEST_CULTURE["en-US"],
            "currencyCode": TEST_CURRENCY["USD"],
            "scope": "Private",
        }
    )

    shopping_list_with_item = shopping_lists_operations.add_item_to_shopping_list(
        list_id=shopping_list["id"],
        product_id=TEST_PRODUCT_1["id"],
        quantity=1,
    )

    # Test teardown

    shopping_lists_operations.remove_shopping_list(
        payload={
            "listId": shopping_list["id"],
        }
    )

    auth.clear_token()

    assert shopping_list_with_item["id"] is not None, "Shopping list ID is not set"
    assert shopping_list_with_item["id"] == shopping_list["id"], "Shopping list ID does not match"
    assert shopping_list_with_item["itemsCount"] == 1, "Shopping list items count is not 1"
