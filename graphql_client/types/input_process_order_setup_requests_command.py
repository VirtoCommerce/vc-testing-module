from pydantic import BaseModel


class InputProcessOrderSetupRequestsCommand(BaseModel):
    def __init__(self):

        self.userId: str
        self.supplierId: str
        self.agencyId: str
