from gql import gql
from graphql_requests.graphql_import_resolver import resolve_imports


register_organization_fragment = resolve_imports("register_organization_fragment.graphql")
register_contact_fragment = resolve_imports("register_contact_fragment.graphql")
register_account_fragment = resolve_imports("register_account_fragment.graphql")
account_creation_result_fragment = resolve_imports("account_creation_result_fragment.graphql")

REQUEST_REGISTRATION = gql(
    f"""
    {register_organization_fragment}
    {register_contact_fragment}
    {register_account_fragment}
    {account_creation_result_fragment}

    mutation RequestRegistration($command: InputRequestRegistrationType!) {{
        requestRegistration(command: $command) {{
            organization {{
                ...RegisterOrganizationFragment
            }}
            contacts {{
                ...RegisterContactFragment
            }}
            account {{
                ...RegisterAccountFragment
            }}
            result {{
                ...AccountCreationResultFragment
            }}
        }}
    }}
    """
)
