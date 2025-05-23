from pydantic import BaseModel


class ContractConnection(BaseModel):
    def __init__(self):
        from graphql_client.types.contract_type import ContractType
        from graphql_client.types.page_info import PageInfo
        from graphql_client.types.contract_edge import ContractEdge

        self.totalCount: int | None
        self.pageInfo: PageInfo
        self.edges: list[ContractEdge] | None
        self.items: list[ContractType] | None
