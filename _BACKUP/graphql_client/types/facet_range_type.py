from pydantic import BaseModel


class FacetRangeType(BaseModel):
    def __init__(self):
        from decimal import Decimal

        self.count: int
        self.from_: Decimal | None
        self.includeFrom: bool
        self.fromStr: str | None
        self.max: Decimal
        self.min: Decimal
        self.to: Decimal | None
        self.includeTo: bool
        self.toStr: str | None
        self.total: int
        self.label: str
        self.isSelected: bool
