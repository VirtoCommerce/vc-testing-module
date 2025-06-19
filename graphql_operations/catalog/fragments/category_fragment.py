from graphql_operations.catalog.fragments.breadcrumb_fragment import BREADCRUMB_FRAGMENT
from graphql_operations.seo.fragments.seo_info_fragment import SEO_INFO_FRAGMENT


CATEGORY_FRAGMENT = f"""
    id
    name
    slug
    path
    seoInfo {{
        {SEO_INFO_FRAGMENT}
    }}
    breadcrumbs {{
        {BREADCRUMB_FRAGMENT}
    }}
"""
