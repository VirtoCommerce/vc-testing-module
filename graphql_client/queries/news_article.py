from gql import gql
from graphql_client.types.news_article_content import NewsArticleContent


class NewsArticleQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> NewsArticleContent:
        query_string = f"""
            query newsArticle($id: String!, $storeId: String!, $languageCode: String!) {{
                newsArticle(
                    id: $id,
                    storeId: $storeId,
                    languageCode: $languageCode
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["newsArticle"]
