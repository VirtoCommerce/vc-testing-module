from pydantic import BaseModel


class ConfigurationSectionInput(BaseModel):
    def __init__(self):
        from graphql_client.types.configurable_product_option_input import ConfigurableProductOptionInput

        self.sectionId: str
        self.type: str
        self.option: ConfigurableProductOptionInput | None
        self.customText: str | None
        self.fileUrls: list[str] | None
