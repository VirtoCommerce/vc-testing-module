from .base import GqlModel


class RegistrationResult(GqlModel):
    succeeded: bool
    require_email_verification: bool
