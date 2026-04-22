from gql import gql
from graphql_client.types.work_task_type import WorkTaskType


class ConfirmTaskMutation:
    def __init__(self, graphql_client):
        self.graphql_client = graphql_client

    def execute(self, variables: dict, return_fields: str = None) -> WorkTaskType:
        query_string = f"""
            mutation confirmTask($command: ConfirmTaskCommandType!) {{
                confirmTask(
                    command: $command
                ) {{
                    {return_fields}
                }}
            }}
        """

        return self.graphql_client.execute(gql(query_string), variables)["confirmTask"]
