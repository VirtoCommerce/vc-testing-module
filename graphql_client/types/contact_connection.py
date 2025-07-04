from pydantic import BaseModel


class ContactConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.contact_type import ContactType
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.contact_edge import ContactEdge

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[ContactEdge] | None
        self.items: list[ContactType] | None
