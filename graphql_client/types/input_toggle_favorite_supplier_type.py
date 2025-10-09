from pydantic import BaseModel


class InputToggleFavoriteSupplierType(BaseModel):
    def __init__(self):

        self.supplierOuterId: str
