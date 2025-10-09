from pydantic import BaseModel


class InputConfirmSupplierOrderType(BaseModel):
    def __init__(self):
        from graphql_client.types.input_confirm_supplier_order_totals_type import InputConfirmSupplierOrderTotalsType

        self.supplierOrderId: str
        self.orderId: str
        self.totals: InputConfirmSupplierOrderTotalsType | None
        self.comment: str | None
