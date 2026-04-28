from pydantic import BaseModel


class MenuLinkListType(BaseModel):
    def __init__(self):
        from graphql_client.types.menu_link_type import MenuLinkType

        self.name: str
        self.outerId: str | None
        self.items: list[MenuLinkType]
