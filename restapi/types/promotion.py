from restapi.types.base import RestModel


class Promotion(RestModel):
    id: str
    name: str
    is_active: bool | None = None
