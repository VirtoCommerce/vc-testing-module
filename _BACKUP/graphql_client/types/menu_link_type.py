from pydantic import BaseModel


class MenuLinkType(BaseModel):
    def __init__(self):
        from graphql_client.types.menu_link_type import MenuLinkType

        self.title: str
        self.url: str
        self.priority: int
        self.associatedObjectId: str | None
        self.associatedObjectName: str | None
        self.associatedObjectType: str | None
        self.outerId: str | None
        self.childItems: list[MenuLinkType]
