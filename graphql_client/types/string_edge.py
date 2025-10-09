from pydantic import BaseModel


class StringEdge(BaseModel):
    def __init__(self):

        self.cursor: str
        self.node: str | None
