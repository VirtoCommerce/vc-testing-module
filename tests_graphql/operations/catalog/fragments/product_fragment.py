from tests_graphql.operations.seo.fragments.seo_info_fragment import SEO_INFO_FRAGMENT
from tests_graphql.operations.catalog.fragments.breadcrumb_fragment import BREADCRUMB_FRAGMENT
from tests_graphql.operations.catalog.fragments.availability_data_fragment import AVAILABILITY_DATA_FRAGMENT


PRODUCT_FRAGMENT = f"""
    id
    code
    name
    slug
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
