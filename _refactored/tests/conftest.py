import os
from typing import Any, Generator

import allure
import pytest
from playwright.sync_api import Page

from core.auth import AuthProvider
from core.clients import GraphQLClient
from core.global_settings import GlobalSettings
from core.global_settings import global_settings as _global_settings
from dataset.manager import DatasetManager
from gql.operations.cart_operations import CartOperations
from gql.types.cart import Cart
from gql.types.cart_item_input import CartItemInput
from page_objects.browser_storage import BrowserStorage
from tests.context import Context

_FEATURE_MARKERS = ["quantity_control", "range_filter_type", "checkout_mode"]


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

    screenshot_path = os.path.join(screenshots_dir, f"{request.node.name}.png")
    _page_for_failure.screenshot(path=screenshot_path, full_page=True)

    allure.attach.file(
        screenshot_path,
        name=request.node.name,
        attachment_type=allure.attachment_type.PNG,
    )


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args: dict[Any, Any]) -> dict[Any, Any]:
    return {**browser_context_args, "viewport": {"width": 1920, "height": 1080}}


@pytest.fixture(scope="session")
def global_settings() -> GlobalSettings:
    return _global_settings


@pytest.fixture(scope="session")
def auth(global_settings: GlobalSettings) -> AuthProvider:
    return AuthProvider(global_settings)


@pytest.fixture(scope="session")
def dataset_manager(global_settings: GlobalSettings) -> DatasetManager:
    return DatasetManager.create(global_settings)


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
        provider.sign_in(username, global_settings.users_password)
        if request.node.get_closest_marker("e2e") and provider.token_info:
            page = request.getfixturevalue("page")
            BrowserStorage(page).set_auth(provider.token_info)
    yield provider
    if provider.is_authenticated:
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
    with GraphQLClient(auth=with_user, global_settings=global_settings) as client:
        cart_ops = CartOperations(client)
        cart = cart_ops.add_items_to_cart(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            items=items,
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
        )
        if request.node.get_closest_marker("e2e"):
            page = request.getfixturevalue("page")
            BrowserStorage(page).set_user_id(ctx.user_id)
        yield cart
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
        cart = cart_ops.get_cart(
            store_id=ctx.store_id,
            user_id=user_id,
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
        )
        if cart:
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
