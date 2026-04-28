from pydantic import BaseModel


class ProductAssociationEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.product_association import ProductAssociation

        self.cursor: str
        self.node: ProductAssociation | None
