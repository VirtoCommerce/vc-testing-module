from pydantic import BaseModel


class DynamicContentItemType(BaseModel):
    def __init__(self):
        from graphql_client.types.dynamic_property_value_type import DynamicPropertyValueType

        self.id: str
        self.contentType: str
        self.name: str
        self.description: str
        self.priority: int
        self.dynamicProperties: list[DynamicPropertyValueType] | None
