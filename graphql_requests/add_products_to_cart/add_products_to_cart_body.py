from gql import gql

ADD_PRODUCTS_TO_CART = gql(
    """
    mutation AddItem($command: InputAddItemType!) {
        addItem(command: $command) {
            ...shortCart
            __typename
        }
    }
    
    fragment cartId on CartType {
        id
        __typename
    }
    
    fragment shortLineItem on LineItemType {
        id
        sku
        quantity
        productId
        extendedPrice {
            amount
            formattedAmount
            __typename
        }
        __typename
    }
    
    fragment validationError on ValidationErrorType {
        errorCode
        errorMessage
        errorParameters {
            key
            value
            __typename
        }
        objectId
        objectType
        __typename
    }
    
    fragment shortCart on CartType {
        ...cartId
        itemsQuantity
        items {
            ...shortLineItem
            __typename
        }
        validationErrors(ruleSet: "*") {
            ...validationError
            __typename
        }
        warnings {
            ...validationError
            __typename
        }
        __typename
    }
"""
)
