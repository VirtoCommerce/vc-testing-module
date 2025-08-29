from pydantic import BaseModel


class CartWithListType(BaseModel):
    def __init__(self):
        from graphql_client.types.cart_type import CartType

        self.cart: CartType | None
        self.list: CartType | None
