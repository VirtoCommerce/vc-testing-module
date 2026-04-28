from restapi.types.base import RestModel


class Pricelist(RestModel):
    id: str
    name: str
    currency: str | None = None


class PricelistAssignment(RestModel):
    id: str
    name: str
    pricelist_id: str | None = None
    catalog_id: str | None = None
