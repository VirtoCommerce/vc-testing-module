from pydantic import BaseModel


class QuoteTotalsType(BaseModel):
    def __init__(self):
        from graphql_client.types.money_type import MoneyType

        self.originalSubTotalExlTax: MoneyType
        self.subTotalExlTax: MoneyType
        self.shippingTotal: MoneyType
        self.discountTotal: MoneyType
        self.taxTotal: MoneyType
        self.adjustmentQuoteExlTax: MoneyType
        self.grandTotalExlTax: MoneyType
        self.grandTotalInclTax: MoneyType
