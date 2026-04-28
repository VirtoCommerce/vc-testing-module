from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class RestModel(BaseModel):
    """Base for REST API response models.

    `extra="allow"` so unknown server fields round-trip through `model_dump()`
    and don't get silently lost on update calls that re-send the response.
    The typed fields are the explicit contract; extras pass through.
    Tightening to `extra="forbid"` (S21 in CODE_REVIEW.md) is a follow-up
    pass — first we need typed coverage, then we can demand strictness.
    """

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
        extra="allow",
    )
