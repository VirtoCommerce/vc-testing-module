from gql import gql
from graphql_client.types.localized_setting_response_type import LocalizedSettingResponseType


class PaymentStatusesQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> LocalizedSettingResponseType:
        query_string = f"""
            query paymentStatuses($cultureName: String) {{
                paymentStatuses(
                    cultureName: $cultureName
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["paymentStatuses"]
