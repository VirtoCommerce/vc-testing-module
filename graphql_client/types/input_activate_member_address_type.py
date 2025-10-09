from pydantic import BaseModel


class InputActivateMemberAddressType(BaseModel):
    def __init__(self):

        self.memberId: str
        self.addressKey: str
