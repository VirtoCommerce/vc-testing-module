from pydantic import BaseModel


class InputCreateConfiguredLineItemCommand(BaseModel):
    def __init__(self):
        from graphql_client.types.configuration_section_input import ConfigurationSectionInput

        self.storeId: str | None
        self.currencyCode: str | None
        self.cultureName: str | None
        self.configurableProductId: str
        self.configurationSections: list[ConfigurationSectionInput] | None
