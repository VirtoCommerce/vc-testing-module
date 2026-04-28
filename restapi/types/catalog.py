from restapi.types.base import RestModel


class CatalogLanguage(RestModel):
    language_code: str
    is_default: bool = False


class Catalog(RestModel):
    id: str
    name: str
    is_virtual: bool = False
    languages: list[CatalogLanguage] = []
