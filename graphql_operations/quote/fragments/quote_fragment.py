from graphql_operations.common.address_fragment import ADDRESS_FRAGMENT
from graphql_operations.quote.fragments.quote_item_fragment import QUOTE_ITEM_FRAGMENT


QUOTE_FRAGMENT = f"""
    id
    comment
    customerId
    number
    status
    storeId
    items {{
        {QUOTE_ITEM_FRAGMENT}
    }}
    addresses {{
        {ADDRESS_FRAGMENT}
    }}
"""
