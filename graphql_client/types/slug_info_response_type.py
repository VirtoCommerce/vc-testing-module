from pydantic import BaseModel


class SlugInfoResponseType(BaseModel):
    def __init__(self):
        from graphql_client.types.seo_info import SeoInfo

        self.entityInfo: SeoInfo | None
