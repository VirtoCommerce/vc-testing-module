from graphql_operations.catalog.fragments.availability_data_fragment import AVAILABILITY_DATA_FRAGMENT
from graphql_operations.catalog.fragments.breadcrumb_fragment import BREADCRUMB_FRAGMENT
from graphql_operations.seo.fragments.seo_info_fragment import SEO_INFO_FRAGMENT


PRODUCT_FRAGMENT = f"""
    id
    code
    name
    slug
    isConfigurable
    seoInfo {{
        {SEO_INFO_FRAGMENT}
    }}
    breadcrumbs {{
        {BREADCRUMB_FRAGMENT}
    }}
    availabilityData {{
        {AVAILABILITY_DATA_FRAGMENT}
    }}
"""
