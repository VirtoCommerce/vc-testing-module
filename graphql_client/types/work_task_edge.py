from pydantic import BaseModel


class WorkTaskEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.work_task_type import WorkTaskType

        self.cursor: str
        self.node: WorkTaskType | None
