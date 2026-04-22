from pydantic import BaseModel


class CreateQuoteCommandType(BaseModel):
    def __init__(self):

        self.storeId: str
        self.userId: str
        self.currencyCode: str
        self.cultureName: str
