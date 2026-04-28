from pydantic import BaseModel


class DynamicPropertyEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.dynamic_property_type import DynamicPropertyType

        self.cursor: str
        self.node: DynamicPropertyType | None
