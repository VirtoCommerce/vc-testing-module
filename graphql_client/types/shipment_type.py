from pydantic import BaseModel


class ShipmentType(BaseModel):
    def __init__(self):
        from graphql_client.types.money_type import MoneyType
        from graphql_client.types.pickup_location_type import PickupLocationType
        from graphql_client.types.cart_address_type import CartAddressType
        from graphql_client.types.common_vendor import CommonVendor
        from decimal import Decimal
        from graphql_client.types.cart_shipment_item_type import CartShipmentItemType
        from graphql_client.types.discount_type import DiscountType
        from graphql_client.types.shipping_method_type import ShippingMethodType
        from graphql_client.types.tax_detail_type import TaxDetailType
        from graphql_client.types.dynamic_property_value_type import DynamicPropertyValueType
        from graphql_client.types.currency_type import CurrencyType

        self.id: str
        self.shipmentMethodCode: str | None
        self.shipmentMethodOption: str | None
        self.fulfillmentCenterId: str | None
        self.deliveryAddress: CartAddressType | None
        self.volumetricWeight: Decimal | None
        self.weightUnit: str | None
        self.weight: Decimal | None
        self.measureUnit: str | None
        self.height: Decimal | None
        self.length: Decimal | None
        self.width: Decimal | None
        self.price: MoneyType
        self.priceWithTax: MoneyType
        self.fee: MoneyType
        self.feeWithTax: MoneyType
        self.total: MoneyType
        self.totalWithTax: MoneyType
        self.discountAmount: MoneyType
        self.discountAmountWithTax: MoneyType
        self.items: list[CartShipmentItemType]
        self.taxTotal: MoneyType
        self.taxPercentRate: Decimal
        self.taxType: str | None
        self.taxDetails: list[TaxDetailType]
        self.discounts: list[DiscountType]
        self.currency: CurrencyType
        self.comment: str | None
        self.vendor: CommonVendor | None
        self.dynamicProperties: list[DynamicPropertyValueType]
        self.shippingMethod: ShippingMethodType | None
        self.pickupLocation: PickupLocationType | None
