from gql import gql
from graphql_client.types.contract_type import ContractType


class ContractQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> ContractType:
        query_string = f"""
            query contract($id: String) {{
                contract(
                    id: $id
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["contract"]
