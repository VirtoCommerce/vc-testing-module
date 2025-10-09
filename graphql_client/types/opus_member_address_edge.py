from pydantic import BaseModel


class OpusMemberAddressEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.opus_member_address_type import OpusMemberAddressType

        self.cursor: str
        self.node: OpusMemberAddressType | None
