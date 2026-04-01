from .base import GqlModel
from .menu_link import MenuLink


class WhiteLabelingSettings(GqlModel):
    logo_url: str | None = None
    secondary_logo_url: str | None = None
    favicon_url: str | None = None
    theme_preset_name: str | None = None
    footer_links: list[MenuLink] = []
    main_menu_links: list[MenuLink] = []
