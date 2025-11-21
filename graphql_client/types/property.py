from pydantic import BaseModel


class Property(BaseModel):
    def __init__(self):
        from graphql_client.types.property_value_types import PropertyValueTypes
        from graphql_client.types.property_group import PropertyGroup
        from graphql_client.types.property_dictionary_item_connection import PropertyDictionaryItemConnection
        from graphql_client.types.property_type import PropertyType

        self.id: str
        self.name: str
        self.hidden: bool
        self.multivalue: bool
        self.displayOrder: int | None
        self.label: str
        self.propertyType: PropertyType
        self.propertyValueType: PropertyValueTypes
        self.value: str | None
        self.valueDisplayOrder: int | None
        self.valueId: str | None
        self.colorCode: str | None
        self.group: PropertyGroup | None
        self.propertyDictionaryItems: PropertyDictionaryItemConnection | None
