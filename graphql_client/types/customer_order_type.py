from pydantic import BaseModel


class CustomerOrderType(BaseModel):
    def __init__(self):
        from graphql_client.types.currency_type import CurrencyType
        from graphql_client.types.order_discount_type import OrderDiscountType
        from graphql_client.types.order_payment_method_type import OrderPaymentMethodType
        from decimal import Decimal
        from graphql_client.types.payment_in_type import PaymentInType
        from graphql_client.types.money_type import MoneyType
        from graphql_client.types.order_shipment_type import OrderShipmentType
        from graphql_client.types.order_tax_detail_type import OrderTaxDetailType
        from graphql_client.types.order_line_item_type import OrderLineItemType
        from graphql_client.types.dynamic_property_value_type import DynamicPropertyValueType
        from graphql_client.types.order_address_type import OrderAddressType
        from datetime import datetime

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
        self.customerId: str
        self.customerName: str | None
        self.channelId: str | None
        self.storeId: str
        self.storeName: str | None
        self.organizationId: str | None
        self.organizationName: str | None
        self.employeeId: str | None
        self.employeeName: str | None
        self.shoppingCartId: str | None
        self.isPrototype: bool
        self.subscriptionNumber: str | None
        self.subscriptionId: str | None
        self.purchaseOrderNumber: str | None
        self.taxType: str | None
        self.taxPercentRate: Decimal
        self.languageCode: str | None
        self.createdDate: datetime
        self.createdBy: str | None
        self.modifiedDate: datetime | None
        self.modifiedBy: str | None
        self.currency: CurrencyType
        self.total: MoneyType
        self.taxTotal: MoneyType
        self.discountAmount: MoneyType
        self.subTotal: MoneyType
        self.subTotalWithTax: MoneyType
        self.subTotalDiscount: MoneyType
        self.subTotalDiscountWithTax: MoneyType
        self.subTotalTaxTotal: MoneyType
        self.shippingTotal: MoneyType
        self.shippingTotalWithTax: MoneyType
        self.shippingSubTotal: MoneyType
        self.shippingSubTotalWithTax: MoneyType
        self.shippingDiscountTotal: MoneyType
        self.shippingDiscountTotalWithTax: MoneyType
        self.shippingTaxTotal: MoneyType
        self.paymentTotal: MoneyType
        self.paymentTotalWithTax: MoneyType
        self.paymentSubTotal: MoneyType
        self.paymentSubTotalWithTax: MoneyType
        self.paymentDiscountTotal: MoneyType
        self.paymentDiscountTotalWithTax: MoneyType
        self.paymentTaxTotal: MoneyType
        self.discountTotal: MoneyType
        self.discountTotalWithTax: MoneyType
        self.fee: MoneyType
        self.feeWithTax: MoneyType
        self.feeTotal: MoneyType
        self.feeTotalWithTax: MoneyType
        self.addresses: list[OrderAddressType]
        self.items: list[OrderLineItemType]
        self.inPayments: list[PaymentInType]
        self.shipments: list[OrderShipmentType]
        self.taxDetails: list[OrderTaxDetailType]
        self.dynamicProperties: list[DynamicPropertyValueType]
        self.coupons: list[str]
        self.discounts: list[OrderDiscountType]
        self.availablePaymentMethods: list[OrderPaymentMethodType]
