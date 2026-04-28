from restapi.types.base import RestModel


class Category(RestModel):
    id: str
    name: str
    code: str
    catalog_id: str
