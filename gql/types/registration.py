from .base import GqlModel
from .registration_account import RegistrationAccount
from .registration_contact import RegistrationContact
from .registration_organization import RegistrationOrganization
from .registration_result import RegistrationResult


class Registration(GqlModel):
    contact: RegistrationContact
    organization: RegistrationOrganization | None = None
    account: RegistrationAccount
    result: RegistrationResult
