import allure
import pytest
from core.clients import GraphQLClient
from gql.operations import CartOperations, ProductOperations
from gql.types import (
    CartConfigurationItem,
    CartItemInput,
    ConfigurableProductOptionInput,
    ConfigurationSectionInput,
    ProductConfiguration,
)
from tests.context import Context

_PRODUCT_ID = "laptop-acer-predator-helios-neo-16-ai"
_CONFIGURED_SKU = f"Configuration-{_PRODUCT_ID}"
# Index used to pick a distinct option per section (each section has 3 options).
_LAST_OPTION_INDEX = 99


def _selection(
    config: ProductConfiguration, index: int
) -> list[ConfigurationSectionInput]:
    """Build a strongly typed selection picking one option per section.

    ``index`` beyond a section's option count falls back to the last option,
    which makes it easy to build two distinct selections for the same product.
    """
    sections: list[ConfigurationSectionInput] = []
    for section in config.configuration_sections:
        if not section.options:
            continue
        option = (
            section.options[index]
            if index < len(section.options)
            else section.options[-1]
        )
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


def _get_configuration(
    product_ops: ProductOperations, ctx: Context
) -> ProductConfiguration:
    config = product_ops.get_product_configuration(
        configurable_product_id=_PRODUCT_ID,
        store_id=ctx.store_id,
        user_id=ctx.user_id,
        culture_name=ctx.culture_name,
        currency_code=ctx.currency_code,
    )
    assert config is not None
    assert len(config.configuration_sections) > 0
    return config


@pytest.mark.graphql
@allure.feature("Cart / Configurable product (GraphQL)")
@allure.title("Add a configured product to the cart")
def test_cart_add_configured_item(
    graphql_client: GraphQLClient, ctx: Context
) -> None:
    product_ops = ProductOperations(client=graphql_client)
    cart_ops = CartOperations(client=graphql_client)

    with allure.step(f"Get configuration for {_PRODUCT_ID}"):
        config = _get_configuration(product_ops, ctx)
        selection = _selection(config, 0)

    cart = None
    try:
        with allure.step("Add the configured product to the cart"):
            cart = cart_ops.add_items_to_cart(
                store_id=ctx.store_id,
                user_id=ctx.user_id,
                items=[
                    CartItemInput(
                        product_id=_PRODUCT_ID,
                        quantity=1,
                        configuration_sections=selection,
                    )
                ],
                currency_code=ctx.currency_code,
                culture_name=ctx.culture_name,
            )

        with allure.step("Verify a configured line item was created"):
            assert cart.items_count == 1
            line_item = cart.items[0]
            assert line_item.product_id == _PRODUCT_ID
            assert line_item.sku == _CONFIGURED_SKU
            assert len(line_item.configuration_items) == len(selection)

        with allure.step("Verify the configured components match the selection"):
            selected_ids = {c.product_id for c in line_item.configuration_items}
            expected_ids = {s.option.product_id for s in selection if s.option}
            assert selected_ids == expected_ids
            for item in line_item.configuration_items:
                assert isinstance(item, CartConfigurationItem)
                assert item.section_id
                assert item.name
    finally:
        if cart:
            cart_ops.delete_cart(cart_id=cart.id, user_id=ctx.user_id)


@pytest.mark.graphql
@allure.feature("Cart / Configurable product (GraphQL)")
@allure.title("Change the configuration of a cart line item")
def test_cart_change_configured_item(
    graphql_client: GraphQLClient, ctx: Context
) -> None:
    product_ops = ProductOperations(client=graphql_client)
    cart_ops = CartOperations(client=graphql_client)

    with allure.step(f"Get configuration for {_PRODUCT_ID}"):
        config = _get_configuration(product_ops, ctx)
        first_selection = _selection(config, 0)
        second_selection = _selection(config, _LAST_OPTION_INDEX)

    cart = None
    try:
        with allure.step("Add the configured product with the first selection"):
            cart = cart_ops.add_items_to_cart(
                store_id=ctx.store_id,
                user_id=ctx.user_id,
                items=[
                    CartItemInput(
                        product_id=_PRODUCT_ID,
                        quantity=1,
                        configuration_sections=first_selection,
                    )
                ],
                currency_code=ctx.currency_code,
                culture_name=ctx.culture_name,
            )
            line_item = cart.items[0]
            original_ids = {c.product_id for c in line_item.configuration_items}

        with allure.step("Change the configuration to the second selection"):
            updated_cart = cart_ops.change_cart_configured_item(
                store_id=ctx.store_id,
                user_id=ctx.user_id,
                line_item_id=line_item.id,
                configuration_sections=second_selection,
                cart_id=cart.id,
                currency_code=ctx.currency_code,
                culture_name=ctx.culture_name,
            )

        with allure.step("Verify the same line item now reflects the new configuration"):
            assert updated_cart.items_count == 1
            updated_item = updated_cart.items[0]
            assert updated_item.id == line_item.id
            updated_ids = {c.product_id for c in updated_item.configuration_items}
            assert updated_ids == {
                s.option.product_id for s in second_selection if s.option
            }
            assert updated_ids != original_ids
    finally:
        if cart:
            cart_ops.delete_cart(cart_id=cart.id, user_id=ctx.user_id)


@pytest.mark.graphql
@allure.feature("Cart / Configurable product (GraphQL)")
@allure.title("Remove a configured line item from the cart")
def test_cart_remove_configured_item(
    graphql_client: GraphQLClient, ctx: Context
) -> None:
    product_ops = ProductOperations(client=graphql_client)
    cart_ops = CartOperations(client=graphql_client)

    with allure.step(f"Get configuration for {_PRODUCT_ID}"):
        config = _get_configuration(product_ops, ctx)
        selection = _selection(config, 0)

    cart = None
    try:
        with allure.step("Add the configured product to the cart"):
            cart = cart_ops.add_items_to_cart(
                store_id=ctx.store_id,
                user_id=ctx.user_id,
                items=[
                    CartItemInput(
                        product_id=_PRODUCT_ID,
                        quantity=1,
                        configuration_sections=selection,
                    )
                ],
                currency_code=ctx.currency_code,
                culture_name=ctx.culture_name,
            )
            assert cart.items_count == 1
            line_item = cart.items[0]

        with allure.step("Remove the configured line item"):
            updated_cart = cart_ops.remove_cart_item(
                store_id=ctx.store_id,
                user_id=ctx.user_id,
                line_item_id=line_item.id,
                cart_id=cart.id,
            )

        with allure.step("Verify the configured line item is gone"):
            assert updated_cart.items_count == 0
            assert not any(i.id == line_item.id for i in updated_cart.items)
    finally:
        if cart:
            cart_ops.delete_cart(cart_id=cart.id, user_id=ctx.user_id)
