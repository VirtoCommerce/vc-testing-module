from pydantic import BaseModel


class InputChangeCartConfiguredItemType(BaseModel):
    def __init__(self):
        from graphql_client.types.configuration_section_input import ConfigurationSectionInput

        self.cartId: str | None
        self.storeId: str
        self.cartName: str | None
        self.userId: str
        self.currencyCode: str | None
        self.cultureName: str | None
        self.cartType: str | None
        self.lineItemId: str
        self.quantity: int | None
        self.configurationSections: list[ConfigurationSectionInput] | None
