from pydantic import BaseModel


class InputUpdateAccountsPayableContactType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_accounts_payable_contact_type import InputAccountsPayableContactType

        self.accountsPayableContact: InputAccountsPayableContactType
