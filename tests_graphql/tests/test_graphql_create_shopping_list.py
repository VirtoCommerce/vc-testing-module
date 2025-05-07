import allure, os
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.operations.shopping_lists.shopping_lists_operations import ShoppingListsOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_user import TEST_PERMANENT_USER


@allure.title("Create shopping list (GraphQL)")
def test_create_shopping_list(config, user_service, graphql_client):
    print(f"{os.linesep}Running test to create shopping list...", end=" ")

    user_operations = UserOperations(graphql_client)
    shopping_lists_operations = ShoppingListsOperations(graphql_client)

    user_service.sign_in(TEST_PERMANENT_USER["username"], TEST_PERMANENT_USER["password"])

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

    # Test teardown

    shopping_lists_operations.remove_shopping_list(
        payload={
            "listId": shopping_list["id"],
        }
    )

    user_service.sign_out()

    assert shopping_list["id"] is not None
    assert shopping_list["storeId"] == config["store_id"]
    assert shopping_list["customerId"] == user["id"]
    assert shopping_list["itemsCount"] == 0
    assert shopping_list["scope"] == "Private"
