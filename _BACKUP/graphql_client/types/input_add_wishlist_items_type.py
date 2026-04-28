from pydantic import BaseModel


class InputAddWishlistItemsType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_new_wishlist_item_type import InputNewWishlistItemType

        self.listId: str
        self.listItems: list[InputNewWishlistItemType]
