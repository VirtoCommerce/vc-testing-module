from restapi.types.base import RestModel


class Store(RestModel):
    id: str
    name: str
    catalog: str | None = None
    store_state: str | None = None
