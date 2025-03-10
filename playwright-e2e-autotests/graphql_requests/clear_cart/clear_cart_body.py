from gql import gql

CLEAR_CART = gql(
    """
    mutation ClearCart($command: InputClearCartType!, $skipQuery: Boolean!) {
        clearCart(command: $command) {
            ...fullCart @skip(if: $skipQuery)
            __typename
        }
    }

    fragment cartId on CartType {
        id
        __typename
    }

    fragment fullCart on CartType {
        ...cartId
        itemsQuantity
        items {
            id
            sku
            quantity
            productId
        }
        __typename
    }
"""
)
