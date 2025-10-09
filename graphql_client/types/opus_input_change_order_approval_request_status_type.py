from pydantic import BaseModel


class OpusInputChangeOrderApprovalRequestStatusType(BaseModel):
    def __init__(self):

        self.approvalRequestId: str
        self.newStatus: str
        self.comment: str | None
        self.isEditing: bool | None
        self.approverWillPay: bool | None
