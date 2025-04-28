from pydantic import BaseModel


class DictionaryItemEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.dictionary_item_type import DictionaryItemType

        self.cursor: str
        self.node: DictionaryItemType | None
