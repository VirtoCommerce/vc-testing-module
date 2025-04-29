import allure, os
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.operations.catalog.products_operations import ProductsOperations
from tests_graphql.operations.catalog.categories_operations import CategoriesOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_product import TEST_PRODUCT_1
from tests_graphql.test_data.test_category import TEST_CATEGORY_1
from tests_graphql.test_data.test_catalog import TEST_CATALOG


@allure.title("Catalog search by product full name (GraphQL)")
def test_catalog_search_by_product_full_name(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to search catalog by product full name...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    products_operations = ProductsOperations(graphql_client)

    user = user_operations.get_user()

    products_response = products_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        query=TEST_PRODUCT_1["name"],
    )

    product = products_response["items"][0]

    assert products_response["totalCount"] == 1, "Total count of products does not match"
    assert product["name"] == TEST_PRODUCT_1["name"], "Product name does not match"


@allure.title("Catalog search by product name fragment (GraphQL)")
def test_catalog_search_by_product_name_fragment(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to search catalog by product name fragment...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    products_operations = ProductsOperations(graphql_client)

    user = user_operations.get_user()

    products_response = products_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        query=TEST_PRODUCT_1["name"][:4],
    )

    assert products_response["totalCount"] > 1, "Total count of products does not match"


@allure.title("Catalog search by product SKU (GraphQL)")
def test_catalog_search_by_product_sku(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to search catalog by product SKU...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    products_operations = ProductsOperations(graphql_client)

    user = user_operations.get_user()

    products_response = products_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        query=TEST_PRODUCT_1["sku"],
    )

    product = products_response["items"][0]

    assert products_response["totalCount"] == 1, "Total count of products does not match"
    assert product["code"] == TEST_PRODUCT_1["sku"], "Product SKU does not match"


@allure.title("Catalog search by product availability (GraphQL)")
def test_catalog_search_by_product_availability(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to search catalog by product availability...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    categories_operations = CategoriesOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)

    user = user_operations.get_user()

    category = categories_operations.get_category(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        id=TEST_CATEGORY_1["id"],
    )

    products_in_stock_only_response = products_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        query=TEST_PRODUCT_1["name"][:4],
        filter=f"category.subtree:{TEST_CATALOG['id']}/{category['id']} availability:InStock",
    )

    products_all_response = products_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        query=TEST_PRODUCT_1["name"][:4],
        filter=f"category.subtree:{TEST_CATALOG['id']}/{category['id']}",
    )

    assert products_in_stock_only_response["totalCount"] == 3, "Total count of products does not match"
    assert products_all_response["totalCount"] == 4, "Total count of products does not match"


@allure.title("Catalog search by product brand (GraphQL)")
def test_catalog_search_by_product_brand(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to search catalog by product brand...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    categories_operations = CategoriesOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)

    user = user_operations.get_user()

    category = categories_operations.get_category(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        id=TEST_CATEGORY_1["id"],
    )

    products_response = products_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        query=TEST_PRODUCT_1["name"][:4],
        filter=f"category.subtree:{TEST_CATALOG['id']}/{category['id']} \"BRAND\":\"{TEST_PRODUCT_1['brand']}\"",
    )

    assert products_response["totalCount"] == 1, "Total count of products does not match"


@allure.title("Catalog search by product price (GraphQL)")
def test_catalog_search_by_product_price(config, auth_token, graphql_client):
    print(f"{os.linesep}Running test to search catalog by product price...", end=" ")

    user_operations = UserOperations(auth_token, graphql_client)
    categories_operations = CategoriesOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)

    user = user_operations.get_user()

    category = categories_operations.get_category(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        id=TEST_CATEGORY_1["id"],
    )

    products_response = products_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        query=TEST_PRODUCT_1["name"][:4],
        filter=f"category.subtree:{TEST_CATALOG['id']}/{category['id']} \"price\":[1000 TO 1500]",
    )

    assert products_response["totalCount"] == 1, "Total count of products does not match"
