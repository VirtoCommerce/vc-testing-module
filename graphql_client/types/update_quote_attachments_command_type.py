from pydantic import BaseModel


class UpdateQuoteAttachmentsCommandType(BaseModel):
    def __init__(self):

        self.quoteId: str
        self.urls: list[str]
