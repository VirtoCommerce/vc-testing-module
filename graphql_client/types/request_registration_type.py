from pydantic import BaseModel


class RequestRegistrationType(BaseModel):
    def __init__(self):
        from graphql_client.types.register_account_type import RegisterAccountType
        from graphql_client.types.register_contact_type import RegisterContactType
        from graphql_client.types.register_organization_type import RegisterOrganizationType
        from graphql_client.types.account_creation_result_type import AccountCreationResultType

        self.organization: RegisterOrganizationType | None
        self.contact: RegisterContactType | None
        self.account: RegisterAccountType | None
        self.result: AccountCreationResultType | None
