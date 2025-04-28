from pydantic import BaseModel


class AvailabilityData(BaseModel):
    def __init__(self):
        from graphql_client.types.inventory_info import InventoryInfo

        self.availableQuantity: int
        self.isBuyable: bool
        self.isAvailable: bool
        self.isInStock: bool
        self.isActive: bool
        self.isTrackInventory: bool
        self.isEstimated: bool
        self.inventories: list[InventoryInfo]
