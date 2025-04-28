from pydantic import BaseModel


class QuoteShipmentMethodType(BaseModel):
    def __init__(self):
        from graphql_client.types.money_type import MoneyType
        from graphql_client.types.currency_type import CurrencyType

        self.shipmentMethodCode: str
        self.optionName: str | None
        self.logoUrl: str | None
        self.typeName: str | None
        self.currency: CurrencyType
        self.price: MoneyType
