from pydantic import BaseModel


class SharingSettingType(BaseModel):
    def __init__(self):
        from graphql_client.types.wishlist_access_type import WishlistAccessType
        from graphql_client.types.wishlist_scope_type import WishlistScopeType

        self.id: str
        self.scope: WishlistScopeType | None
        self.access: WishlistAccessType | None
        self.isOwner: bool
