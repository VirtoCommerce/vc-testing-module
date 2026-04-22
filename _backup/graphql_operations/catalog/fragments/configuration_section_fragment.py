from graphql_operations.catalog.fragments.configuration_line_item_fragment import CONFIGURATION_LINE_ITEM_FRAGMENT

CONFIGURATION_SECTION_FRAGMENT = f"""
    id
    name
    description
    isRequired
    type
    allowCustomText
    allowTextOptions
    options {{
        {CONFIGURATION_LINE_ITEM_FRAGMENT}
    }}
"""
