from tests_graphql.operations.quote.fragments.quote_item_fragment import QUOTE_ITEM_FRAGMENT
from tests_graphql.operations.common.address_fragment import ADDRESS_FRAGMENT

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
