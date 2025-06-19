from pydantic import BaseModel


class StoreSettingsType(BaseModel):
    def __init__(self):
        from graphql_client.types.password_options_type import PasswordOptionsType
        from graphql_client.types.module_settings_type import ModuleSettingsType

        self.quotesEnabled: bool
        self.subscriptionEnabled: bool
        self.isSpa: bool
        self.createAnonymousOrderEnabled: bool
        self.defaultSelectedForCheckout: bool
        self.taxCalculationEnabled: bool
        self.anonymousUsersAllowed: bool
        self.emailVerificationEnabled: bool
        self.emailVerificationRequired: bool
        self.seoLinkType: str
        self.environmentName: str
        self.passwordRequirements: PasswordOptionsType | None
        self.authenticationTypes: list[str]
        self.modules: list[ModuleSettingsType]
