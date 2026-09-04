from restapi.types.base import RestModel


class PageBuilderPage(RestModel):
    id: str
    name: str
    store_id: str | None = None
    permalink: str | None = None
    culture_name: str | None = None
    status: str | None = None
