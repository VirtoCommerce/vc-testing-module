from pydantic import BaseModel


class NewsArticleContentConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.news_article_content import NewsArticleContent
        from graphql_client.types.news_article_content_edge import NewsArticleContentEdge
        from graphql_client.types.page_info import PageInfo

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[NewsArticleContentEdge] | None
        self.items: list[NewsArticleContent] | None
