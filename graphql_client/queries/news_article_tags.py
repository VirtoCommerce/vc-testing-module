from gql import gql
from graphql_client.types.str import str


class NewsArticleTagsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> list[str]:
        query_string = f"""
            query newsArticleTags($languageCode: String!) {{
                newsArticleTags(
                    languageCode: $languageCode
                )
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["newsArticleTags"]
