from pydantic import BaseModel


class QuoteItemType(BaseModel):
    def __init__(self):
        from graphql_client.types.money_type import MoneyType
        from graphql_client.types.quote_tier_price_type import QuoteTierPriceType
        from graphql_client.types.product import Product
        from graphql_client.types.quote_tier_price_type import QuoteTierPriceType

        self.id: str
        self.sku: str | None
        self.productId: str | None
        self.catalogId: str | None
        self.categoryId: str | None
        self.name: str
        self.comment: str | None
        self.imageUrl: str | None
        self.taxType: str | None
        self.quantity: int
        self.listPrice: MoneyType
        self.salePrice: MoneyType
        self.selectedTierPrice: QuoteTierPriceType | None
        self.proposalPrices: list[QuoteTierPriceType]
        self.product: Product | None
