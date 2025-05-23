from pydantic import BaseModel


class OrderShipmentType(BaseModel):
    def __init__(self):
        from graphql_client.types.payment_in_type import PaymentInType
        from graphql_client.types.currency_type import CurrencyType
        from graphql_client.types.common_vendor import CommonVendor
        from decimal import Decimal
        from graphql_client.types.order_shipment_item_type import OrderShipmentItemType
        from graphql_client.types.dynamic_property_value_type import DynamicPropertyValueType
        from graphql_client.types.order_shipping_method_type import OrderShippingMethodType
        from graphql_client.types.order_tax_detail_type import OrderTaxDetailType
        from graphql_client.types.order_discount_type import OrderDiscountType
        from datetime import datetime
        from graphql_client.types.order_address_type import OrderAddressType
        from graphql_client.types.order_shipment_package_type import OrderShipmentPackageType
        from graphql_client.types.money_type import MoneyType

        self.id: str
        self.operationType: str
        self.parentOperationId: str | None
        self.number: str
        self.isApproved: bool
        self.status: str | None
        self.statusDisplayValue: str | None
        self.comment: str | None
        self.outerId: str | None
        self.isCancelled: bool
        self.cancelledDate: datetime | None
        self.cancelReason: str | None
        self.objectType: str
        self.organizationId: str | None
        self.organizationName: str | None
        self.fulfillmentCenterId: str | None
        self.fulfillmentCenterName: str | None
        self.employeeId: str | None
        self.employeeName: str | None
        self.shipmentMethodCode: str | None
        self.shipmentMethodOption: str | None
        self.shippingMethod: OrderShippingMethodType | None
        self.customerOrderId: str | None
        self.weightUnit: str | None
        self.weight: Decimal | None
        self.measureUnit: str | None
        self.height: Decimal | None
        self.length: Decimal | None
        self.width: Decimal | None
        self.deliveryAddress: OrderAddressType | None
        self.taxType: str | None
        self.taxPercentRate: Decimal
        self.trackingNumber: str | None
        self.trackingUrl: str | None
        self.deliveryDate: datetime | None
        self.price: MoneyType
        self.priceWithTax: MoneyType
        self.fee: MoneyType
        self.feeWithTax: MoneyType
        self.total: MoneyType
        self.totalWithTax: MoneyType
        self.discountAmount: MoneyType
        self.discountAmountWithTax: MoneyType
        self.taxTotal: MoneyType
        self.currency: CurrencyType
        self.taxDetails: list[OrderTaxDetailType]
        self.items: list[OrderShipmentItemType]
        self.packages: list[OrderShipmentPackageType]
        self.inPayments: list[PaymentInType]
        self.discounts: list[OrderDiscountType]
        self.vendor: CommonVendor | None
        self.dynamicProperties: list[DynamicPropertyValueType]
