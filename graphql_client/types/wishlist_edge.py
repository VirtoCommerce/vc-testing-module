from pydantic import BaseModel


class WishlistEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.wishlist_type import WishlistType

        self.cursor: str
        self.node: WishlistType | None
