"""Shared fixtures for REST API tests.

Provides:
- `admin_auth` — session-scoped AuthProvider signed in as admin
- `rest_client` — function-scoped RestClient with admin auth
- `backend_base_url` — convenience string for operations constructors
- `har_recorder` — autouse, writes HAR 1.2 traces to har-output/<module>/
"""

import re
from pathlib import Path
from typing import Generator

import pytest

from core.auth import AuthProvider
from core.clients.rest import RestClient
from core.global_settings import GlobalSettings
from utils.har_recorder import HARRecorder

_INVALID_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*]')


def _module_folder(node_path: Path) -> str:
    """Derive the module name from the test file path.

    tests/restapi/<module>/test_*.py → module name.
    """
    parts = node_path.parts
    try:
        idx = parts.index("restapi")
        candidate = parts[idx + 1]
        if candidate.endswith(".py"):
            return "_root"
        return candidate
    except (ValueError, IndexError):
        return node_path.parent.name or "_unknown"


@pytest.fixture(scope="session")
def admin_auth(global_settings: GlobalSettings) -> AuthProvider:
    """Session-scoped admin auth — signed in once, reused across all REST tests."""
    provider = AuthProvider(global_settings)
    provider.sign_in(global_settings.admin_username, global_settings.admin_password)
    return provider


@pytest.fixture
def rest_client(global_settings: GlobalSettings, admin_auth: AuthProvider) -> Generator[RestClient, None, None]:
    with RestClient(global_settings=global_settings, auth=admin_auth) as client:
        yield client


@pytest.fixture(scope="session")
def backend_base_url(global_settings: GlobalSettings) -> str:
    return global_settings.backend_base_url


@pytest.fixture(autouse=True)
def har_recorder(request: pytest.FixtureRequest, rest_client: RestClient) -> Generator[HARRecorder, None, None]:
    """Record every REST API call and write a HAR file per test to har-output/<module>/."""
    recorder = HARRecorder()
    rest_client._session.hooks["response"].append(recorder.hook)
    try:
        yield recorder
    finally:
        try:
            rest_client._session.hooks["response"].remove(recorder.hook)
        except ValueError:
            pass

        if recorder.has_entries():
            root_dir = Path(request.config.rootpath)
            module = _module_folder(Path(request.node.path))
            out_dir = root_dir / "har-output" / module
            out_dir.mkdir(parents=True, exist_ok=True)

            safe_name = _INVALID_FILENAME_CHARS.sub("_", request.node.name)
            (out_dir / f"{safe_name}.har").write_text(recorder.serialize(), encoding="utf-8")
