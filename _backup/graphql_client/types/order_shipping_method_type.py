from pydantic import BaseModel


class OrderShippingMethodType(BaseModel):
    def __init__(self):

        self.id: str
        self.code: str
        self.name: str | None
        self.description: str | None
        self.logoUrl: str | None
        self.isActive: bool
        self.priority: int
        self.taxType: str | None
        self.storeId: str | None
        self.typeName: str | None
