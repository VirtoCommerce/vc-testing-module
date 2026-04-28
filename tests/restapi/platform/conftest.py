"""Platform module fixtures — operations + factory fixtures."""

import uuid
from typing import Any, Callable, Generator

import pytest

from core.clients.rest import RestClient
from core.global_settings import GlobalSettings
from restapi.operations import (
    ApiKeyOperations,
    NotificationsOperations,
    OAuthOperations,
    RoleOperations,
    SettingsOperations,
    UserOperations,
)
from restapi.types import Role


@pytest.fixture
def user_ops(rest_client: RestClient, backend_base_url: str) -> UserOperations:
    return UserOperations(rest_client, backend_base_url)


@pytest.fixture
def api_key_ops(rest_client: RestClient, backend_base_url: str) -> ApiKeyOperations:
    return ApiKeyOperations(rest_client, backend_base_url)


@pytest.fixture
def oauth_ops(rest_client: RestClient, backend_base_url: str) -> OAuthOperations:
    return OAuthOperations(rest_client, backend_base_url)


@pytest.fixture
def settings_ops(rest_client: RestClient, backend_base_url: str) -> SettingsOperations:
    return SettingsOperations(rest_client, backend_base_url)


@pytest.fixture
def role_ops(rest_client: RestClient, backend_base_url: str) -> RoleOperations:
    return RoleOperations(rest_client, backend_base_url)


@pytest.fixture
def notifications_ops(rest_client: RestClient, backend_base_url: str) -> NotificationsOperations:
    return NotificationsOperations(rest_client, backend_base_url)


@pytest.fixture
def make_user(
    user_ops: UserOperations,
    global_settings: GlobalSettings,
) -> Generator[Callable[..., dict], None, None]:
    """Factory: creates a fresh platform user, cleans up at teardown."""
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


@pytest.fixture
def make_role(
    role_ops: RoleOperations,
) -> Generator[Callable[..., Role], None, None]:
    """Factory: creates a platform role, cleans up at teardown."""
    created_ids: list[str] = []

    def _make(**overrides: Any) -> Role:
        suffix = uuid.uuid4().hex[:8]
        name = overrides.pop("name", f"QARole_{suffix}")
        role = role_ops.create(name=name, **overrides)
        created_ids.append(role.id)
        return role

    yield _make

    for rid in reversed(created_ids):
        try:
            role_ops.delete(rid)
        except Exception:
            pass


@pytest.fixture
def make_oauth_client(
    oauth_ops: OAuthOperations,
) -> Generator[Callable[..., dict], None, None]:
    """Factory: creates an OAuth client, cleans up at teardown."""
    created_client_ids: list[str] = []

    def _make(**overrides: Any) -> dict:
        suffix = uuid.uuid4().hex[:8]
        client_id = overrides.pop("client_id", f"qa_client_{suffix}")
        client_secret = overrides.pop("client_secret", f"QASecret!{suffix}")
        result = oauth_ops.create(client_id=client_id, client_secret=client_secret, **overrides)
        created_client_ids.append(client_id)
        result["_client_id"] = client_id
        result["_client_secret"] = client_secret
        return result

    yield _make

    for cid in reversed(created_client_ids):
        try:
            oauth_ops.delete(cid)
        except Exception:
            pass
