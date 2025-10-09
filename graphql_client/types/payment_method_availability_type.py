from pydantic import BaseModel


class PaymentMethodAvailabilityType(BaseModel):
    NONE = "NONE"
    ACTIVE = "ACTIVE"
    AVAILABLE = "AVAILABLE"
    DISABLED = "DISABLED"
    IN_PROGRESS = "IN_PROGRESS"
