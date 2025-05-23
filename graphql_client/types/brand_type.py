from pydantic import BaseModel


class BrandType(BaseModel):
    def __init__(self):

        self.id: str
        self.brandPropertyName: str | None
        self.brandPropertyValue: str | None
        self.name: str | None
        self.featured: bool | None
        self.description: str | None
        self.permalink: str
        self.bannerUrl: str | None
        self.logoUrl: str | None
