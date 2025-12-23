from pydantic import BaseModel


class InputNewQuoteItemType(BaseModel):
    def __init__(self):
        from decimal import Decimal
        from graphql_client.types.input_dynamic_property_value_type import InputDynamicPropertyValueType

        self.productId: str | None
        self.name: str | None
        self.quantity: int
        self.price: Decimal | None
        self.comment: str | None
        self.dynamicProperties: list[InputDynamicPropertyValueType] | None
