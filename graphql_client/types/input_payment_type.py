from pydantic import BaseModel


class InputPaymentType(BaseModel):
    def __init__(self):
        from decimal import Decimal

        from graphql_client.types.input_address_type import InputAddressType
        from graphql_client.types.input_dynamic_property_value_type import (
            InputDynamicPropertyValueType,
        )

        self.id: str | None
        self.outerId: str | None
        self.paymentGatewayCode: str | None
        self.billingAddress: InputAddressType | None
        self.purpose: str | None
        self.currency: str | None
        self.price: Decimal | None
        self.amount: Decimal | None
        self.vendorId: str | None
        self.comment: str | None
        self.dynamicProperties: list[InputDynamicPropertyValueType] | None
