import time

import allure
import pytest
from gql import gql
from gql.transport.exceptions import TransportQueryError

from fixtures.config import Config
from fixtures.graphql_client import GraphQLClient


PRODUCTS_READINESS_QUERY = gql(
    """
    query productsReadinessCheck($storeId: String!) {
        products(storeId: $storeId, first: 1) {
            totalCount
        }
    }
"""
)

PAGE_CONTEXT_READINESS_QUERY = gql(
    """
    query pageContextReadinessCheck($storeId: String!, $permalink: String) {
        pageContext(storeId: $storeId, permalink: $permalink) {
            store {
                storeId
            }
        }
    }
"""
)

SLUG_INFO_READINESS_QUERY = gql(
    """
    query slugInfoReadinessCheck($storeId: String!, $slug: String) {
        slugInfo(storeId: $storeId, slug: $slug) {
            entityInfo {
                objectType
            }
        }
    }
"""
)


def _check_query(graphql_client, query, variables, label):
    """Execute a query and return (success, message)."""
    try:
        graphql_client.execute(query, variables)
        return True, f"{label}: OK"
    except TransportQueryError as e:
        return False, f"{label}: {e}"
    except Exception as e:
        return False, f"{label}: {e}"


@pytest.fixture(scope="session", autouse=True)
@allure.title("Fixture to verify search index readiness")
def search_readiness(config: Config, graphql_client: GraphQLClient):
    max_attempts = 15
    delay_seconds = 3

    store_id = config["STORE_ID"]

    checks = [
        (PRODUCTS_READINESS_QUERY, {"storeId": store_id, "first": 1}, "products"),
        (PAGE_CONTEXT_READINESS_QUERY, {"storeId": store_id, "permalink": "/"}, "pageContext"),
        (SLUG_INFO_READINESS_QUERY, {"storeId": store_id, "slug": "/"}, "slugInfo"),
    ]

    for attempt in range(1, max_attempts + 1):
        results = []
        all_ok = True

        for query, variables, label in checks:
            ok, msg = _check_query(graphql_client, query, variables, label)
            results.append(msg)
            if not ok:
                all_ok = False

        status = "; ".join(results)

        if all_ok:
            print(f"\nSearch index is ready (attempt {attempt}): {status}")
            return

        print(f"\nSearch index not ready (attempt {attempt}/{max_attempts}): {status}")

        if attempt < max_attempts:
            time.sleep(delay_seconds)

    pytest.fail(
        f"Search index not ready after {max_attempts} attempts ({max_attempts * delay_seconds}s). "
        f"Last status: {status}"
    )
