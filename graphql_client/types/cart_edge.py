from pydantic import BaseModel


class CartEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.cart_type import CartType

        self.cursor: str
        self.node: CartType | None
