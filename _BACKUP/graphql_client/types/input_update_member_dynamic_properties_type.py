from pydantic import BaseModel


class InputUpdateMemberDynamicPropertiesType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_dynamic_property_value_type import InputDynamicPropertyValueType

        self.memberId: str
        self.dynamicProperties: list[InputDynamicPropertyValueType]
