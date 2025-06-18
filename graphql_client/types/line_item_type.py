from pydantic import BaseModel


class LineItemType(BaseModel):
    def __init__(self):
        from graphql_client.types.validation_error_type import ValidationErrorType
        from datetime import datetime
        from graphql_client.types.discount_type import DiscountType
        from graphql_client.types.product import Product
        from graphql_client.types.common_vendor import CommonVendor
        from graphql_client.types.tax_detail_type import TaxDetailType
        from graphql_client.types.money_type import MoneyType
        from decimal import Decimal
        from graphql_client.types.cart_configuration_item_type import CartConfigurationItemType
        from graphql_client.types.dynamic_property_value_type import DynamicPropertyValueType

        self.product: Product | None
        self.inStockQuantity: int
        self.warehouseLocation: str | None
        self.isValid: bool
        self.validationErrors: list[ValidationErrorType]
        self.catalogId: str
        self.categoryId: str | None
        self.createdDate: datetime
        self.height: Decimal | None
        self.id: str
        self.imageUrl: str | None
        self.isGift: bool
        self.isReadOnly: bool
        self.isReccuring: bool
        self.selectedForCheckout: bool
        self.languageCode: str | None
        self.length: Decimal | None
        self.measureUnit: str | None
        self.name: str
        self.productOuterId: str | None
        self.note: str | None
        self.objectType: str
        self.productId: str
        self.productType: str | None
        self.quantity: int
        self.requiredShipping: bool
        self.shipmentMethodCode: str | None
        self.sku: str
        self.taxPercentRate: Decimal
        self.taxType: str | None
        self.thumbnailImageUrl: str | None
        self.volumetricWeight: Decimal | None
        self.weight: Decimal | None
        self.weightUnit: str | None
        self.width: Decimal | None
        self.fulfillmentCenterId: str | None
        self.fulfillmentCenterName: str | None
        self.discounts: list[DiscountType]
        self.taxDetails: list[TaxDetailType]
        self.discountAmount: MoneyType
        self.discountAmountWithTax: MoneyType
        self.discountTotal: MoneyType
        self.discountTotalWithTax: MoneyType
        self.extendedPrice: MoneyType
        self.extendedPriceWithTax: MoneyType
        self.listPrice: MoneyType
        self.listPriceWithTax: MoneyType
        self.listTotal: MoneyType
        self.listTotalWithTax: MoneyType
        self.showPlacedPrice: bool
        self.placedPrice: MoneyType
        self.placedPriceWithTax: MoneyType
        self.salePrice: MoneyType
        self.salePriceWithTax: MoneyType
        self.taxTotal: MoneyType
        self.dynamicProperties: list[DynamicPropertyValueType] | None
        self.vendor: CommonVendor | None
        self.configurationItems: list[CartConfigurationItemType] | None
