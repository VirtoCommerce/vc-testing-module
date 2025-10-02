from pydantic import BaseModel


class Subscriptions(BaseModel):
    def __init__(self):

        self.ping: str | None
