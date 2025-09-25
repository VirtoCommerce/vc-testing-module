from pydantic import BaseModel


class NewsArticleContentEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.news_article_content import NewsArticleContent

        self.cursor: str
        self.node: NewsArticleContent | None
