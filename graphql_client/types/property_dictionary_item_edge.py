from pydantic import BaseModel


class PropertyDictionaryItemEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.property_dictionary_item import PropertyDictionaryItem

        self.cursor: str
        self.node: PropertyDictionaryItem | None
