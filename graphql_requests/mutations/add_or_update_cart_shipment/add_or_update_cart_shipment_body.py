from gql import gql
from graphql_requests.graphql_import_resolver import resolve_imports


cart_fragment = resolve_imports("cart_fragment.graphql")

ADD_OR_UPDATE_CART_SHIPMENT = gql(
    f"""
    {cart_fragment}

    mutation AddOrUpdateCartShipment($command: InputAddOrUpdateCartShipmentType!) {{
        addOrUpdateCartShipment(command: $command) {{
            ...CartFragment
        }}
    }}
    """
)
