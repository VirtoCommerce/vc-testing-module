from .base import GqlModel
from .money import Money


class QuoteTotals(GqlModel):
    original_sub_total_exl_tax: Money
    sub_total_exl_tax: Money
    shipping_total: Money
    discount_total: Money
    tax_total: Money
    grand_total_exl_tax: Money
    grand_total_incl_tax: Money
