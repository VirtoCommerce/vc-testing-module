from .base import GqlModel


class SeoInfo(GqlModel):
    id: str
    name: str | None = None
    semantic_url: str
    outline: str | None = None
    page_title: str | None = None
    meta_description: str | None = None
    image_alt_description: str | None = None
    meta_keywords: str | None = None
    store_id: str | None = None
    object_id: str
    object_type: str
    is_active: bool
    language_code: str | None = None
