from pydantic import BaseModel


class PageEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.page_type import PageType

        self.cursor: str
        self.node: PageType | None
