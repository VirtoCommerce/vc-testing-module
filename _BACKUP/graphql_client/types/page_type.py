from pydantic import BaseModel


class PageType(BaseModel):
    def __init__(self):

        self.id: str
        self.name: str | None
        self.relativeUrl: str
        self.permalink: str | None
        self.content: str
