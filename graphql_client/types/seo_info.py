from pydantic import BaseModel


class SeoInfo(BaseModel):
    def __init__(self):

        self.id: str
        self.name: str | None
        self.semanticUrl: str
        self.pageTitle: str | None
        self.metaDescription: str | None
        self.imageAltDescription: str | None
        self.metaKeywords: str | None
        self.storeId: str | None
        self.objectId: str
        self.objectType: str
        self.isActive: bool
        self.languageCode: str | None
