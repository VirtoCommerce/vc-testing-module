from pydantic import BaseModel


class SupplierType(BaseModel):
    def __init__(self):
        from datetime import datetime
        from decimal import Decimal
        from graphql_client.types.attachment_file_type import AttachmentFileType
        from graphql_client.types.white_labeling_settings_type import WhiteLabelingSettingsType
        from graphql_client.types.favorite_suppliers_type import FavoriteSuppliersType

        self.id: str
        self.name: str
        self.outerId: str
        self.description: str | None
        self.fullDescription: str | None
        self.externalLink: str | None
        self.externalLinkDescription: str | None
        self.logo: str | None
        self.isActive: bool
        self.isVisibleInCarousel: bool
        self.isChannelPartner: bool
        self.isActivePerAgency: bool
        self.isConnectedToSupplierPortal: bool
        self.isPaymentMethodsForGuestsOnly: bool
        self.isPONumberMandatory: bool
        self.isBuyOnlinePickupInStoreEnabled: bool
        self.pONumberMandatoryThreshold: Decimal | None
        self.relevanceScore: float | None
        self.categories: list[str] | None
        self.rank: int
        self.isConnected: bool
        self.isComingSoon: bool
        self.comingDate: datetime | None
        self.isOrderAllowed: bool
        self.isOrderSetupRequestRequired: bool
        self.isRequestSetupAccountBillingAllowed: bool
        self.paymentMethods: list[str]
        self.contractNumber: str | None
        self.productVisibilityCode: str | None
        self.isFavorite: bool | None
        self.favoriteType: FavoriteSuppliersType
        self.whiteLabelingSettings: WhiteLabelingSettingsType | None
        self.w9Attachment: AttachmentFileType | None
