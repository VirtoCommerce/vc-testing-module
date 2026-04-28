from pydantic import BaseModel


class DynamicPropertyType(BaseModel):
    def __init__(self):
        from graphql_client.types.dictionary_item_connection import DictionaryItemConnection
        from graphql_client.types.dynamic_property_value_types import DynamicPropertyValueTypes

        self.id: str
        self.name: str
        self.objectType: str
        self.label: str | None
        self.displayOrder: int | None
        self.dynamicPropertyValueType: DynamicPropertyValueTypes
        self.isArray: bool
        self.isDictionary: bool
        self.isMultilingual: bool
        self.isRequired: bool
        self.dictionaryItems: DictionaryItemConnection | None
