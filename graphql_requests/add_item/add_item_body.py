from gql import gql

ADD_ITEM = gql(
    """
    mutation AddItem($command: InputAddItemType!) {
        addItem(command: $command) {
            id
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
