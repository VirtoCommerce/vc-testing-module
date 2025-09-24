from pydantic import BaseModel


class InputOrderPaymentType(BaseModel):
    def __init__(self):
        from decimal import Decimal
        from graphql_client.types.input_order_address_type import InputOrderAddressType
        from graphql_client.types.input_dynamic_property_value_type import InputDynamicPropertyValueType

        self.id: str | None
        self.outerId: str | None
        self.paymentGatewayCode: str | None
        self.currency: str | None
        self.price: Decimal | None
        self.amount: Decimal | None
        self.vendorId: str | None
        self.comment: str | None
        self.billingAddress: InputOrderAddressType | None
        self.dynamicProperties: list[InputDynamicPropertyValueType] | None
