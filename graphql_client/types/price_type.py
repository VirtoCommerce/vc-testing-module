from pydantic import BaseModel


class PriceType(BaseModel):
    def __init__(self):
        from graphql_client.types.money_type import MoneyType
        from graphql_client.types.tier_price_type import TierPriceType
        from graphql_client.types.catalog_discount_type import CatalogDiscountType
        from datetime import datetime
        from decimal import Decimal

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
