from gql import gql
from graphql_requests.graphql_import_resolver import resolve_imports


customer_order_fragment = resolve_imports("customer_order_fragment.graphql")

ORDER = gql(
    f"""
    {customer_order_fragment}

    query GetFullOrder($id: String!) {{
        order(id: $id) {{
            ...CustomerOrderFragment
        }}
    }}
    """
)
