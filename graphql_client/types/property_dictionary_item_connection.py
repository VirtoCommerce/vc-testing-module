from pydantic import BaseModel


class PropertyDictionaryItemConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.property_dictionary_item_edge import PropertyDictionaryItemEdge
        from graphql_client.types.property_dictionary_item import PropertyDictionaryItem
        from graphql_client.types.page_info import PageInfo

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[PropertyDictionaryItemEdge] | None
        self.items: list[PropertyDictionaryItem] | None
