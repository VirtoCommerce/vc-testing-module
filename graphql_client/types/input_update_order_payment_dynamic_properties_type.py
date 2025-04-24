from pydantic import BaseModel


class InputUpdateOrderPaymentDynamicPropertiesType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_dynamic_property_value_type import InputDynamicPropertyValueType

        self.orderId: str | None
        self.paymentId: str | None
        self.dynamicProperties: list[InputDynamicPropertyValueType]
