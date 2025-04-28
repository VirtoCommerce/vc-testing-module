import allure, os
from tests_graphql.operations.catalog.categories_operations import CategoriesOperations
from tests_graphql.operations.catalog.products_operations import ProductsOperations
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_catalog import TEST_CATALOG


@allure.title("Catalog browsing (GraphQL)")
def test_catalog_browsing(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to browse catalog...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    categories_operations = CategoriesOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)

    user = user_operations.get_user()

    categories_response = categories_operations.get_categories(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        filter=f"category.subtree:{TEST_CATALOG['id']}",
    )

    category_to_compare = categories_response["items"][0]

    category = categories_operations.get_category(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        id=category_to_compare["id"],
    )

    products_response = products_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        filter=f"category.subtree:{TEST_CATALOG['id']}/{category['id']}",
    )

    product_to_compare = products_response["items"][0]

    product = products_operations.get_product(
        store_id=config["store_id"],
        user_id=user["id"],
        culture_name=TEST_CULTURE["en-US"],
        currency_code=TEST_CURRENCY["USD"],
        id=product_to_compare["id"],
    )

    assert category["id"] == category_to_compare["id"], "Category ID does not match"
    assert product["id"] == product_to_compare["id"], "Product ID does not match"
