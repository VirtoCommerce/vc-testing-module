from pydantic import BaseModel


class NewsArticleContent(BaseModel):
    def __init__(self):
        from graphql_client.types.seo_info import SeoInfo
        from datetime import datetime
        from graphql_client.types.news_article_author import NewsArticleAuthor

        self.id: str
        self.publishDate: datetime | None
        self.isArchived: bool
        self.title: str | None
        self.content: str | None
        self.contentPreview: str | None
        self.listTitle: str | None
        self.listPreview: str | None
        self.tags: list[str] | None
        self.seoInfo: SeoInfo
        self.author: NewsArticleAuthor | None
