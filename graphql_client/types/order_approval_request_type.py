from pydantic import BaseModel


class OrderApprovalRequestType(BaseModel):
    def __init__(self):
        from datetime import datetime
        from decimal import Decimal

        self.id: str
        self.createdDate: datetime | None
        self.createdBy: str
        self.modifiedDate: datetime | None
        self.modifiedBy: str
        self.flowType: str
        self.approverId: str | None
        self.approverName: str | None
        self.approverEmail: str | None
        self.resolvedById: str | None
        self.resolvedByName: str | None
        self.resolvedDate: datetime | None
        self.customerOrderId: str | None
        self.cartId: str | None
        self.editingCartId: str | None
        self.prototypeId: str | None
        self.isPrototype: bool
        self.orderNumber: str
        self.customerId: str
        self.customerName: str
        self.customerEmail: str | None
        self.subTotal: Decimal
        self.shippingTotal: Decimal
        self.discountTotal: Decimal
        self.feeTotal: Decimal
        self.taxTotal: Decimal
        self.total: Decimal
        self.comment: str | None
        self.status: str
        self.orderStatus: str
        self.hasAttachments: bool
