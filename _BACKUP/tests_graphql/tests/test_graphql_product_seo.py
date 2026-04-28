import os
from typing import Any

import allure
import pytest

from fixtures.config import Config
from fixtures.graphql_client import GraphQLClient
from graphql_operations.catalog.products_operations import ProductsOperations
from graphql_operations.seo.seo_operations import SeoOperations
from graphql_operations.user.user_operations import UserOperations


@pytest.mark.graphql
@allure.title("Product SEO (GraphQL)")
def test_product_seo(
    config: Config, dataset: dict[str, Any], graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running test to get product SEO...", end=" ")

    user_operations = UserOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)
    seo_operations = SeoOperations(graphql_client)

    currency = dataset["currencies"][0]["code"]
    culture = dataset["languages"][0]["allowedValues"][0]
    product = dataset["products"][1]

    user = user_operations.get_me()

    product = products_operations.get_product(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        culture_name=culture,
        currency_code=currency,
        id=product["id"],
    )

    seo_info = seo_operations.get_slug_info(
        store_id=config["STORE_ID"],
        user_id=user["id"],
        culture_name=culture,
        slug=product["slug"],
    )

    product_breadcrumbs = product["breadcrumbs"][-1]

    assert product["seoInfo"] is not None, "SEO info is not found"
    assert product["seoInfo"]["semanticUrl"] is not None, "Semantic URL is not found"
    assert (
        seo_info["entityInfo"]["semanticUrl"] is not None
    ), "Semantic URL is not found"
    assert (
        product["seoInfo"]["semanticUrl"] == seo_info["entityInfo"]["semanticUrl"]
    ), "Semantic URL does not match"
    assert len(product["breadcrumbs"]) > 0, "Breadcrumbs are empty"
    assert product_breadcrumbs is not None, "Breadcrumb is not found"
