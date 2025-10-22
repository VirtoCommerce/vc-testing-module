from pydantic import BaseModel


class InputRequestRegistrationType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_register_account_type import InputRegisterAccountType
        from graphql_client.types.input_register_organization_type import InputRegisterOrganizationType
        from graphql_client.types.input_register_contact_type import InputRegisterContactType

        self.storeId: str
        self.languageCode: str | None
        self.organization: InputRegisterOrganizationType | None
        self.contact: InputRegisterContactType
        self.account: InputRegisterAccountType
