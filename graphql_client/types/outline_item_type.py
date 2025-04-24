from pydantic import BaseModel


class OutlineItemType(BaseModel):
    def __init__(self):
        from graphql_client.types.seo_info import SeoInfo

        self.id: str
        self.name: str
        self.seoObjectType: str
        self.seoInfos: list[SeoInfo] | None
