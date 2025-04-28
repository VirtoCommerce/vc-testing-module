from pydantic import BaseModel


class ContactEdge(BaseModel):
    def __init__(self):
        from graphql_client.types.contact_type import ContactType

        self.cursor: str
        self.node: ContactType | None
