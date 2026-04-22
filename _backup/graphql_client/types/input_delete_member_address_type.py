from pydantic import BaseModel


class InputDeleteMemberAddressType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_member_address_type import InputMemberAddressType

        self.memberId: str
        self.addresses: list[InputMemberAddressType]
