from pydantic import BaseModel


class OutlineType(BaseModel):
    def __init__(self):
        from graphql_client.types.outline_item_type import OutlineItemType

        self.items: list[OutlineItemType] | None
