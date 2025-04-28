from pydantic import BaseModel


class DictionaryItemConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.dictionary_item_edge import DictionaryItemEdge
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.dictionary_item_type import DictionaryItemType

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[DictionaryItemEdge] | None
        self.items: list[DictionaryItemType] | None
