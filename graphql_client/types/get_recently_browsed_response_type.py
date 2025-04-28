from pydantic import BaseModel


class GetRecentlyBrowsedResponseType(BaseModel):
    def __init__(self):
        from graphql_client.types.product import Product

        self.products: list[Product] | None
