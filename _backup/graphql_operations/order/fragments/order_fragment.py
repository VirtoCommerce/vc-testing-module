ORDER_FRAGMENT = f"""
    id
    number
    customerId
    createdDate
    status
    items {{
        id
        productId
        quantity
    }}
    shipments {{
        shipmentMethodCode
        shipmentMethodOption
    }}
    total {{
        amount
    }}
"""
