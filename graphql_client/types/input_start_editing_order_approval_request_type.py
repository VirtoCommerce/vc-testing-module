from pydantic import BaseModel


class InputStartEditingOrderApprovalRequestType(BaseModel):
    def __init__(self):

        self.approvalRequestId: str
