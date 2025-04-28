from pydantic import BaseModel


class GraphQLSettingsType(BaseModel):
    def __init__(self):

        self.keepAliveInterval: int
