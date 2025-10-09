from gql import gql
from graphql_client.types.result_type import ResultType


class AddTaxCertificatesMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> ResultType:
        query_string = f"""
            mutation addTaxCertificates($command: InputAddTaxCertificatesType!) {{
                addTaxCertificates(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["addTaxCertificates"]
