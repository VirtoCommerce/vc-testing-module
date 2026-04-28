from gql import gql
from graphql_client.types.news_article_author import NewsArticleAuthor


class NewsArticleAuthorQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> NewsArticleAuthor:
        query_string = f"""
            query newsArticleAuthor($authorId: String!) {{
                newsArticleAuthor(
                    authorId: $authorId
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["newsArticleAuthor"]
