from pydantic import BaseModel


class OpusInputChangeApproverType(BaseModel):
    def __init__(self):

        self.agencyUserId: str
        self.orderApproverId: str | None
