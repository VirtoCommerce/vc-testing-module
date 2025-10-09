from pydantic import BaseModel


class SupplierEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.supplier_type import SupplierType

        self.cursor: str
        self.node: SupplierType | None
