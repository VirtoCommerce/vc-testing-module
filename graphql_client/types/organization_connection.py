from pydantic import BaseModel


class OrganizationConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.organization_edge import OrganizationEdge
        from graphql_client.types.organization import Organization

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[OrganizationEdge] | None
        self.items: list[Organization] | None
