from pydantic import BaseModel


class QuoteAttachmentType(BaseModel):
    def __init__(self):

        self.name: str
        self.url: str
        self.contentType: str | None
        self.size: int
