from pydantic import BaseModel


class InputUpdateOrderShipmentDynamicPropertiesType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_dynamic_property_value_type import InputDynamicPropertyValueType

        self.orderId: str | None
        self.shipmentId: str | None
        self.dynamicProperties: list[InputDynamicPropertyValueType]
