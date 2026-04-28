from pydantic import BaseModel


class ConfigurationQueryResponseType(BaseModel):
    def __init__(self):
        from graphql_client.types.configuration_section_type import ConfigurationSectionType

        self.configurationSections: list[ConfigurationSectionType] | None
