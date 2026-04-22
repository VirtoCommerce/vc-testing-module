from pydantic import BaseModel


class InputAddBulkItemsType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_new_bulk_item_type import InputNewBulkItemType

        self.cartId: str | None
        self.storeId: str
        self.cartName: str | None
        self.userId: str
        self.currencyCode: str | None
        self.cultureName: str | None
        self.cartType: str | None
        self.cartItems: list[InputNewBulkItemType]
