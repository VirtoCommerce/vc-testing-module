from .base import GqlModel
from .product_price import ProductPrice
from .seo_info import SeoInfo
from .vendor import Vendor


class Product(GqlModel):
    id: str
    code: str
    product_type: str
    is_configurable: bool
    name: str
    vendor: Vendor | None = None
    seo_info: SeoInfo | None = None
    price: ProductPrice | None = None
