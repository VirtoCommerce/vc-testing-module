from pydantic import BaseModel


class SupplierAgencyEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.supplier_agency_type import SupplierAgencyType

        self.cursor: str
        self.node: SupplierAgencyType | None
