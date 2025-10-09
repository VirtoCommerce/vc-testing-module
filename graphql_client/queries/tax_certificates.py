from gql import gql
from graphql_client.types.tax_certificate_connection import TaxCertificateConnection


class TaxCertificatesQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> TaxCertificateConnection:
        query_string = f"""
            query taxCertificates($after: String, $first: Int, $keyword: String, $sort: String, $storeId: String!, $userId: String) {{
                taxCertificates(
                    after: $after,
                    first: $first,
                    keyword: $keyword,
                    sort: $sort,
                    storeId: $storeId,
                    userId: $userId
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["taxCertificates"]
