import pytest
from playwright.sync_api import Page, expect

from fixtures import Auth, Config, GraphQLClient
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.pages import HomePage


@pytest.mark.e2e
def test_e2e_search_bar_user_search_history_single_item(config: Config, page: Page):
    print("Running E2E test to check search history single item...", end=" ")

    home_page = HomePage(page, config)
    home_page.navigate()

    home_page.search_bar.search_input.fill("acer")
    home_page.search_bar.search_button.click()

    expect(page).to_have_url(f"{config['FRONTEND_BASE_URL']}/search?q=acer")

    home_page.navigate()
    home_page.search_bar.search_input.fill("asus")

    expect(home_page.search_bar.suggestions_dropdown.element).to_be_visible()
    expect(
        home_page.search_bar.suggestions_dropdown.search_history_section.element
    ).to_be_visible()
    assert (
        home_page.search_bar.suggestions_dropdown.search_history_section.has_item(
            "acer"
        )
        == True
    )


@pytest.mark.e2e
def test_e2e_search_bar_user_search_history_multiple_items(config: Config, page: Page):
    print("Running E2E test to check search history multiple items...", end=" ")

    home_page = HomePage(page, config)
    home_page.navigate()

    home_page.search_bar.search_input.fill("acer")
    home_page.search_bar.search_button.click()

    expect(page).to_have_url(f"{config['FRONTEND_BASE_URL']}/search?q=acer")

    home_page.navigate()
    home_page.search_bar.search_input.fill("asus")
    home_page.search_bar.search_button.click()

    expect(page).to_have_url(f"{config['FRONTEND_BASE_URL']}/search?q=asus")

    home_page.navigate()
    home_page.search_bar.search_input.fill("lenovo")
    home_page.search_bar.search_button.click()

    expect(page).to_have_url(f"{config['FRONTEND_BASE_URL']}/search?q=lenovo")

    home_page.navigate()
    home_page.search_bar.search_input.focus()

    expect(home_page.search_bar.suggestions_dropdown.element).to_be_visible()
    expect(
        home_page.search_bar.suggestions_dropdown.search_history_section.element
    ).to_be_visible()
    assert (
        home_page.search_bar.suggestions_dropdown.search_history_section.has_item(
            "acer"
        )
        == True
    )
    assert (
        home_page.search_bar.suggestions_dropdown.search_history_section.has_item(
            "asus"
        )
        == True
    )
    assert (
        home_page.search_bar.suggestions_dropdown.search_history_section.has_item(
            "lenovo"
        )
        == True
    )

    history_item = (
        home_page.search_bar.suggestions_dropdown.search_history_section.get_item(
            "acer"
        )
    )

    assert history_item is not None

    history_item.element.click()

    expect(page).to_have_url(f"{config['FRONTEND_BASE_URL']}/search?q=acer")


@pytest.mark.e2e
def test_e2e_search_bar_products_suggestions(config: Config, page: Page):
    print("Running E2E test to check product suggestions items...", end=" ")

    home_page = HomePage(page, config)

    home_page.navigate()
    home_page.search_bar.search_input.fill("acer")

    expect(home_page.search_bar.suggestions_dropdown.element).to_be_visible()
    expect(
        home_page.search_bar.suggestions_dropdown.product_suggestions_section.element
    ).to_be_visible()
    expect(
        home_page.search_bar.suggestions_dropdown.product_suggestions_section.products_list_element
    ).to_be_visible()
    assert (
        home_page.search_bar.suggestions_dropdown.product_suggestions_section.products
        is not None
    )
    assert (
        len(
            home_page.search_bar.suggestions_dropdown.product_suggestions_section.products
        )
        >= 1
    )


@pytest.mark.e2e
def test_e2e_search_bar_products_view_all(config: Config, page: Page):
    print("Running E2E test to check product suggestions view all button...", end=" ")

    home_page = HomePage(page, config)
    home_page.navigate()

    home_page.search_bar.search_input.fill("a")

    expect(
        home_page.search_bar.suggestions_dropdown.product_suggestions_section.element
    ).to_be_visible()
    expect(
        home_page.search_bar.suggestions_dropdown.product_suggestions_section.view_all_button
    ).to_be_visible()

    home_page.search_bar.suggestions_dropdown.product_suggestions_section.view_all_button.click()

    expect(page).to_have_url(f"{config['FRONTEND_BASE_URL']}/search?q=a")


