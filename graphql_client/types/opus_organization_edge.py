from pydantic import BaseModel


class OpusOrganizationEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.organization import Organization

        self.cursor: str
        self.node: Organization | None
