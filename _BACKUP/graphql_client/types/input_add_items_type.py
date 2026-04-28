from pydantic import BaseModel


class InputAddItemsType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_new_cart_item_type import InputNewCartItemType

        self.cartId: str | None
        self.storeId: str
        self.cartName: str | None
        self.userId: str
        self.currencyCode: str | None
        self.cultureName: str | None
        self.cartType: str | None
        self.cartItems: list[InputNewCartItemType]