@pytest.mark.e2e
def test_e2e_search_bar_products_pdp(config: Config, page: Page):
    print(
        "Running E2E test to check product suggestions product page navigation...",
        end=" ",
    )

    home_page = HomePage(page, config)
    home_page.navigate()

    home_page.search_bar.search_input.fill("acer")

    expect(home_page.search_bar.suggestions_dropdown.element).to_be_visible()
    expect(
        home_page.search_bar.suggestions_dropdown.product_suggestions_section.element
    ).to_be_visible()
    expect(
        home_page.search_bar.suggestions_dropdown.product_suggestions_section.products_list_element
    ).to_be_visible()

    product = (
        home_page.search_bar.suggestions_dropdown.product_suggestions_section.products[
            0
        ]
    )
    product_path = product.product_link.get_attribute("href")
    product.product_link.click()

    expect(page).to_have_url(f"{config['FRONTEND_BASE_URL']}{product_path}")


@pytest.mark.e2e
def test_e2e_search_bar_empty_query(config: Config, page: Page):
    print(
        "Running E2E test to check empty query behavior...",
        end=" ",
    )

    home_page = HomePage(page, config)
    home_page.navigate()

    home_page.search_bar.search_input.focus()
    home_page.search_bar.search_button.click()

    expect(page).to_have_url(f"{config['FRONTEND_BASE_URL']}/search")


@pytest.mark.e2e
def test_e2e_search_bar_unexisting_item_query(config: Config, page: Page):
    print(
        "Running E2E test to check unexisting item query behavior...",
        end=" ",
    )

    home_page = HomePage(page, config)
    home_page.navigate()

    home_page.search_bar.search_input.fill("unexisting item")

    expect(home_page.search_bar.suggestions_dropdown.element).to_be_visible()
    expect(
        home_page.search_bar.suggestions_dropdown.not_found_section_element
    ).to_be_visible()


@pytest.mark.e2e
def test_e2e_search_bar_history_different_users(
    config: Config, page: Page, auth: Auth, graphql_client: GraphQLClient
):
    print(
        "Running E2E test to check search history for different users...",
        end=" ",
    )

    temp_username_1 = "acme-temp-employee-1@acme.com"
    temp_username_2 = "acme-temp-employee-2@acme.com"

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    auth.authenticate(config["ADMIN_USERNAME"], config["USERS_PASSWORD"])

    temp_registration_info_1 = contact_operations.create_contact(
        payload={
            "storeId": config["STORE_ID"],
            "account": {
                "username": temp_username_1,
                "email": temp_username_1,
                "password": config["USERS_PASSWORD"],
            },
            "contact": {
                "firstName": "Test",
                "lastName": "Employee 1",
            },
        }
    )
    temp_registration_info_2 = contact_operations.create_contact(
        payload={
            "storeId": config["STORE_ID"],
            "account": {
                "username": temp_username_2,
                "email": temp_username_2,
                "password": config["USERS_PASSWORD"],
            },
            "contact": {
                "firstName": "Test",
                "lastName": "Employee 2",
            },
        }
    )

    temp_contact_1 = temp_registration_info_1["contact"]
    temp_contact_2 = temp_registration_info_2["contact"]

    auth.clear_token()

    auth.authenticate(temp_username_1, config["USERS_PASSWORD"], page)

    home_page = HomePage(page, config)
    home_page.navigate()

    home_page.search_bar.search_input.fill("acer")
    home_page.search_bar.search_button.click()

    expect(page).to_have_url(f"{config['FRONTEND_BASE_URL']}/search?q=acer")

    home_page.navigate()
    home_page.search_bar.search_input.focus()

    expect(home_page.search_bar.suggestions_dropdown.element).to_be_visible()
    expect(
        home_page.search_bar.suggestions_dropdown.search_history_section.element
    ).to_be_visible()
    assert (
        home_page.search_bar.suggestions_dropdown.search_history_section.has_item(
            "acer"
        )
        == True
    )

    auth.clear_token()

    auth.authenticate(temp_username_2, config["USERS_PASSWORD"], page)

    home_page.navigate()

    home_page.search_bar.search_input.fill("asus")

    home_page.search_bar.search_button.click()

    expect(page).to_have_url(f"{config['FRONTEND_BASE_URL']}/search?q=asus")

    home_page.navigate()
    home_page.search_bar.search_input.focus()

    expect(home_page.search_bar.suggestions_dropdown.element).to_be_visible()
    expect(
        home_page.search_bar.suggestions_dropdown.search_history_section.element
    ).to_be_visible()
    assert (
        home_page.search_bar.suggestions_dropdown.search_history_section.has_item(
            "asus"
        )
        == True
    )
    assert (
        home_page.search_bar.suggestions_dropdown.search_history_section.has_item(
            "acer"
        )
        == False
    )

    auth.clear_token()

    auth.authenticate(config["ADMIN_USERNAME"], config["USERS_PASSWORD"])

    user_operations.delete_users(
        payload={
            "userNames": [temp_username_1, temp_username_2],
        }
    )

    contact_operations.delete_contact(
        payload={
            "contactId": temp_contact_1["id"],
        }
    )
    contact_operations.delete_contact(
        payload={
            "contactId": temp_contact_2["id"],
        }
    )

    auth.clear_token()
