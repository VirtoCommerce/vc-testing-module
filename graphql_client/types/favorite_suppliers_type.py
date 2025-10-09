from pydantic import BaseModel


class FavoriteSuppliersType(BaseModel):
    NONE = "NONE"
    USER = "USER"
    AGENCY = "AGENCY"
