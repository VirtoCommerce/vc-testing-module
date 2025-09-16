import os
from typing import Any, Dict

import allure
import pytest

from fixtures import GraphQLClient
from graphql_operations.catalog.categories_operations import CategoriesOperations
from graphql_operations.seo.seo_operations import SeoOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Category SEO (GraphQL)")
def test_category_seo(
    config: Dict[str, Any], dataset: Dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to get category SEO...", end=" ")

    user_operations = UserOperations(graphql_client)
    categories_operations = CategoriesOperations(graphql_client)
    seo_operations = SeoOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]
    catalog = dataset["catalogs"][0]

    user = user_operations.get_me()

    categories_response = categories_operations.get_categories(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        filter=f"category.subtree:{catalog['id']}",
    )

    category_to_browse = next(
        category
        for category in dataset["categories"]
        if category["id"] == "category-acme-laptops"
    )

    category = categories_operations.get_category(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=currency,
        culture_name=culture,
        id=category_to_browse["id"],
    )

    seo_info = seo_operations.get_slug_info(
        store_id=config["store_id"],
        user_id=user["id"],
        culture_name=culture,
        slug=category["slug"],
    )

    category_breadcrumbs = category["breadcrumbs"][-1]

    assert category["seoInfo"] is not None, "SEO info is not found"
    assert category["seoInfo"]["semanticUrl"] is not None, "Semantic URL is not found"
    assert (
        seo_info["entityInfo"]["semanticUrl"] is not None
    ), "Semantic URL is not found"
    assert (
        category["seoInfo"]["semanticUrl"] == seo_info["entityInfo"]["semanticUrl"]
    ), "Semantic URL does not match"
    assert len(category["breadcrumbs"]) > 0, "Breadcrumbs are empty"
    assert category_breadcrumbs is not None, "Breadcrumb is not found"
