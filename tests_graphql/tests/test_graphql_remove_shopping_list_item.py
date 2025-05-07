import allure, os
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.operations.shopping_lists.shopping_lists_operations import ShoppingListsOperations
from tests_graphql.test_data.test_user import TEST_PERMANENT_USER
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_product import TEST_PRODUCT_1


@allure.title("Remove shopping list item (GraphQL)")
def test_remove_shopping_list_item(config, user_service, graphql_client):
    print(f"{os.linesep}Running test to remove shopping list item...", end=" ")

    user_operations = UserOperations(graphql_client)
    shopping_lists_operations = ShoppingListsOperations(graphql_client)

    user_service.sign_in(TEST_PERMANENT_USER["username"], TEST_PERMANENT_USER["password"])

    user = user_operations.get_user()

    new_shopping_list = shopping_lists_operations.create_shopping_list(
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
        list_id=new_shopping_list["id"],
        product_id=TEST_PRODUCT_1["id"],
        quantity=1,
    )

    empty_shopping_list = shopping_lists_operations.remove_shopping_list_item(
        payload={
            "listId": shopping_list_with_item["id"],
            "lineItemId": shopping_list_with_item["items"][0]["id"],
        }
    )

    # Test teardown

    shopping_lists_operations.remove_shopping_list(
        payload={
            "listId": new_shopping_list["id"],
        }
    )

    user_service.sign_out()

    assert empty_shopping_list["id"] is not None, "Shopping list ID is not set"
    assert empty_shopping_list["id"] == new_shopping_list["id"], "Shopping list ID does not match"
    assert empty_shopping_list["itemsCount"] == 0, "Shopping list is not empty"
