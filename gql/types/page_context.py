from .base import GqlModel
from .slug_info import SlugInfo
from .store_info import StoreInfo
from .user import User
from .white_labeling_settings import WhiteLabelingSettings


class PageContext(GqlModel):
    slug_info: SlugInfo | None = None
    store: StoreInfo | None = None
    white_labeling_settings: WhiteLabelingSettings | None = None
    user: User | None = None
