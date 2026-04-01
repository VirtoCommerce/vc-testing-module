from .base import GqlModel
from .seo_info import SeoInfo


class SlugInfo(GqlModel):
    entity_info: SeoInfo | None = None
    redirect_url: str | None = None
