from gql import gql
from graphql_client.types.country_type import CountryType


class CountriesQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> list[CountryType]:
        query_string = f"""
            query countries() {{
                countries(
                    
                )
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["countries"]
