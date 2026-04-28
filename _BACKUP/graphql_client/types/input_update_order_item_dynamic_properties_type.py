from pydantic import BaseModel


class InputUpdateOrderItemDynamicPropertiesType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_dynamic_property_value_type import InputDynamicPropertyValueType

        self.orderId: str | None
        self.lineItemId: str | None
        self.dynamicProperties: list[InputDynamicPropertyValueType]
