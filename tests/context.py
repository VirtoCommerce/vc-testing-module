from dataclasses import dataclass
from typing import Any
from uuid import uuid4


@dataclass(frozen=True)
class Context:
    store_id: str
    catalog_id: str
    currency_code: str
    culture_name: str
    user_name: str
    user_id: str
    contact_id: str | None = None
    organization_id: str | None = None

    @classmethod
    def from_dataset(
        cls,
        dataset: dict[str, list[dict[str, Any]]],
        store_id: str,
        username: str | None = None,
    ) -> "Context":
        store = next((s for s in dataset["stores"] if s["id"] == store_id), None)
        if store is None:
            raise ValueError(f"Store '{store_id}' not found in dataset")

        user_name = "Anonymous"
        user_id: str = str(uuid4())
        contact_id: str | None = None
        organization_id: str | None = None

        if username is not None:
            user = next(
                (u for u in dataset["users"] if u["userName"] == username), None
            )
            if user is None:
                raise ValueError(f"User '{username}' not found in dataset")
            contact = next(
                (c for c in dataset["contacts"] if c["id"] == user.get("memberId")),
                None,
            )
            user_name = username
            user_id = user["id"]
            contact_id = user.get("memberId")
            organization_id = contact.get("defaultOrganizationId") if contact else None

        return cls(
            store_id=store_id,
            catalog_id=store["catalog"],
            currency_code=store["defaultCurrency"],
            culture_name=store["defaultLanguage"],
            user_name=user_name,
            user_id=user_id,
            contact_id=contact_id,
            organization_id=organization_id,
        )
