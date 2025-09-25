from pydantic import BaseModel


class InputShipmentType(BaseModel):
    def __init__(self):
        from decimal import Decimal

        from graphql_client.types.input_address_type import InputAddressType
        from graphql_client.types.input_dynamic_property_value_type import (
            InputDynamicPropertyValueType,
        )

        self.id: str | None
        self.fulfillmentCenterId: str | None
        self.height: Decimal | None
        self.length: Decimal | None
        self.measureUnit: str | None
        self.shipmentMethodCode: str | None
        self.shipmentMethodOption: str | None
        self.volumetricWeight: Decimal | None
        self.weight: Decimal | None
        self.weightUnit: str | None
        self.width: Decimal | None
        self.deliveryAddress: InputAddressType | None
        self.currency: str | None
        self.price: Decimal | None
        self.vendorId: str | None
        self.comment: str | None
        self.pickupLocationId: str | None
        self.dynamicProperties: list[InputDynamicPropertyValueType] | None
