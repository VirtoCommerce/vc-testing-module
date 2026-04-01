from .base import GqlModel
from .currency import Currency
from .language import Language
from .store_settings import StoreSettings


class StoreInfo(GqlModel):
    store_id: str
    store_name: str
    catalog_id: str
    store_url: str | None = None
    default_language: Language
    available_languages: list[Language] = []
    default_currency: Currency
    available_currencies: list[Currency] = []
    settings: StoreSettings | None = None
