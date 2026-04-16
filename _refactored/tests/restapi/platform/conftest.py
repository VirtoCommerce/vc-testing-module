"""Platform module fixtures — factory fixtures for users."""

import uuid
from typing import Any, Callable, Generator

import pytest

from core.clients.rest import RestClient
from core.global_settings import GlobalSettings
from restapi.operations import UserOperations


@pytest.fixture
def user_ops(rest_client: RestClient, backend_base_url: str) -> UserOperations:
    return UserOperations(rest_client, backend_base_url)


@pytest.fixture
def make_user(
    user_ops: UserOperations,
    global_settings: GlobalSettings,
) -> Generator[Callable[..., dict], None, None]:
    """Factory: creates a fresh platform user, cleans up at teardown.

    Returns the backend response augmented with `user_name`, `email`, `password`
    (since the /users/create response only has `{succeeded, errors}`).
    """
    created_user_names: list[str] = []

    def _make(**overrides: Any) -> dict:
        suffix = uuid.uuid4().hex[:8]
        user_name = overrides.pop("user_name", f"QAUser_{suffix}")
        email = overrides.pop("email", f"qauser_{suffix}@example.com")
        password = overrides.pop("password", f"QAPwd!{suffix}")
        store_id = overrides.pop("store_id", global_settings.store_id)

        response = user_ops.create(
            user_name=user_name,
            email=email,
            password=password,
            store_id=store_id,
            **overrides,
        )
        created_user_names.append(user_name)
        response["user_name"] = user_name
        response["email"] = email
        response["password"] = password
        return response

    yield _make

    if created_user_names:
        try:
            user_ops.delete(*created_user_names)
        except Exception:
            pass
