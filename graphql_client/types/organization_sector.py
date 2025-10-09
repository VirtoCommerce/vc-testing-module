from pydantic import BaseModel


class OrganizationSector(BaseModel):
    NONE = "NONE"
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    NONPROFIT = "NONPROFIT"
