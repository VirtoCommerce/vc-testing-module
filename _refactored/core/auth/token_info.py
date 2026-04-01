from datetime import UTC, datetime, timedelta

from pydantic import BaseModel, Field, SecretStr, model_validator


class TokenInfo(BaseModel):
    access_token: SecretStr
    expires_in: int
    refresh_token: str | None = None
    expires_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

    @model_validator(mode="after")
    def compute_expires_at(self) -> "TokenInfo":
        self.expires_at = datetime.now(UTC) + timedelta(seconds=self.expires_in)
        return self

    @property
    def is_expired(self) -> bool:
        return datetime.now(UTC) >= self.expires_at - timedelta(seconds=30)
