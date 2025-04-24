from pydantic import BaseModel


class ProductAssociation(BaseModel):
    def __init__(self):
        from graphql_client.types.product import Product

        self.type: str
        self.priority: int
        self.quantity: int | None
        self.associatedObjectId: str | None
        self.associatedObjectType: str | None
        self.tags: list[str]
        self.product: Product | None
