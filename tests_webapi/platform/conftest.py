import uuid
from typing import Any, Callable

import pytest

from fixtures.auth import Auth
from fixtures.config import Config
from fixtures.webapi_client import WebAPISession
from webapi_operations.platform.user_operations import UserOperations


@pytest.fixture
def user_operations(webapi_client: WebAPISession) -> UserOperations:
    return UserOperations(webapi_client)


@pytest.fixture
def make_user(
    user_operations: UserOperations,
    auth: Auth,
    config: Config,
) -> Callable[..., dict]:
    """Factory that creates a fresh platform user and cleans up at teardown.

    Returns the `{succeeded, errors, ...}` response from /users/create plus the
    generated `user_name`, `email`, `password` so tests can reuse them without
    touching the factory's private state.

    Usage:
        def test_x(make_user):
            result = make_user()
            assert result["succeeded"]
            user_name = result["user_name"]   # synthesized field, not from backend

    Cleanup deletes by user_name, swallowing errors so a test failure
    (e.g. the user was never actually created) never breaks teardown.
    """
    created_user_names: list[str] = []

    def _make(**overrides: Any) -> dict:
        if auth.token_data is None or not auth.token_data.access_token:
            auth.authenticate(config["ADMIN_USERNAME"], config["ADMIN_PASSWORD"])

        suffix = uuid.uuid4().hex[:8]
        user_name = overrides.pop("user_name", f"QAUser_{suffix}")
        email = overrides.pop("email", f"qauser_{suffix}@example.com")
        password = overrides.pop("password", f"QAPwd!{suffix}")
        store_id = overrides.pop("store_id", config["STORE_ID"])

        response = user_operations.create(
            user_name=user_name,
            email=email,
            password=password,
            store_id=store_id,
            **overrides,
        )

        # Track by name regardless of whether the create "succeeded" — we want
        # cleanup even for negative-path tests that expect duplicate-name 400s.
        created_user_names.append(user_name)

        # Augment the response with the inputs so tests don't reach into factory state.
        response["user_name"] = user_name
        response["email"] = email
        response["password"] = password
        return response

    yield _make

    if created_user_names:
        try:
            user_operations.delete(*created_user_names)
        except Exception:
            pass
