from gql import Client
from typing import Optional
from graphql_client.queries.slug_info import SlugInfoQuery
from graphql_client.types.slug_info_response_type import SlugInfoResponseType
from graphql_operations.seo.fragments.seo_info_fragment import SEO_INFO_FRAGMENT


class SeoOperations:
    def __init__(self, graphql_client: Client):
        self.graphql_client = graphql_client

    def get_slug_info(
        self,
        store_id: str,
        user_id: str,
        culture_name: str,
        slug: str,
        permalink: Optional[str] = None,
    ) -> SlugInfoResponseType:
        slug_info_query = SlugInfoQuery(self.graphql_client)

        variables = {
            "storeId": store_id,
            "userId": user_id,
            "cultureName": culture_name,
            "slug": slug,
            "permalink": permalink,
        }

        return_fields = f"""
            entityInfo {{
                {SEO_INFO_FRAGMENT}
            }}
        """

        result = slug_info_query.execute(variables=variables, return_fields=return_fields)

        return result
