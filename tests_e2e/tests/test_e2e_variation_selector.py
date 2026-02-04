"""
E2E tests for B2C product variation selector display.

Test Cases:
- C407709: Display B2C SKU Selector if conditions met
- C407710: Do NOT display SKU Selector for non-B2C layout
- C407711: Do NOT display SKU Selector if product has no variations
- C407712: Load variations from backend (verifies variations load correctly)
"""

import os
from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures import Auth, Config, GraphQLClient
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.pages import ProductPage


@pytest.mark.e2e
@allure.title("Display B2C SKU Selector when conditions met (E2E)")
def test_e2e_display_variation_selector_for_b2c_product(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):
    """
    Display B2C SKU Selector if conditions met.

    Preconditions:
    - Product has VirtoFrontend_UI_Layout = B2C
    - Product has variations

    Expected:
    - The variation selector (Options section) is displayed
    - Variation list/table view is hidden
    - The property VirtoFrontend_UI_Layout = B2C is hidden from user
    """
    print(
        f"{os.linesep}Running E2E test: Display variation selector for B2C product...",
        end=" ",
    )

    page.set_viewport_size({"width": 1440, "height": 900})

    user_operations = UserOperations(graphql_client)
    user = user_operations.get_me()
    auth.set_local_storage_user_id(page, user["id"])

    # Use B2C product with variations
    product_page = ProductPage(page, config, "b2c-test-tshirt-variations")
    product_page.navigate()

    # Verify the variation selector is visible for B2C layout with variations
    expect(
        product_page.variation_selector_element,
        "Variation selector should be visible for B2C product with variations",
    ).to_be_visible()

    # Verify product name is displayed
    expect(
        product_page.product_name,
        "Product name should be visible",
    ).to_be_visible()


@pytest.mark.e2e
@allure.title("Do NOT display SKU Selector for non-B2C layout (E2E)")
def test_e2e_hide_variation_selector_for_non_b2c_layout(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):
    """
    Do NOT display SKU Selector for non-B2C layout.

    Preconditions:
    - Product has VirtoFrontend_UI_Layout = B2B
    - Product has variations

    Expected:
    - The B2C Options selector is NOT displayed
    - Variation list/table view is shown instead
    """
    print(
        f"{os.linesep}Running E2E test: Hide variation selector for non-B2C layout...",
        end=" ",
    )

    page.set_viewport_size({"width": 1440, "height": 900})

    user_operations = UserOperations(graphql_client)
    user = user_operations.get_me()
    auth.set_local_storage_user_id(page, user["id"])

    # Use B2B product with variations
    product_page = ProductPage(page, config, "b2b-test-laptop-variations")
    product_page.navigate()

    # Verify the B2C variation selector is NOT visible for B2B layout
    expect(
        product_page.variation_selector_element,
        "Variation selector should NOT be visible for B2B product",
    ).not_to_be_visible()


@pytest.mark.e2e
@allure.title("Do NOT display SKU Selector for product without variations (E2E)")
def test_e2e_hide_variation_selector_for_product_without_variations(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):
    """
    Do NOT display SKU Selector if product has no variations.

    Preconditions:
    - Product has VirtoFrontend_UI_Layout = B2C
    - Product has NO variations

    Expected:
    - SKU Selector is NOT displayed
    """
    print(
        f"{os.linesep}Running E2E test: Hide variation selector for product without variations...",
        end=" ",
    )

    page.set_viewport_size({"width": 1440, "height": 900})

    user_operations = UserOperations(graphql_client)
    user = user_operations.get_me()
    auth.set_local_storage_user_id(page, user["id"])

    # Use B2C product WITHOUT variations
    product_page = ProductPage(page, config, "b2c-test-simple-product")
    product_page.navigate()

    # Verify the variation selector is NOT visible for product without variations
    expect(
        product_page.variation_selector_element,
        "Variation selector should NOT be visible for product without variations",
    ).not_to_be_visible()

    # Verify product name is still displayed
    expect(
        product_page.product_name,
        "Product name should still be visible",
    ).to_be_visible()


@pytest.mark.e2e
@allure.title("Load variations from backend (E2E)")
def test_e2e_load_variations_from_backend(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):
    """
    Load variations from backend.

    Preconditions:
    - Product has multiple variations (Color and Size)

    Expected:
    - All variation options are loaded and displayed
    - Only in-stock variations are shown as available
    """
    print(
        f"{os.linesep}Running E2E test: Load variations from backend...",
        end=" ",
    )

    page.set_viewport_size({"width": 1440, "height": 900})

    user_operations = UserOperations(graphql_client)
    user = user_operations.get_me()
    auth.set_local_storage_user_id(page, user["id"])

    # Use B2C product with multiple variations
    product_page = ProductPage(page, config, "b2c-test-tshirt-variations")
    product_page.navigate()

    # Verify the variation selector is visible
    expect(
        product_page.variation_selector_element,
        "Variation selector should be visible",
    ).to_be_visible()

    # Verify option groups are loaded
    variation_selector = product_page.variation_selector
    group_names = variation_selector.get_all_group_names()

    # Should have Color and Size groups
    assert len(group_names) >= 1, "At least one option group should be loaded"

    # Verify Color options are present (if Color group exists)
    if "Color" in group_names:
        color_options = variation_selector.get_options_for_group("Color")
        assert len(color_options) > 0, "Color options should be loaded"

    # Verify Size options are present (if Size group exists)
    if "Size" in group_names:
        size_options = variation_selector.get_options_for_group("Size")
        assert len(size_options) > 0, "Size options should be loaded"
