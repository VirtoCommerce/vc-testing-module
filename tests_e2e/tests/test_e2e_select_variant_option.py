"""
E2E tests for variant options on a B2C product page (Sport Band).

Test Cases:
- test_e2e_select_variant_option: Verify variant picker, selection, and stepper behavior
- test_e2e_variant_title_and_price_change: Verify title/price update when switching options
- test_e2e_add_variant_combinations_to_cart: Add 3 variants to cart, verify count labels and cart line items
"""

from typing import Any

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures import Auth, Config, GraphQLClient
from graphql_operations.cart.cart_operations import CartOperations
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.pages import ProductPage

SPORT_BAND_PRODUCT_ID = "product-b2c-test-sport-band"


def _build_seo_path(product: dict, dataset: dict) -> str:
    """Build full SEO path from category hierarchy + product semantic URL."""
    categories_by_id = {c["id"]: c for c in dataset["categories"]}
    parts = []
    category_id = product["categoryId"]
    while category_id:
        cat = categories_by_id[category_id]
        parts.append(cat["seoInfos"][0]["semanticUrl"])
        category_id = cat.get("parentId")
    parts.reverse()
    parts.append(product["seoInfos"][0]["semanticUrl"])
    return "/".join(parts)


def _find_variation(dataset: dict, color: str, size: str, wrist_size: str) -> dict:
    """Find a Sport Band variation by its Color, Size, and WristSize property values."""
    for var in dataset["productVariations"]:
        if var.get("mainProductId") != SPORT_BAND_PRODUCT_ID:
            continue
        props = {p["name"]: p["values"][0]["value"] for p in var["properties"]}
        if props.get("Color") == color and props.get("Size") == size and props.get("WristSize") == wrist_size:
            return var
    raise ValueError(f"No variation found for Color={color}, Size={size}, WristSize={wrist_size}")


def _get_variation_price_usd(dataset: dict, variation_id: str) -> float:
    """Get the USD list price for a variation from the dataset."""
    for price_entry in dataset["prices"]:
        if price_entry["productId"] == variation_id:
            for price in price_entry["prices"]:
                if price["currency"] == "USD":
                    return price["list"]
    raise ValueError(f"No USD price found for variation {variation_id}")


@pytest.mark.e2e
@allure.title("Select variant option on B2C product page (E2E)")
def test_e2e_select_variant_option(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):
    """
    Verify variant option selection behavior on the Sport Band product page.

    Steps:
    1. Navigate to the Sport Band product page
    2. Check that variant picker group is displayed
    3. Check that no variant is selected and Add to Cart button is disabled
    4. Select Color, Size, and Wrist Size options manually
    5. Check that the Add to Cart button changed to a stepper (increase/decrease)
    """
    with allure.step("Prepare browser and navigate to product page"):
        page.set_viewport_size({"width": 1920, "height": 1080})

        product = next(p for p in dataset["products"] if p["id"] == SPORT_BAND_PRODUCT_ID)
        variation_props = [prop for prop in product["properties"] if prop["type"] == "Variation"]
        color_prop = next(p for p in variation_props if p["name"] == "Color")
        color_value = next(v["value"] for v in color_prop["values"] if v["value"] == "Stone Gray")
        size_prop = next(p for p in variation_props if p["name"] == "Size")
        size_value = size_prop["values"][1]["value"]  # 45mm
        wrist_size_prop = next(p for p in variation_props if p["name"] == "WristSize")
        wrist_size_value = wrist_size_prop["values"][0]["value"]  # S/M

        seo_path = _build_seo_path(product, dataset)

        user_operations = UserOperations(graphql_client)
        user = user_operations.get_me()
        auth.set_local_storage_user_id(page, user["id"])

        product_page = ProductPage(page, config, seo_path)
        product_page.navigate()
        page.wait_for_load_state("networkidle")

    with allure.step("Verify variant picker is displayed with no selection"):
        variation_selector = product_page.variation_selector

        expect(
            product_page.variation_selector_element,
            "Variation selector should be visible on the Sport Band product page",
        ).to_be_visible()

        assert not variation_selector.are_all_groups_selected(), "No variant group should be selected initially"
        expect(
            product_page.disabled_add_to_cart_button,
            "Disabled Add to Cart button should be visible when no options are selected",
        ).to_be_visible()

    with allure.step(f"Select Color: {color_value}"):
        assert variation_selector.select_option(
            color_prop["name"], color_value
        ), f"Should be able to select '{color_value}' in '{color_prop['name']}' group"
        page.wait_for_load_state("networkidle")

    with allure.step(f"Select Size: {size_value}"):
        assert variation_selector.select_option(
            size_prop["name"], size_value
        ), f"Should be able to select '{size_value}' in '{size_prop['name']}' group"
        page.wait_for_load_state("networkidle")

    with allure.step(f"Select Wrist Size: {wrist_size_value}"):
        assert variation_selector.select_option(
            wrist_size_prop["name"], wrist_size_value
        ), f"Should be able to select '{wrist_size_value}' in '{wrist_size_prop['name']}' group"
        page.wait_for_load_state("networkidle")

    with allure.step("Verify all groups selected and stepper is visible"):
        assert variation_selector.are_all_groups_selected(), "All option groups should be selected"

        expect(
            product_page.quantity_stepper_input,
            "Quantity stepper input should be visible after full variant selection",
        ).to_be_visible()

        expect(
            product_page.quantity_stepper_increment,
            "Stepper increment button should be visible after full variant selection",
        ).to_be_visible()

        expect(
            product_page.quantity_stepper_decrement,
            "Stepper decrement button should be visible after full variant selection",
        ).to_be_visible()

        expect(
            product_page.disabled_add_to_cart_button,
            "Disabled Add to Cart button should no longer be visible after full variant selection",
        ).not_to_be_visible()


