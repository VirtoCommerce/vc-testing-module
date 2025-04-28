from pydantic import BaseModel


class Breadcrumb(BaseModel):
    def __init__(self):

        self.itemId: str
        self.title: str
        self.typeName: str
        self.seoPath: str | None
        self.semanticUrl: str | None
