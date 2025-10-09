from pydantic import BaseModel


class QuoteReferralInfoType(BaseModel):
    def __init__(self):

        self.categoryId: str | None
        self.categoryName: str | None
        self.location: str | None
        self.productCode: str | None
        self.productId: str | None
        self.productName: str | None
        self.searchPhrase: str | None
