from gql import gql
from graphql_requests.graphql_import_resolver import resolve_imports


cart_fragment = resolve_imports("cart_fragment.graphql")

REMOVE_SHIPMENT = gql(
    f"""
    {cart_fragment}

    mutation removeShipment($command: InputRemoveShipmentType!) {{
        removeShipment(command: $command) {{
            ...CartFragment
        }}
    }}
    """
)
