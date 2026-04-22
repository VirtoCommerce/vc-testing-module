from pydantic import BaseModel


class ContractEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.contract_type import ContractType

        self.cursor: str
        self.node: ContractType | None
