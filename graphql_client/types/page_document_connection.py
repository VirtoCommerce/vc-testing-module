from pydantic import BaseModel


class PageDocumentConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.page_document_edge import PageDocumentEdge
        from graphql_client.types.page_document_type import PageDocumentType

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[PageDocumentEdge] | None
        self.items: list[PageDocumentType] | None
