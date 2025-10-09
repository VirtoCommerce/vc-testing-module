from pydantic import BaseModel


class InputQuoteReferralInfoType(BaseModel):
    def __init__(self):

        self.productId: str | None
        self.productCode: str | None
        self.productName: str | None
        self.searchPhrase: str | None
        self.categoryId: str | None
        self.categoryName: str | None
        self.location: str | None
