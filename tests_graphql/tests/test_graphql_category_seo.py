import allure, os, pytest
from graphql_operations.catalog.categories_operations import CategoriesOperations
from graphql_operations.seo.seo_operations import SeoOperations
from graphql_operations.user.user_operations import UserOperations
from tests_graphql.test_data.test_catalog import TEST_CATALOG
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY


@pytest.mark.graphql
@allure.title("Category SEO (GraphQL)")
def test_category_seo(config, graphql_client):
    print(f"{os.linesep}Running test to get category SEO...", end=" ")

    user_operations = UserOperations(graphql_client)
    categories_operations = CategoriesOperations(graphql_client)
    seo_operations = SeoOperations(graphql_client)

    user = user_operations.get_user()

    categories_response = categories_operations.get_categories(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        filter=f"category.subtree:{TEST_CATALOG['id']}",
    )

    category_to_browse = categories_response["items"][0]

    category = categories_operations.get_category(
        store_id=config["store_id"],
        user_id=user["id"],
        currency_code=TEST_CURRENCY["USD"],
        culture_name=TEST_CULTURE["en-US"],
        id=category_to_browse["id"],
    )

    seo_info = seo_operations.get_slug_info(
        store_id=config["store_id"],
        user_id=user["id"],
        culture_name=TEST_CULTURE["en-US"],
        slug=category["slug"],
    )

    category_breadcrumbs = category["breadcrumbs"][-1]

    assert category["seoInfo"] is not None, "SEO info is not found"
    assert category["seoInfo"]["semanticUrl"] is not None, "Semantic URL is not found"
    assert seo_info["entityInfo"]["semanticUrl"] is not None, "Semantic URL is not found"
    assert category["seoInfo"]["semanticUrl"] == seo_info["entityInfo"]["semanticUrl"], "Semantic URL does not match"
    assert len(category["breadcrumbs"]) > 0, "Breadcrumbs are empty"
    assert category_breadcrumbs is not None, "Breadcrumb is not found"
