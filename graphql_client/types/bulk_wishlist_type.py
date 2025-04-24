from pydantic import BaseModel


class BulkWishlistType(BaseModel):
    def __init__(self):
        from graphql_client.types.wishlist_type import WishlistType

        self.wishlists: list[WishlistType] | None
