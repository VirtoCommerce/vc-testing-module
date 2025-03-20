from gql import gql

CREATE_ORDER_FROM_CART = gql(
    """
    mutation CreateOrderFromCart($command: InputCreateOrderFromCartType!) {
        createOrderFromCart(command: $command) {
            id
            number
            items {
                productId
                name
                sku
                quantity
            }
        }
    }
    """
)
