from pydantic import BaseModel


class ProductPickupAvailabilityType(BaseModel):
    Today = "Today"
    Transfer = "Transfer"
    GlobalTransfer = "GlobalTransfer"
