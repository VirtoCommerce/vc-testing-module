from pydantic import BaseModel


class PropertyEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.property import Property

        self.cursor: str
        self.node: Property | None
