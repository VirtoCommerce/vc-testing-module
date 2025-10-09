from pydantic import BaseModel


class OpusInputRunProcessMainOrderInputType(BaseModel):
    def __init__(self):

        self.mainOrderId: str
