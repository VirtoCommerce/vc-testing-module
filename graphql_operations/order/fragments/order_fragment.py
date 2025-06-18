ORDER_FRAGMENT = f"""
    id
    number
    customerId
    createdDate
    items {{
        id
        productId
        quantity
    }}
    total {{
        amount
    }}
"""
