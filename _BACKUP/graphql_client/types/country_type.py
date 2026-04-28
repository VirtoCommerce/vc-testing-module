from pydantic import BaseModel


class CountryType(BaseModel):
    def __init__(self):
        from graphql_client.types.country_region_type import CountryRegionType

        self.id: str
        self.name: str
        self.regions: list[CountryRegionType]
