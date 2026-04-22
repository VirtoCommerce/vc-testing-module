from pydantic import BaseModel


class InputNewBulkItemType(BaseModel):
    def __init__(self):

        self.productSku: str
        self.quantity: int | None
