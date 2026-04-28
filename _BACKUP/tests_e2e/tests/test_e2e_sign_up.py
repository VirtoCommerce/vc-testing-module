import os
import random

import pytest
from playwright.sync_api import Page, expect

from fixtures import Auth, Config, GraphQLClient, WebAPISession
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.pages import SignUpPage, SuccessfulRegistrationPage


@pytest.mark.e2e
def test_e2e_select_personal_registration(config: Config, page: Page):
    print(f"{os.linesep}Running E2E test to select personal registration...", end=" ")

    sign_up_page = SignUpPage(config, page)

    sign_up_page.navigate()

    sign_up_page.select_personal_registration()

    expect(sign_up_page.organization_name_input).not_to_be_visible(), "Organization name input is visible"


@pytest.mark.e2e
def test_e2e_select_organization_registration(config: Config, page: Page):
    print(f"{os.linesep}Running E2E test to select organization registration...", end=" ")

    sign_up_page = SignUpPage(config, page)

    sign_up_page.navigate()

    sign_up_page.select_organization_registration()

    expect(sign_up_page.organization_name_input).to_be_visible(), "Organization name input is not visible"


@pytest.mark.e2e
def test_e2e_sign_up_personal_account(
    config: Config,
    page: Page,
    auth: Auth,
    graphql_client: GraphQLClient,
):
    print(f"{os.linesep}Running E2E test to sign up personal account...", end=" ")

    sign_up_page = SignUpPage(config, page)
    successful_registration_page = SuccessfulRegistrationPage(config, page)
    contact_operations = ContactOperations(graphql_client)
    user_operations = UserOperations(graphql_client)

    sign_up_page.navigate()

    user_email = f"john.doe-{random.randint(1000, 9999)}@example.com"

    sign_up_page.select_personal_registration()
    sign_up_page.sign_up(
        first_name="John",
        last_name="Doe",
        email=user_email,
        password=config["USERS_PASSWORD"],
    )

    expect(page).to_have_url(successful_registration_page.url)

    # Test teardown

    auth.authenticate(config["ADMIN_USERNAME"], config["ADMIN_PASSWORD"])

    user = user_operations.get_user_by_username(user_email)

    contact_operations.delete_contact(
        payload={
            "contactId": user["contact"]["id"],
        }
    )

    user_operations.delete_users(
        payload={
            "userNames": [user_email],
        }
    )

    auth.clear_token()


@pytest.mark.e2e
def test_e2e_sign_up_organization_account(
    config: Config,
    page: Page,
    auth: Auth,
    graphql_client: GraphQLClient,
    webapi_client: WebAPISession,
):
    print(f"{os.linesep}Running E2E test to sign up organization account...", end=" ")

    sign_up_page = SignUpPage(config, page)
    successful_registration_page = SuccessfulRegistrationPage(config, page)
    contact_operations = ContactOperations(graphql_client)
    user_operations = UserOperations(graphql_client)
    sign_up_page.navigate()

    user_email = f"john.doe-{random.randint(1000, 9999)}@example.com"

    sign_up_page.select_organization_registration()
    sign_up_page.sign_up(
        first_name="John",
        last_name="Doe",
        email=user_email,
        password=config["USERS_PASSWORD"],
        organization_name="Some fake organization",
    )

    expect(page).to_have_url(successful_registration_page.url)

    auth.authenticate(user_email, config["USERS_PASSWORD"])
    get_me = user_operations.get_me()
    organization_id = get_me["contact"]["organizationId"]
    assert organization_id, "Expected organizationId from get_me response"

    # Test teardown

    auth.authenticate(config["ADMIN_USERNAME"], config["ADMIN_PASSWORD"])

    user = user_operations.get_user_by_username(user_email)

    contact_operations.delete_contact(
        payload={
            "contactId": user["contact"]["id"],
        }
    )

    user_operations.delete_users(
        payload={
            "userNames": [user_email],
        }
    )

    webapi_client.delete(f"/api/members?ids={organization_id}")

    response = webapi_client.get(f"/api/members?ids={organization_id}")
    assert response == [], "Expected empty response"

    auth.clear_token()
