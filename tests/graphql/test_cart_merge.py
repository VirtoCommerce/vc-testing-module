from typing import Any

import allure
import pytest
from core.auth import AuthProvider
from core.clients import GraphQLClient
from core.global_settings import GlobalSettings
from gql.operations import CartOperations, ProductOperations
from gql.types import (
    CartItemInput,
    ConfigurableProductOptionInput,
    ConfigurationSectionInput,
    ProductConfiguration,
)
from gql.types.cart import Cart
from tests.context import Context

from utils.line_item_utils import has_line_item

_USER = "acme_store_employee_1@acme.com"
_PRODUCT_ID_1 = "smartphone-apple-iphone-17-256gb-black"
_PRODUCT_ID_2 = "smartphone-apple-iphone-17-256gb-mist-blue"
_QTY_1 = 2
_QTY_2 = 1

_REGULAR_PRODUCT_ID = "smartphone-apple-iphone-17-256gb-black"
_REGULAR_QTY = 2
_CONFIGURABLE_PRODUCT_ID = "laptop-acer-predator-helios-neo-16-ai"
_CONFIGURED_SKU = f"Configuration-{_CONFIGURABLE_PRODUCT_ID}"


def _first_option_selection(
    config: ProductConfiguration,
) -> list[ConfigurationSectionInput]:
    sections: list[ConfigurationSectionInput] = []
    for section in config.configuration_sections:
        if not section.options:
            continue
        option = section.options[0]
        assert option.product is not None
        sections.append(
            ConfigurationSectionInput(
                section_id=section.id,
                type=section.type,
                option=ConfigurableProductOptionInput(
                    product_id=option.product.id,
                    quantity=option.quantity,
                ),
            )
        )
    return sections


@pytest.mark.graphql
@pytest.mark.with_cart([(_PRODUCT_ID_1, _QTY_1), (_PRODUCT_ID_2, _QTY_2)])
@allure.feature("Cart / Merge (GraphQL)")
@allure.title("Merge an anonymous cart into a registered user's cart")
def test_cart_merge(
    with_cart: Cart,
    with_user: AuthProvider,
    graphql_client: GraphQLClient,
    ctx: Context,
    dataset: dict[str, list[dict[str, Any]]],
    global_settings: GlobalSettings,
) -> None:
    anon_cart = with_cart

    user = next(u for u in dataset["users"] if u["userName"] == _USER)
    user_id = user["id"]

    with allure.step(f"Sign in as {_USER}"):
        with_user.sign_in(_USER, global_settings.users_password)

    cart_ops = CartOperations(client=graphql_client)

    with allure.step(f"Merge anonymous cart {anon_cart.id} into user's cart"):
        merged_cart = cart_ops.merge_cart(
            store_id=ctx.store_id,
            user_id=user_id,
            second_cart_id=anon_cart.id,
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
        )
    try:
        with allure.step("Verify merged cart contains items from anonymous cart"):
            assert merged_cart.items_count == 2
            assert has_line_item(merged_cart.items, _PRODUCT_ID_1, _QTY_1)
            assert has_line_item(merged_cart.items, _PRODUCT_ID_2, _QTY_2)
    finally:
        with allure.step(f"Teardown: delete cart {merged_cart.id}"):
            cart_ops.delete_cart(cart_id=merged_cart.id, user_id=user_id)


@pytest.mark.graphql
@allure.feature("Cart / Merge (GraphQL)")
@allure.title(
    "Merge an anonymous cart with a configured item into a user's cart with a regular item"
)
def test_cart_merge_configured_and_regular(
    with_user: AuthProvider,
    graphql_client: GraphQLClient,
    ctx: Context,
    dataset: dict[str, list[dict[str, Any]]],
    global_settings: GlobalSettings,
) -> None:
    product_ops = ProductOperations(client=graphql_client)
    cart_ops = CartOperations(client=graphql_client)

    with allure.step("As anonymous user, build a cart with a configured product"):
        config = product_ops.get_product_configuration(
            configurable_product_id=_CONFIGURABLE_PRODUCT_ID,
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            culture_name=ctx.culture_name,
            currency_code=ctx.currency_code,
        )
        assert config is not None
        selection = _first_option_selection(config)
        anon_cart = cart_ops.add_items_to_cart(
            store_id=ctx.store_id,
            user_id=ctx.user_id,
            items=[
                CartItemInput(
                    product_id=_CONFIGURABLE_PRODUCT_ID,
                    quantity=1,
                    configuration_sections=selection,
                )
            ],
            currency_code=ctx.currency_code,
            culture_name=ctx.culture_name,
        )
        assert anon_cart.items_count == 1

    user = next(u for u in dataset["users"] if u["userName"] == _USER)
    user_id = user["id"]

    with allure.step(f"Sign in as {_USER}"):
        with_user.sign_in(_USER, global_settings.users_password)

    merged_cart = None
    try:
        with allure.step("Seed the registered user's cart with a regular product"):
            cart_ops.add_items_to_cart(
                store_id=ctx.store_id,
                user_id=user_id,
                items=[
                    CartItemInput(
                        product_id=_REGULAR_PRODUCT_ID, quantity=_REGULAR_QTY
                    )
                ],
                currency_code=ctx.currency_code,
                culture_name=ctx.culture_name,
            )

        with allure.step(
            f"Merge anonymous cart {anon_cart.id} into the user's cart"
        ):
            merged_cart = cart_ops.merge_cart(
                store_id=ctx.store_id,
                user_id=user_id,
                second_cart_id=anon_cart.id,
                currency_code=ctx.currency_code,
                culture_name=ctx.culture_name,
            )

        with allure.step(
            "Verify the merged cart contains both the regular and configured items"
        ):
            assert merged_cart.items_count == 2
            assert has_line_item(
                merged_cart.items, _REGULAR_PRODUCT_ID, _REGULAR_QTY
            )
            configured_item = next(
                (i for i in merged_cart.items if i.sku == _CONFIGURED_SKU), None
            )
            assert configured_item is not None
            assert configured_item.product_id == _CONFIGURABLE_PRODUCT_ID
            assert len(configured_item.configuration_items) == len(selection)
            selected_ids = {
                c.product_id for c in configured_item.configuration_items
            }
            expected_ids = {s.option.product_id for s in selection if s.option}
            assert selected_ids == expected_ids
    finally:
        if merged_cart:
            with allure.step(f"Teardown: delete cart {merged_cart.id}"):
                cart_ops.delete_cart(cart_id=merged_cart.id, user_id=user_id)
