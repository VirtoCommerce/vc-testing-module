from gql import gql
from graphql_client.types.fcm_settings_type import FcmSettingsType


class FcmSettingsQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> FcmSettingsType:
        query_string = f"""
            query fcmSettings() {{
                fcmSettings(
                    
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["fcmSettings"]
