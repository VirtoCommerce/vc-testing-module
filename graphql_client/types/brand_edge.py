from pydantic import BaseModel


class BrandEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.brand_type import BrandType

        self.cursor: str
        self.node: BrandType | None
