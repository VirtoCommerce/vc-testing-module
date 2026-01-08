from pydantic import BaseModel


class WhiteLabelingSettingsType(BaseModel):
    def __init__(self):
        from graphql_client.types.menu_link_type import MenuLinkType
        from graphql_client.types.favicon_type import FaviconType

        self.userId: str | None
        self.organizationId: str | None
        self.storeId: str | None
        self.logoUrl: str | None
        self.secondaryLogoUrl: str | None
        self.faviconUrl: str | None
        self.themePresetName: str | None
        self.footerLinks: list[MenuLinkType] | None
        self.favicons: list[FaviconType] | None
        self.isOrganizationLogoUploaded: bool | None
        self.isOrganizationSecondaryLogoUploaded: bool | None
        self.isOrganizationFaviconUploaded: bool | None
