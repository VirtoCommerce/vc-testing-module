from gql import gql
from graphql_client.types.tax_certificate_type import TaxCertificateType


class TaxCertificateQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> TaxCertificateType:
        query_string = f"""
            query taxCertificate($storeId: String!, $userId: String!, $taxCertificateId: String!) {{
                taxCertificate(
                    storeId: $storeId,
                    userId: $userId,
                    taxCertificateId: $taxCertificateId
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["taxCertificate"]
