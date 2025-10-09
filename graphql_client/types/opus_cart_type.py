from pydantic import BaseModel


class OpusCartType(BaseModel):
    def __init__(self):
        from graphql_client.types.gift_item_type import GiftItemType
        from graphql_client.types.tax_detail_type import TaxDetailType
        from graphql_client.types.coupon_type import CouponType
        from graphql_client.types.money_type import MoneyType
        from graphql_client.types.opus_cart_vendor_type import OpusCartVendorType
        from graphql_client.types.dynamic_property_value_type import DynamicPropertyValueType
        from graphql_client.types.discount_type import DiscountType
        from graphql_client.types.opus_cart_address_type import OpusCartAddressType
        from decimal import Decimal
        from graphql_client.types.opus_shipping_method_type import OpusShippingMethodType
        from graphql_client.types.opus_line_item_type import OpusLineItemType
        from graphql_client.types.opus_payment_method_type import OpusPaymentMethodType
        from graphql_client.types.currency_type import CurrencyType
        from graphql_client.types.opus_payment_type import OpusPaymentType
        from graphql_client.types.attachment_file_type import AttachmentFileType
        from graphql_client.types.opus_shipment_type import OpusShipmentType
        from graphql_client.types.validation_error_type import ValidationErrorType

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
        self.shipments: list[OpusShipmentType]
        self.availableShippingMethods: list[OpusShippingMethodType]
        self.paymentPrice: MoneyType
        self.paymentPriceWithTax: MoneyType
        self.paymentTotal: MoneyType
        self.paymentTotalWithTax: MoneyType
        self.payments: list[OpusPaymentType]
        self.availablePaymentMethods: list[OpusPaymentMethodType]
        self.handlingTotal: MoneyType
        self.handlingTotalWithTax: MoneyType
        self.discountTotal: MoneyType
        self.discountTotalWithTax: MoneyType
        self.subTotalDiscount: MoneyType
        self.subTotalDiscountWithTax: MoneyType
        self.discounts: list[DiscountType]
        self.addresses: list[OpusCartAddressType]
        self.gifts: list[GiftItemType]
        self.availableGifts: list[GiftItemType]
        self.items: list[OpusLineItemType]
        self.itemsCount: int
        self.itemsQuantity: int
        self.coupons: list[CouponType]
        self.dynamicProperties: list[DynamicPropertyValueType]
        self.validationErrors: list[ValidationErrorType]
        self.type: str | None
        self.warnings: list[ValidationErrorType]
        self.vendors: list[OpusCartVendorType] | None
        self.approvalFlowType: str | None
        self.attachments: list[AttachmentFileType] | None
