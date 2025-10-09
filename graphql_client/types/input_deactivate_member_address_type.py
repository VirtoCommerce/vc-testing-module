from pydantic import BaseModel


class InputDeactivateMemberAddressType(BaseModel):
    def __init__(self):

        self.memberId: str
        self.addressKey: str
