import json
from typing import Any, Dict

from fixtures.graphql_client import GraphQLClient
from graphql_operations.catalog.categories_operations import CategoriesOperations
from graphql_operations.catalog.products_operations import ProductsOperations
from graphql_operations.user.user_operations import UserOperations


def test_show_products(
    config: Dict[str, Any], graphql_client: GraphQLClient, dataset: Dict[str, Any]
):
    print("================ Products ==================")

    user_operations = UserOperations(graphql_client)
    categories_operations = CategoriesOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    catalog = dataset["catalogs"][0]
    user = user_operations.get_me()

    category = categories_operations.get_category(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        id="category-acme-laptops",
    )

    products_all_response = products_operations.get_products(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        filter=f"category.subtree:{catalog['id']}/{category['id']}",
    )

    for product in products_all_response["items"]:
        print(json.dumps(product, indent=2))
        print("--------------------------------")
