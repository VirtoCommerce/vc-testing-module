from pydantic import BaseModel


class OpusProductEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.product import Product

        self.cursor: str
        self.node: Product | None
