from pydantic import BaseModel


class InputUpdateOrderDynamicPropertiesType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_dynamic_property_value_type import InputDynamicPropertyValueType

        self.orderId: str | None
        self.dynamicProperties: list[InputDynamicPropertyValueType]
