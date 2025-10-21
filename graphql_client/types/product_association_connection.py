from pydantic import BaseModel


class ProductAssociationConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.product_association import ProductAssociation
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.product_association_edge import ProductAssociationEdge

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[ProductAssociationEdge] | None
        self.items: list[ProductAssociation] | None
