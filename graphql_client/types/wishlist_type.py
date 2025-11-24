from pydantic import BaseModel


class WishlistType(BaseModel):
    def __init__(self):
        from graphql_client.types.currency_type import CurrencyType
        from graphql_client.types.wishlist_scope_type import WishlistScopeType
        from graphql_client.types.money_type import MoneyType
        from graphql_client.types.line_item_type import LineItemType
        from graphql_client.types.sharing_setting_type import SharingSettingType
        from datetime import datetime

        self.id: str
        self.name: str
        self.storeId: str | None
        self.customerId: str | None
        self.customerName: str | None
        self.currency: CurrencyType | None
        self.items: list[LineItemType] | None
        self.itemsCount: int | None
        self.scope: WishlistScopeType | None
        self.description: str | None
        self.modifiedDate: datetime | None
        self.subTotal: MoneyType
        self.sharingSetting: SharingSettingType | None
