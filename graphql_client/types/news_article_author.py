from pydantic import BaseModel


class NewsArticleAuthor(BaseModel):
    def __init__(self):

        self.id: str
        self.name: str | None
        self.iconUrl: str | None
