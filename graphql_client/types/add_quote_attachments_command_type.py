from pydantic import BaseModel


class AddQuoteAttachmentsCommandType(BaseModel):
    def __init__(self):

        self.quoteId: str
        self.urls: list[str]
