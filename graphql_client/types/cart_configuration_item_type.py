from pydantic import BaseModel


class CartConfigurationItemType(BaseModel):
    def __init__(self):
        from graphql_client.types.cart_configuration_item_file_type import CartConfigurationItemFileType

        self.id: str
        self.name: str | None
        self.sectionId: str
        self.productId: str | None
        self.quantity: int | None
        self.customText: str | None
        self.type: str
        self.files: list[CartConfigurationItemFileType] | None
