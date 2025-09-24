from pydantic import BaseModel


class CartType(BaseModel):
    def __init__(self):
        from graphql_client.types.payment_method_type import PaymentMethodType
        from graphql_client.types.shipment_type import ShipmentType
        from graphql_client.types.payment_type import PaymentType
        from graphql_client.types.discount_type import DiscountType
        from graphql_client.types.cart_address_type import CartAddressType
        from graphql_client.types.coupon_type import CouponType
        from graphql_client.types.money_type import MoneyType
        from graphql_client.types.tax_detail_type import TaxDetailType
        from graphql_client.types.dynamic_property_value_type import DynamicPropertyValueType
        from graphql_client.types.validation_error_type import ValidationErrorType
        from graphql_client.types.currency_type import CurrencyType
        from decimal import Decimal
        from graphql_client.types.gift_item_type import GiftItemType
        from graphql_client.types.line_item_type import LineItemType
        from graphql_client.types.shipping_method_type import ShippingMethodType

        self.id: str
        self.name: str
        self.status: str | None
        self.storeId: str
        self.channelId: str | None
        self.hasPhysicalProducts: bool | None
        self.isAnonymous: bool
        self.customerId: str
        self.customerName: str | None
        self.organizationId: str | None
        self.organizationName: str | None
        self.isRecuring: bool | None
        self.comment: str | None
        self.purchaseOrderNumber: str | None
        self.checkoutId: str
        self.volumetricWeight: Decimal | None
        self.weightUnit: str | None
        self.weight: Decimal | None
        self.total: MoneyType
        self.subTotal: MoneyType
        self.subTotalWithTax: MoneyType
        self.extendedPriceTotal: MoneyType
        self.extendedPriceTotalWithTax: MoneyType
        self.currency: CurrencyType
        self.taxTotal: MoneyType
        self.taxPercentRate: Decimal
        self.taxType: str
        self.taxDetails: list[TaxDetailType]
        self.fee: MoneyType
        self.feeWithTax: MoneyType
        self.feeTotal: MoneyType
        self.feeTotalWithTax: MoneyType
        self.shippingPrice: MoneyType
        self.shippingPriceWithTax: MoneyType
        self.shippingTotal: MoneyType
        self.shippingTotalWithTax: MoneyType
        self.shipments: list[ShipmentType]
        self.availableShippingMethods: list[ShippingMethodType]
        self.paymentPrice: MoneyType
        self.paymentPriceWithTax: MoneyType
        self.paymentTotal: MoneyType
        self.paymentTotalWithTax: MoneyType
        self.payments: list[PaymentType]
        self.availablePaymentMethods: list[PaymentMethodType]
        self.handlingTotal: MoneyType
        self.handlingTotalWithTax: MoneyType
        self.discountTotal: MoneyType
        self.discountTotalWithTax: MoneyType
        self.subTotalDiscount: MoneyType
        self.subTotalDiscountWithTax: MoneyType
        self.discounts: list[DiscountType]
        self.addresses: list[CartAddressType]
        self.gifts: list[GiftItemType]
        self.availableGifts: list[GiftItemType]
        self.items: list[LineItemType]
        self.itemsCount: int
        self.itemsQuantity: int
        self.coupons: list[CouponType]
        self.dynamicProperties: list[DynamicPropertyValueType]
        self.validationErrors: list[ValidationErrorType]
        self.type: str | None
        self.warnings: list[ValidationErrorType]
