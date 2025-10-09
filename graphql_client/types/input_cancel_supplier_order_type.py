from pydantic import BaseModel


class InputCancelSupplierOrderType(BaseModel):
    def __init__(self):

        self.supplierOrderId: str
        self.cancelReason: str
