from gql import gql
from graphql_requests.graphql_import_resolver import resolve_imports


user_fragment = resolve_imports("user_fragment.graphql")

ME = gql(
    f"""
    {user_fragment}

    query Me($userId: String) {{
        me(userId: $userId) {{
            ...UserFragment
        }}
    }}
    """
)
