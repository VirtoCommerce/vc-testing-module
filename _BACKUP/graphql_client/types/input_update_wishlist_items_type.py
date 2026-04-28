from pydantic import BaseModel


class InputUpdateWishlistItemsType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_update_wishlist_line_item_type import InputUpdateWishlistLineItemType

        self.listId: str
        self.items: list[InputUpdateWishlistLineItemType]
