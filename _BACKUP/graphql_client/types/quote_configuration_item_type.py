from pydantic import BaseModel


class QuoteConfigurationItemType(BaseModel):
    def __init__(self):
        from graphql_client.types.quote_configuration_item_file_type import QuoteConfigurationItemFileType

        self.id: str
        self.name: str | None
        self.type: str
        self.customText: str | None
        self.files: list[QuoteConfigurationItemFileType] | None
