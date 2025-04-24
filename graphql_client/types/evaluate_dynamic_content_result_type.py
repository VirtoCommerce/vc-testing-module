from pydantic import BaseModel


class EvaluateDynamicContentResultType(BaseModel):
    def __init__(self):
        from graphql_client.types.dynamic_content_item_type import DynamicContentItemType

        self.totalCount: int
        self.items: list[DynamicContentItemType] | None
