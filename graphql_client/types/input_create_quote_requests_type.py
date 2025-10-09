from pydantic import BaseModel


class InputCreateQuoteRequestsType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_quote_referral_info_type import InputQuoteReferralInfoType
        from graphql_client.types.input_quote_address_type import InputQuoteAddressType
        from graphql_client.types.input_quote_item_type import InputQuoteItemType

        self.supplierIds: list[str] | None
        self.comment: str | None
        self.purpose: str
        self.phone: str | None
        self.email: str
        self.firstName: str | None
        self.lastName: str | None
        self.attachments: list[str] | None
        self.items: list[InputQuoteItemType] | None
        self.shippingAddress: InputQuoteAddressType | None
        self.quoteReferralInfo: InputQuoteReferralInfoType | None
