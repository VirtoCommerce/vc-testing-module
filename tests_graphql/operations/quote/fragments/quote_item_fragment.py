QUOTE_ITEM_FRAGMENT = f"""
    id
    sku
    productId
    name
    quantity
    selectedTierPrice {{
        quantity
        price {{
            amount
        }}
    }}
    proposalPrices {{
        quantity
        price {{
            amount
        }}
    }}
"""
