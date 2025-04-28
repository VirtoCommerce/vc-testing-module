from pydantic import BaseModel


class InputNewCartItemType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_dynamic_property_value_type import InputDynamicPropertyValueType

        self.productId: str
        self.quantity: int | None
        self.dynamicProperties: list[InputDynamicPropertyValueType] | None