@pytest.mark.e2e
@allure.title("Verify title and price change when switching variant options (E2E)")
def test_e2e_variant_title_and_price_change(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):
    """
    Verify product title and price update when switching between variant options.

    Steps:
    1. Navigate to the Sport Band product page
    2. Select Starlight + 42mm + S/M, verify title and price match dataset
    3. Switch color to Midnight Black, verify title and price changed and match dataset
    """
    with allure.step("Prepare browser and navigate to product page"):
        page.set_viewport_size({"width": 1920, "height": 1080})

        product = next(p for p in dataset["products"] if p["id"] == SPORT_BAND_PRODUCT_ID)
        variation_props = [prop for prop in product["properties"] if prop["type"] == "Variation"]
        color_prop = next(p for p in variation_props if p["name"] == "Color")
        size_prop = next(p for p in variation_props if p["name"] == "Size")
        wrist_size_prop = next(p for p in variation_props if p["name"] == "WristSize")

        first_color = next(v["value"] for v in color_prop["values"] if v["value"] == "Starlight")
        second_color = next(v["value"] for v in color_prop["values"] if v["value"] == "Midnight Black")
        size_value = size_prop["values"][0]["value"]  # 42mm
        wrist_size_value = wrist_size_prop["values"][0]["value"]  # S/M

        first_variation = _find_variation(dataset, first_color, size_value, wrist_size_value)
        first_expected_price = _get_variation_price_usd(dataset, first_variation["id"])

        second_variation = _find_variation(dataset, second_color, size_value, wrist_size_value)
        second_expected_price = _get_variation_price_usd(dataset, second_variation["id"])

        seo_path = _build_seo_path(product, dataset)

        user_operations = UserOperations(graphql_client)
        user = user_operations.get_me()
        auth.set_local_storage_user_id(page, user["id"])

        product_page = ProductPage(page, config, seo_path)
        product_page.navigate()
        page.wait_for_load_state("networkidle")

        variation_selector = product_page.variation_selector

    with allure.step(f"Select first combination: {first_color} + {size_value} + {wrist_size_value}"):
        assert variation_selector.select_option(color_prop["name"], first_color)
        page.wait_for_load_state("networkidle")
        assert variation_selector.select_option(size_prop["name"], size_value)
        page.wait_for_load_state("networkidle")
        assert variation_selector.select_option(wrist_size_prop["name"], wrist_size_value)
        page.wait_for_load_state("networkidle")

    with allure.step(f"Verify title and price for first combination"):
        expect(product_page.product_name).to_have_text(first_variation["name"])

        first_displayed_price = product_page.get_current_price()
        assert first_displayed_price is not None, "Price should be visible after selecting variant"
        assert (
            first_displayed_price == f"${first_expected_price:.2f}"
        ), f"Expected price '${first_expected_price:.2f}', got '{first_displayed_price}'"

    with allure.step(f"Switch color to {second_color}"):
        assert variation_selector.select_option(color_prop["name"], second_color)
        page.wait_for_load_state("networkidle")

    with allure.step(f"Verify title and price changed for second combination"):
        expect(product_page.product_name).to_have_text(second_variation["name"])

        second_displayed_price = product_page.get_current_price()
        assert second_displayed_price is not None, "Price should be visible after switching color"
        assert (
            second_displayed_price != first_displayed_price
        ), f"Price should change after switching color, but both are '{first_displayed_price}'"
        assert (
            second_displayed_price == f"${second_expected_price:.2f}"
        ), f"Expected price '${second_expected_price:.2f}', got '{second_displayed_price}'"


