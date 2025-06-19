import allure, os, pytest
from graphql_operations.user.user_operations import UserOperations
from graphql_operations.catalog.products_operations import ProductsOperations
from graphql_operations.seo.seo_operations import SeoOperations
from tests_graphql.test_data.test_culture import TEST_CULTURE
from tests_graphql.test_data.test_currency import TEST_CURRENCY
from tests_graphql.test_data.test_product import TEST_PRODUCT_1


@pytest.mark.graphql
@allure.title("Product SEO (GraphQL)")
def test_product_seo(config, graphql_client):
    print(f"{os.linesep}Running test to get product SEO...", end=" ")

    user_operations = UserOperations(graphql_client)
    products_operations = ProductsOperations(graphql_client)
    seo_operations = SeoOperations(graphql_client)

    user = user_operations.get_user()

    product = products_operations.get_product(
        store_id=config["store_id"],
        user_id=user["id"],
        culture_name=TEST_CULTURE["en-US"],
        currency_code=TEST_CURRENCY["USD"],
        id=TEST_PRODUCT_1["id"],
    )

    seo_info = seo_operations.get_slug_info(
        store_id=config["store_id"],
        user_id=user["id"],
        culture_name=TEST_CULTURE["en-US"],
        slug=product["slug"],
    )

    product_breadcrumbs = product["breadcrumbs"][-1]

    assert product["seoInfo"] is not None, "SEO info is not found"
    assert product["seoInfo"]["semanticUrl"] is not None, "Semantic URL is not found"
    assert seo_info["entityInfo"]["semanticUrl"] is not None, "Semantic URL is not found"
    assert product["seoInfo"]["semanticUrl"] == seo_info["entityInfo"]["semanticUrl"], "Semantic URL does not match"
    assert len(product["breadcrumbs"]) > 0, "Breadcrumbs are empty"
    assert product_breadcrumbs is not None, "Breadcrumb is not found"
