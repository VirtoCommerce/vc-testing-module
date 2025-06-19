from graphql_operations.cart.fragments.cart_address_fragment import CART_ADDRESS_FRAGMENT
from graphql_operations.cart.fragments.coupon_fragment import COUPON_FRAGMENT


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
    coupons {{
        {COUPON_FRAGMENT}
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
    discountTotal {{
        amount
    }}
    gifts {{
        id
        name
        productId
        quantity
    }}
"""
