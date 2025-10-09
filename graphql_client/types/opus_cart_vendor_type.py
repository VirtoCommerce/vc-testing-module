from pydantic import BaseModel


class OpusCartVendorType(BaseModel):
    def __init__(self):
        from graphql_client.types.money_type import MoneyType
        from graphql_client.types.common_vendor import CommonVendor
        from graphql_client.types.currency_type import CurrencyType
        from graphql_client.types.line_item_type import LineItemType

        self.vendor: CommonVendor | None
        self.currency: CurrencyType
        self.total: MoneyType
        self.subTotal: MoneyType
        self.subTotalWithTax: MoneyType
        self.extendedPriceTotal: MoneyType
        self.extendedPriceTotalWithTax: MoneyType
        self.taxTotal: MoneyType
        self.fee: MoneyType
        self.feeWithTax: MoneyType
        self.feeTotal: MoneyType
        self.feeTotalWithTax: MoneyType
        self.shippingPrice: MoneyType
        self.shippingPriceWithTax: MoneyType
        self.shippingTotal: MoneyType
        self.shippingTotalWithTax: MoneyType
        self.paymentPrice: MoneyType
        self.paymentPriceWithTax: MoneyType
        self.paymentTotal: MoneyType
        self.paymentTotalWithTax: MoneyType
        self.discountTotal: MoneyType
        self.discountTotalWithTax: MoneyType
        self.subTotalDiscount: MoneyType
        self.subTotalDiscountWithTax: MoneyType
        self.items: list[LineItemType]
        self.itemsCount: int
        self.itemsQuantity: int
        self.isPONumberMandatory: bool
        self.contractNumbers: list[str]
