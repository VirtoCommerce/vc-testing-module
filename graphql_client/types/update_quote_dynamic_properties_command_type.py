from pydantic import BaseModel


class UpdateQuoteDynamicPropertiesCommandType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_dynamic_property_value_type import InputDynamicPropertyValueType

        self.quoteId: str
        self.dynamicProperties: list[InputDynamicPropertyValueType]
