from pydantic import BaseModel


class DeleteSkyflowCardCommandType(BaseModel):
    def __init__(self):

        self.skyflowId: str
        self.storeId: str
