from pydantic import BaseModel


class PaymentInType(BaseModel):
    def __init__(self):
        from graphql_client.types.common_vendor import CommonVendor
        from graphql_client.types.currency_type import CurrencyType
        from graphql_client.types.money_type import MoneyType
        from graphql_client.types.payment_transaction_type import PaymentTransactionType
        from graphql_client.types.order_payment_method_type import OrderPaymentMethodType
        from graphql_client.types.customer_order_type import CustomerOrderType
        from graphql_client.types.dynamic_property_value_type import DynamicPropertyValueType
        from graphql_client.types.order_address_type import OrderAddressType
        from datetime import datetime

        self.id: str
        self.organizationId: str | None
        self.organizationName: str | None
        self.customerName: str | None
        self.customerId: str
        self.purpose: str | None
        self.gatewayCode: str | None
        self.incomingDate: datetime | None
        self.outerId: str | None
        self.operationType: str
        self.number: str
        self.isApproved: bool
        self.status: str | None
        self.statusDisplayValue: str | None
        self.comment: str | None
        self.isCancelled: bool
        self.cancelledDate: datetime | None
        self.cancelReason: str | None
        self.parentOperationId: str | None
        self.objectType: str
        self.createdDate: datetime
        self.modifiedDate: datetime | None
        self.createdBy: str | None
        self.modifiedBy: str | None
        self.authorizedDate: datetime | None
        self.capturedDate: datetime | None
        self.voidedDate: datetime | None
        self.orderId: str | None
        self.price: MoneyType
        self.sum: MoneyType
        self.tax: MoneyType
        self.paymentMethod: OrderPaymentMethodType | None
        self.currency: CurrencyType
        self.billingAddress: OrderAddressType | None
        self.vendor: CommonVendor | None
        self.transactions: list[PaymentTransactionType]
        self.order: CustomerOrderType
        self.dynamicProperties: list[DynamicPropertyValueType]
