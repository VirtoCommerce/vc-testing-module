from restapi.types.base import RestModel


class Product(RestModel):
    id: str
    name: str
    code: str
    catalog_id: str
    category_id: str | None = None
