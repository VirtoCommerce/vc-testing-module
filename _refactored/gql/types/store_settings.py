from .base import GqlModel


class StoreSettings(GqlModel):
    anonymous_users_allowed: bool
    tax_calculation_enabled: bool
    seo_link_type: str | None = None
