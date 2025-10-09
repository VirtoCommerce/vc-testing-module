from pydantic import BaseModel


class OpusOrganizationConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.opus_organization_edge import OpusOrganizationEdge
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.organization import Organization

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[OpusOrganizationEdge] | None
        self.items: list[Organization] | None
