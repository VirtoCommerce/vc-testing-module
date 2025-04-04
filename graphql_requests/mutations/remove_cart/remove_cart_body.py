from gql import gql


REMOVE_CART = gql(
    """
    mutation removeCart($command: InputRemoveCartType!) {
        removeCart(command: $command)
    }
    """
)
