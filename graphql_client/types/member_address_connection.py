from pydantic import BaseModel


class MemberAddressConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.member_address_edge import MemberAddressEdge
        from graphql_client.types.member_address_type import MemberAddressType

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[MemberAddressEdge] | None
        self.items: list[MemberAddressType] | None
