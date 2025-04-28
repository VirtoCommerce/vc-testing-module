from pydantic import BaseModel


class InputChangeCartItemsQuantityType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_cart_item_quantity_type import InputCartItemQuantityType

        self.cartId: str | None
        self.storeId: str
        self.cartName: str | None
        self.userId: str
        self.currencyCode: str | None
        self.cultureName: str | None
        self.cartType: str | None
        self.cartItems: list[InputCartItemQuantityType]
