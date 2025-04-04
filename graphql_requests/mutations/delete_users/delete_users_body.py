from gql import gql
from graphql_requests.graphql_import_resolver import resolve_imports


identity_result_fragment = resolve_imports("identity_result_fragment.graphql")

DELETE_USERS = gql(
    f"""
    {identity_result_fragment}

    mutation DeleteUsers($command: InputDeleteUserType!) {{
        deleteUsers(command: $command) {{
            ...IdentityResultFragment
        }}
    }}
    """
)
