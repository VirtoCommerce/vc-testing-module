import os
import re
import time
from pathlib import Path
from typing import Any, Generator

import allure
import pytest
import requests
from core.auth import AuthProvider
from core.clients import GraphQLClient
from core.global_settings import GlobalSettings
from core.global_settings import global_settings as _global_settings
from core.logger import NullLogger
from gql.operations.cart_operations import CartOperations
from gql.types.cart import Cart
from gql.types.cart_item_input import CartItemInput
from page_objects.browser_storage import BrowserStorage
from playwright.sync_api import Page
from tests.context import Context

from dataset.dataset_manager import DatasetManager
from utils.har_recorder import HARRecorder

_FEATURE_MARKERS = ["quantity_control", "range_filter_type", "checkout_mode"]
_INVALID_FILENAME_CHARS = re.compile(r'[<>:"/\\|?*]')


def pytest_runtest_setup(item: pytest.Item) -> None:
    for marker_name in _FEATURE_MARKERS:
        marker = item.get_closest_marker(marker_name)
        if marker and marker.args[0] != getattr(_global_settings, marker_name):
            pytest.skip(
                f"Requires {marker_name}='{marker.args[0]}', "
                f"current config has '{getattr(_global_settings, marker_name)}'"
            )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo) -> Generator:
    """Capture test outcome so fixtures can react to failures."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)


@pytest.fixture
def _page_for_failure(request: pytest.FixtureRequest) -> Page | None:
    """Grab the Playwright page before it closes, only for tests that use it."""
    if "page" not in request.fixturenames:
        return None
    return request.getfixturevalue("page")


@pytest.fixture(autouse=True)
def screenshot_on_failure(request: pytest.FixtureRequest, _page_for_failure: Page | None) -> Generator:
    """Take a full-page screenshot when an E2E test fails and attach to Allure."""
    yield

    rep_call = getattr(request.node, "rep_call", None)
    if not rep_call or not rep_call.failed or _page_for_failure is None:
        return

    screenshots_dir = os.path.join("screenshots", "failures")
    os.makedirs(screenshots_dir, exist_ok=True)

    safe_name = _INVALID_FILENAME_CHARS.sub("_", request.node.name)
    screenshot_path = os.path.join(screenshots_dir, f"{safe_name}.png")
    _page_for_failure.screenshot(path=screenshot_path, full_page=True)

    allure.attach.file(
        screenshot_path,
        name=request.node.name,
        attachment_type=allure.attachment_type.PNG,
    )


def _har_module(node_path: Path) -> str:
    """Derive a HAR subfolder from the test file path.

    tests/graphql/test_cart.py         → graphql
    tests/restapi/catalog/test_foo.py  → restapi/catalog
    tests/e2e/test_checkout.py         → e2e
    """
    parts = node_path.parts
    try:
        idx = parts.index("tests")
        remaining = parts[idx + 1 : -1]  # between "tests/" and the filename
        return "/".join(remaining) if remaining else "_root"
    except ValueError:
        return node_path.parent.name or "_unknown"


@pytest.fixture(autouse=True)
def har_recorder(request: pytest.FixtureRequest) -> Generator[HARRecorder, None, None]:
    """Record HTTP calls from graphql_client and/or rest_client and write a
    per-test HAR file to har-output/<suite>/<test_name>.har.

    Hooks are installed only for clients that the test actually uses
    (checked via ``request.fixturenames``), so a GraphQL-only test won't
    force a RestClient to be created and vice versa.
    """
    recorder = HARRecorder()
    hooked_sessions = []

    for fixture_name in ("graphql_client", "rest_client"):
        if fixture_name in request.fixturenames:
            client = request.getfixturevalue(fixture_name)
            client._session.hooks["response"].append(recorder.hook)
            hooked_sessions.append(client._session)

    yield recorder

    for session in hooked_sessions:
        try:
            session.hooks["response"].remove(recorder.hook)
        except ValueError:
            pass

    if recorder.has_entries():
        har_json = recorder.serialize()

        # Write to disk (har-output/<suite>/<test>.har) for the workflow artifact
        root_dir = Path(request.config.rootpath)
        module = _har_module(Path(request.node.path))
        out_dir = root_dir / "har-output" / module
        out_dir.mkdir(parents=True, exist_ok=True)
        safe_name = _INVALID_FILENAME_CHARS.sub("_", request.node.name)
        (out_dir / f"{safe_name}.har").write_text(har_json, encoding="utf-8")

        # Attach to Allure so users can download directly from the test report.
        # Raw MIME string (not the enum) lets the explicit extension="har" stick.
        allure.attach(
            har_json,
            name=f"{request.node.name}.har",
            attachment_type="application/json",
            extension="har",
        )


@pytest.fixture
def browser_context_args(browser_context_args: dict[Any, Any], request: pytest.FixtureRequest) -> dict[Any, Any]:
    extra: dict[str, Any] = {"viewport": {"width": 1920, "height": 1080}}
    if request.node.get_closest_marker("e2e"):
        root_dir = Path(request.config.rootpath)
        module = _har_module(Path(request.node.path))
        out_dir = root_dir / "har-output" / module
        out_dir.mkdir(parents=True, exist_ok=True)
        safe_name = _INVALID_FILENAME_CHARS.sub("_", request.node.name)
        har_path = out_dir / f"{safe_name}.har"
        request.node._e2e_har_path = har_path
        extra["record_har_path"] = str(har_path)
        extra["record_har_omit_content"] = False
    return {**browser_context_args, **extra}


@pytest.fixture(autouse=True)
def attach_e2e_har(request: pytest.FixtureRequest) -> Generator[None, None, None]:
    """Attach the Playwright HAR file to Allure once the context has flushed it."""
    yield
    if not request.node.get_closest_marker("e2e"):
        return
    har_path: Path | None = getattr(request.node, "_e2e_har_path", None)
    if har_path and har_path.exists():
        allure.attach.file(
            str(har_path),
            name=f"{request.node.name}.har",
            attachment_type="application/json",
            extension="har",
        )


@pytest.fixture(scope="session")
def global_settings() -> GlobalSettings:
    return _global_settings


@pytest.fixture(scope="session")
def auth(global_settings: GlobalSettings) -> AuthProvider:
    return AuthProvider(global_settings)


_STOREFRONT_SEARCH_READY_QUERY = """
query SearchReadyProbe(
  $storeId: String!
  $userId: String!
  $currencyCode: String!
  $cultureName: String
) {
  products(
    storeId: $storeId
    userId: $userId
    currencyCode: $currencyCode
    cultureName: $cultureName
    first: 1
    withFacets: false
    withImages: false
  ) {
    totalCount
  }
}
"""
_TRANSPORT_ERROR_CODES = {"SEARCH", "TRANSPORT"}


@pytest.fixture(scope="session")
def storefront_search_ready(global_settings: GlobalSettings) -> None:
    """Probe the storefront's xapi /graphql until it can resolve `products`
    cleanly. The mysql Docker CI has been observed booting with the storefront-
    to-search transport broken for several minutes, during which every category
    test fails the same way and retries can't recover. Abort the session early
    with a clear diagnostic when we explicitly see the SEARCH/TRANSPORT error
    code; on other failure shapes (HTTP 400 from a schema-version mismatch,
    network blip, etc.) just log a warning and let tests proceed so this fixture
    never blocks unrelated environments.
    """
    url = f"{global_settings.frontend_base_url.rstrip('/')}/graphql"
    payload = {
        "operationName": "SearchReadyProbe",
        "query": _STOREFRONT_SEARCH_READY_QUERY,
        "variables": {
            "storeId": global_settings.store_id,
            "userId": "00000000-0000-0000-0000-000000000000",
            "currencyCode": "USD",
            "cultureName": "en-US",
        },
    }
    deadline = time.monotonic() + 90.0
    last_status: str = "no response"
    saw_transport_error = False
    while time.monotonic() < deadline:
        try:
            resp = requests.post(url, json=payload, timeout=10, verify=global_settings.verify_ssl)
            body: dict[str, Any] = (
                resp.json() if resp.headers.get("content-type", "").startswith("application/json") else {}
            )
            errors = body.get("errors") or []
            if resp.status_code == 200 and not errors:
                return
            last_status = f"status={resp.status_code} errors={errors!r}"
            transport_in_response = False
            for err in errors:
                codes = set((err.get("extensions") or {}).get("codes") or [])
                if codes & _TRANSPORT_ERROR_CODES:
                    saw_transport_error = True
                    transport_in_response = True
            if 400 <= resp.status_code < 500 and not transport_in_response:
                # Client-side rejection without a transport error code means
                # the probe doesn't match this environment's schema; polling
                # won't recover. Bail immediately.
                break
        except requests.RequestException as exc:
            last_status = repr(exc)
        time.sleep(3)
    if saw_transport_error:
        pytest.exit(
            f"Storefront search not ready within 90s: {last_status}. "
            f"Saw SEARCH/TRANSPORT error during probe — storefront-to-search "
            f"transport outage on this CI run.",
            returncode=1,
        )
    # Probe never produced a clean response, but never saw the specific
    # SEARCH/TRANSPORT signal either — most likely the probe query doesn't
    # match this environment's schema. Don't block the session; tests' own
    # retries will catch real flakes.
    print(
        f"\n[storefront_search_ready] probe inconclusive after 90s "
        f"(last: {last_status}); proceeding without gating."
    )


@pytest.fixture(autouse=True)
def _gate_e2e_on_storefront_search(request: pytest.FixtureRequest) -> None:
    if request.node.get_closest_marker("e2e"):
        request.getfixturevalue("storefront_search_ready")


@pytest.fixture(scope="session")
def dataset_manager(global_settings: GlobalSettings) -> DatasetManager:
    return DatasetManager.create(global_settings, logger=NullLogger())


@pytest.fixture(scope="session")
def dataset(dataset_manager: DatasetManager) -> dict[str, list[dict[str, Any]]]:
    return dataset_manager.dataset


@pytest.fixture
def graphql_client(with_user: AuthProvider, global_settings: GlobalSettings) -> Generator[GraphQLClient, None, None]:
    with GraphQLClient(auth=with_user, global_settings=global_settings) as client:
        yield client


@pytest.fixture
def with_user(request: pytest.FixtureRequest, global_settings: GlobalSettings) -> Generator[AuthProvider, None, None]:
    provider = AuthProvider(global_settings)
    marker = request.node.get_closest_marker("with_user")
    if marker:
        username: str = marker.args[0]
        with allure.step(f"Sign in as {username}"):
            provider.sign_in(username, global_settings.users_password)
            if request.node.get_closest_marker("e2e") and provider.token_info:
                page = request.getfixturevalue("page")
                BrowserStorage(page).set_auth(provider.token_info)
    yield provider
    if provider.is_authenticated:
        with allure.step("Sign out"):
            provider.sign_out()


@pytest.fixture(autouse=True)
def with_cart(
    request: pytest.FixtureRequest,
    with_user: AuthProvider,
    ctx: Context,
    global_settings: GlobalSettings,
) -> Generator[Cart | None, None, None]:
    marker = request.node.get_closest_marker("with_cart")
    if not marker:
        yield None
        return
    items = [CartItemInput(product_id=product_id, quantity=quantity) for product_id, quantity in marker.args[0]]
    item_summary = ", ".join(f"{p}×{q}" for p, q in marker.args[0])
    with GraphQLClient(auth=with_user, global_settings=global_settings) as client:
        cart_ops = CartOperations(client)
        with allure.step(f"Seed cart with items: {item_summary}"):
            cart = cart_ops.add_items_to_cart(
                store_id=ctx.store_id,
                user_id=ctx.user_id,
                items=items,
                currency_code=ctx.currency_code,
                culture_name=ctx.culture_name,
            )
            # Poll until the cart is read-back-visible. On some demo backends
            # the storefront's first cart query can race the create and return
            # null; ensure read-after-write consistency before yielding so e2e
            # tests don't flake on initial page load.
            for _ in range(global_settings.poll_attempts):
                fetched = cart_ops.get_cart(
                    store_id=ctx.store_id,
                    user_id=ctx.user_id,
                    currency_code=ctx.currency_code,
                    culture_name=ctx.culture_name,
                    cart_id=cart.id,
                )
                if fetched and (fetched.items_count or 0) > 0:
                    break
                time.sleep(global_settings.poll_interval)
            if request.node.get_closest_marker("e2e"):
                page = request.getfixturevalue("page")
                BrowserStorage(page).set_user_id(ctx.user_id)
        yield cart
        with allure.step(f"Teardown: delete seeded cart {cart.id}"):
            cart_ops.delete_cart(cart_id=cart.id, user_id=ctx.user_id)


@pytest.fixture(autouse=True)
def delete_cart_after(
    request: pytest.FixtureRequest,
    ctx: Context,
    global_settings: GlobalSettings,
    auth: AuthProvider,
) -> Generator[None, None, None]:
    if not request.node.get_closest_marker("delete_cart_after"):
        yield None
        return
    page = request.getfixturevalue("page") if request.node.get_closest_marker("e2e") else None
    yield
    if page is not None:
        user_id: str | None = BrowserStorage(page).get_user_id()
    else:
        user_id = ctx.user_id
    if not user_id:
        return
    with GraphQLClient(auth=auth, global_settings=global_settings) as client:
        cart_ops = CartOperations(client)
        with allure.step(f"Teardown: lookup cart for user {user_id}"):
            cart = cart_ops.get_cart(
                store_id=ctx.store_id,
                user_id=user_id,
                currency_code=ctx.currency_code,
                culture_name=ctx.culture_name,
            )
        if cart:
            with allure.step(f"Teardown: delete cart {cart.id}"):
                cart_ops.delete_cart(cart_id=cart.id, user_id=user_id)


@pytest.fixture
def ctx(
    request: pytest.FixtureRequest,
    dataset: dict[str, list[dict[str, Any]]],
    global_settings: GlobalSettings,
) -> Context:
    marker = request.node.get_closest_marker("with_user")
    username: str | None = marker.args[0] if marker else None
    return Context.from_dataset(dataset, global_settings.store_id, username)
