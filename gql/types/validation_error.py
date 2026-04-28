from .base import GqlModel


class ValidationErrorParameter(GqlModel):
    key: str | None = None
    value: str | None = None


class ValidationError(GqlModel):
    error_code: str | None = None
    error_message: str | None = None
    error_parameters: list[ValidationErrorParameter] | None = None
    object_type: str | None = None
    object_id: str | None = None
