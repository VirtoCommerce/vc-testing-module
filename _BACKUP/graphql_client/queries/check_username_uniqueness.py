from gql import gql


class CheckUsernameUniquenessQuery:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> bool:
        query_string = f"""
            query checkUsernameUniqueness($username: String!) {{
                checkUsernameUniqueness(
                    username: $username
                )
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["checkUsernameUniqueness"]
