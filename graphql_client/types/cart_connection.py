from pydantic import BaseModel


class CartConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.cart_edge import CartEdge
        from graphql_client.types.cart_type import CartType

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[CartEdge] | None
        self.items: list[CartType] | None
