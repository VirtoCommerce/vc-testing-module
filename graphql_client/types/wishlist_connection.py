from pydantic import BaseModel


class WishlistConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.wishlist_type import WishlistType
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.wishlist_edge import WishlistEdge

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[WishlistEdge] | None
        self.items: list[WishlistType] | None
