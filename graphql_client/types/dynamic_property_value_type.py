from pydantic import BaseModel


class DynamicPropertyValueType(BaseModel):
    def __init__(self):
        from graphql_client.types.dynamic_property_type import DynamicPropertyType
        from graphql_client.types.dynamic_property_value_types import DynamicPropertyValueTypes
        from graphql_client.types.dictionary_item_type import DictionaryItemType

        self.name: str | None
        self.valueType: str
        self.dynamicPropertyValueType: DynamicPropertyValueTypes
        self.value: str | None
        self.dictionaryItem: DictionaryItemType | None
        self.dynamicProperty: DynamicPropertyType | None
