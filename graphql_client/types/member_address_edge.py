from pydantic import BaseModel


class MemberAddressEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.member_address_type import MemberAddressType

        self.cursor: str
        self.node: MemberAddressType | None
