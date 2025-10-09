from pydantic import BaseModel


class InputAccountsPayableContactType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_accounts_payable_contact_address_type import InputAccountsPayableContactAddressType

        self.firstName: str
        self.lastName: str
        self.email: str
        self.phone: str | None
        self.address: InputAccountsPayableContactAddressType
