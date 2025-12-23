from pydantic import BaseModel


class PageDocumentType(BaseModel):
    def __init__(self):

        self.id: str
        self.title: str | None
        self.source: str | None
        self.permalink: str | None
        self.content: str
