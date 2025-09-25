from gql import gql
from graphql_client.types.news_article_content_connection import NewsArticleContentConnection


class NewsArticlesQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> NewsArticleContentConnection:
        query_string = f"""
            query newsArticles($after: String, $first: Int, $keyword: String, $sort: String, $storeId: String!, $languageCode: String!, $userId: String, $authorId: String, $tags: [String]) {{
                newsArticles(
                    after: $after,
                    first: $first,
                    keyword: $keyword,
                    sort: $sort,
                    storeId: $storeId,
                    languageCode: $languageCode,
                    userId: $userId,
                    authorId: $authorId,
                    tags: $tags
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["newsArticles"]
