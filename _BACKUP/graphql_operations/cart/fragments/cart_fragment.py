from graphql_operations.cart.fragments.cart_address_fragment import (
    CART_ADDRESS_FRAGMENT,
)
from graphql_operations.cart.fragments.coupon_fragment import COUPON_FRAGMENT
from graphql_operations.common.money_fragment import MONEY_FRAGMENT

CART_FRAGMENT = f"""
    id
    name
    customerId
    isAnonymous
    items {{
        id
        sku
        quantity
        productId
        selectedForCheckout
        discountTotal {{
            {MONEY_FRAGMENT}
        }}
        listPrice {{
            {MONEY_FRAGMENT}
        }}
        salePrice {{
            {MONEY_FRAGMENT}
        }}
        placedPrice {{
            {MONEY_FRAGMENT}
        }}
    }}
    coupons {{
        {COUPON_FRAGMENT}
    }}
    payments {{
        id
        paymentGatewayCode
        price {{
            {MONEY_FRAGMENT}
        }}
        billingAddress
            {CART_ADDRESS_FRAGMENT}
    }}
    shipments {{
        id
        shipmentMethodCode
        shipmentMethodOption
        price {{
            {MONEY_FRAGMENT}
        }}
        deliveryAddress
            {CART_ADDRESS_FRAGMENT}
    }}
    availablePaymentMethods {{
        code
        name
        price {{
            {MONEY_FRAGMENT}
        }}
    }}
    availableShippingMethods {{
        code
        name
        optionName
        price {{
            {MONEY_FRAGMENT}
        }}
    }}
    itemsQuantity
    discountTotal {{
        {MONEY_FRAGMENT}
    }}
    gifts {{
        id
        name
        productId
        quantity
    }}
    shippingTotal {{
        {MONEY_FRAGMENT}
    }}
    validationErrors {{
        errorCode
        errorMessage
    }}
"""
