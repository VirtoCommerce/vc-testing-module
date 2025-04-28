from gql import gql
from graphql_client.types.white_labeling_settings_type import WhiteLabelingSettingsType


class WhiteLabelingSettingsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> WhiteLabelingSettingsType:
        query_string = f"""
            query whiteLabelingSettings($organizationId: String, $userId: String, $storeId: String, $cultureName: String) {{
                whiteLabelingSettings(
                    organizationId: $organizationId,
                    userId: $userId,
                    storeId: $storeId,
                    cultureName: $cultureName
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["whiteLabelingSettings"]
