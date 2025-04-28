from pydantic import BaseModel


class PriceType(BaseModel):
    def __init__(self):
        from decimal import Decimal
        from graphql_client.types.tier_price_type import TierPriceType
        from graphql_client.types.money_type import MoneyType
        from datetime import datetime
        from graphql_client.types.catalog_discount_type import CatalogDiscountType

        self.list: MoneyType
        self.listWithTax: MoneyType
        self.sale: MoneyType
        self.saleWithTax: MoneyType
        self.actual: MoneyType
        self.actualWithTax: MoneyType
        self.discountAmount: MoneyType
        self.discountAmountWithTax: MoneyType
        self.discountPercent: Decimal
        self.currency: str
        self.startDate: datetime | None
        self.endDate: datetime | None
        self.tierPrices: list[TierPriceType]
        self.discounts: list[CatalogDiscountType]
        self.pricelistId: str | None
        self.minQuantity: int | None
