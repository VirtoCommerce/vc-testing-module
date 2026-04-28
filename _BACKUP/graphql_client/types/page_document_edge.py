from pydantic import BaseModel


class PageDocumentEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.page_document_type import PageDocumentType

        self.cursor: str
        self.node: PageDocumentType | None
