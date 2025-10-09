from pydantic import BaseModel


class IndustrySector(BaseModel):
    NONE = "NONE"
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
