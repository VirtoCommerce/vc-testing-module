from pydantic import BaseModel


class CountryRegionType(BaseModel):
    def __init__(self):

        self.id: str
        self.name: str
