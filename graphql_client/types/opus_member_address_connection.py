from pydantic import BaseModel


class OpusMemberAddressConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.opus_member_address_type import OpusMemberAddressType
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.opus_member_address_edge import OpusMemberAddressEdge

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[OpusMemberAddressEdge] | None
        self.items: list[OpusMemberAddressType] | None
