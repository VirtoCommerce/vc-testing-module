from pydantic import BaseModel


class GiftItemType(BaseModel):
    def __init__(self):
        from graphql_client.types.product import Product

        self.promotionId: str
        self.quantity: int
        self.productId: str | None
        self.categoryId: str | None
        self.imageUrl: str | None
        self.name: str
        self.measureUnit: str | None
        self.lineItemId: str | None
        self.id: str
        self.product: Product | None
