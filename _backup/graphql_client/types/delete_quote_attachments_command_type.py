from pydantic import BaseModel


class DeleteQuoteAttachmentsCommandType(BaseModel):
    def __init__(self):

        self.quoteId: str
        self.urls: list[str]
