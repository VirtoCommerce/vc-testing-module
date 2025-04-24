from pydantic import BaseModel


class CurrencyType(BaseModel):
    def __init__(self):
        from decimal import Decimal

        self.code: str
        self.symbol: str
        self.exchangeRate: Decimal
        self.customFormatting: str | None
        self.englishName: str
        self.cultureName: str