@pytest.mark.e2e
@allure.title("Add 3 variant combinations to cart and verify cart line items (E2E)")
def test_e2e_add_variant_combinations_to_cart(
    config: Config,
    auth: Auth,
    graphql_client: GraphQLClient,
    page: Page,
    dataset: dict[str, Any],
):
    """
    Add 3 different variant combinations to cart and verify cart contents.

    Steps:
    1. Navigate to the Sport Band product page
    2. Select Light Blush + 45mm + S/M, click increase, check count-in-cart-label
    3. Select Purple Fog + 42mm + S/M, click increase, check count-in-cart-label
    4. Select Neon Yellow + 49mm + M/L, click increase, check count-in-cart-label
    5. Verify cart badge shows correct count
    """
    with allure.step("Prepare browser and navigate to product page"):
        page.set_viewport_size({"width": 1920, "height": 1080})

        product = next(p for p in dataset["products"] if p["id"] == SPORT_BAND_PRODUCT_ID)
        variation_props = [prop for prop in product["properties"] if prop["type"] == "Variation"]
        color_prop = next(p for p in variation_props if p["name"] == "Color")
        size_prop = next(p for p in variation_props if p["name"] == "Size")
        wrist_size_prop = next(p for p in variation_props if p["name"] == "WristSize")

        combinations = [
            {
                "color": next(v["value"] for v in color_prop["values"] if v["value"] == "Light Blush"),
                "size": size_prop["values"][1]["value"],  # 45mm
                "wrist_size": wrist_size_prop["values"][0]["value"],  # S/M
            },
            {
                "color": next(v["value"] for v in color_prop["values"] if v["value"] == "Purple Fog"),
                "size": size_prop["values"][0]["value"],  # 42mm
                "wrist_size": wrist_size_prop["values"][0]["value"],  # S/M
            },
            {
                "color": next(v["value"] for v in color_prop["values"] if v["value"] == "Neon Yellow"),
                "size": size_prop["values"][2]["value"],  # 49mm
                "wrist_size": wrist_size_prop["values"][1]["value"],  # M/L
            },
        ]

        variations = []
        for combo in combinations:
            var = _find_variation(dataset, combo["color"], combo["size"], combo["wrist_size"])
            variations.append(var)

        seo_path = _build_seo_path(product, dataset)

    with allure.step("Authenticate and open product page"):
        user_operations = UserOperations(graphql_client)
        cart_operations = CartOperations(graphql_client)

        dataset_user = dataset["users"][0]
        auth.authenticate(dataset_user["userName"], config["USERS_PASSWORD"], page)
        user = user_operations.get_me()

        product_page = ProductPage(page, config, seo_path)
        product_page.navigate()
        page.wait_for_load_state("networkidle")

    try:
        for i, combo in enumerate(combinations):
            with allure.step(
                f"Select and add combination {i + 1}: {combo['color']} + {combo['size']} + {combo['wrist_size']}"
            ):
                page.wait_for_load_state("networkidle")
                variation_selector = product_page.variation_selector

                expect(
                    product_page.variation_selector_element,
                    "Variation selector should be visible on the Sport Band product page",
                ).to_be_visible()

                assert variation_selector.select_option(color_prop["name"], combo["color"])
                page.wait_for_load_state("networkidle")

                expected_name = variations[i]["name"]
                current_name = product_page.product_name.text_content() or ""
                if current_name.strip() != expected_name:
                    assert variation_selector.select_option(size_prop["name"], combo["size"])
                    page.wait_for_load_state("networkidle")
                    assert variation_selector.select_option(wrist_size_prop["name"], combo["wrist_size"])
                    page.wait_for_load_state("networkidle")

                expect(product_page.product_name).to_have_text(expected_name)

                product_page.quantity_stepper_increment.click()
                page.wait_for_load_state("networkidle")

                expect(
                    product_page.count_in_cart_label,
                    f"Count in cart label should be visible after adding combination {i + 1}",
                ).to_be_visible()

        with allure.step(f"Verify cart badge shows {len(combinations)} items"):
            expect(product_page.cart_badge).to_have_text(str(len(combinations)))
    finally:
        with allure.step("Cleanup: remove cart"):
            cart = cart_operations.get_cart(
                store_id=config["STORE_ID"],
                user_id=user["id"],
                currency_code="USD",
                culture_name="en-US",
            )
            if cart and cart.get("id"):
                cart_operations.remove_cart(payload={"cartId": cart["id"], "userId": user["id"]})
            auth.clear_token()
