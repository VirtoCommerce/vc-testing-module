from pydantic import BaseModel


class ConfigurationSectionType(BaseModel):
    def __init__(self):
        from graphql_client.types.configuration_line_item_type import ConfigurationLineItemType

        self.id: str
        self.name: str | None
        self.description: str | None
        self.isRequired: bool
        self.type: str
        self.allowCustomText: bool
        self.allowTextOptions: bool
        self.options: list[ConfigurationLineItemType] | None
