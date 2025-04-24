from tests_graphql.operations.cart.cart_address_fragment import CART_ADDRESS_FRAGMENT


CART_FRAGMENT = f"""
    id
    customerId
    isAnonymous
    items {{
        id
        sku
        quantity
        productId
        selectedForCheckout
    }}
    payments {{
        id
        paymentGatewayCode
        price {{
            amount
        }}
        billingAddress
            {CART_ADDRESS_FRAGMENT}
    }}
    shipments {{
        id
        shipmentMethodCode
        shipmentMethodOption
        price {{
            amount
        }}
        deliveryAddress
            {CART_ADDRESS_FRAGMENT}
    }}
    availablePaymentMethods {{
        code
        name
        price {{
            amount
        }}
    }}
    availableShippingMethods {{
        code
        name
        optionName
        price {{
            amount
        }}
    }}
    itemsQuantity
"""
