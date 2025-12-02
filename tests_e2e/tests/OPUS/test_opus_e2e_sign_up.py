import os
import re
from typing import Any, Dict

import allure
import pytest
from playwright.sync_api import Page, expect

from fixtures.auth import Auth
from fixtures.graphql_client import GraphQLClient
from graphql_operations.contact.contact_operations import ContactOperations
from graphql_operations.user.user_operations import UserOperations
from tests_e2e.pages.sign_up_page import SignUpPage
from tests_e2e.pages.successful_registration_page import SuccessfulRegistrationPage


@pytest.mark.e2e
@pytest.mark.skip(reason="not needed on opus")
@allure.feature("Select personal registration (E2E)")
def test_e2e_select_personal_registration(config: Dict[str, Any], page: Page):
    print(f"{os.linesep}Running E2E test to select personal registration...", end=" ")

    sign_up_page = SignUpPage(config, page)

    sign_up_page.navigate()

    #sign_up_page.select_personal_registration()

    expect(
        sign_up_page.organization_name_input
    ).not_to_be_visible(), "Organization name input is visible"


@pytest.mark.e2e
@pytest.mark.skip(reason="not needed on opus")
@allure.feature("Select organization registration (E2E)")
def test_e2e_select_organization_registration(config: Dict[str, Any], page: Page):
    print(
        f"{os.linesep}Running E2E test to select organization registration...", end=" "
    )

    sign_up_page = SignUpPage(config, page)

    sign_up_page.navigate()

    sign_up_page.select_organization_registration()

    expect(
        sign_up_page.organization_name_input
    ).to_be_visible(), "Organization name input is not visible"


@pytest.mark.e2e
@allure.feature("Sign up personal account (E2E)")
def test_e2e_sign_up_personal_account(
    config: Dict[str, Any],
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

    #sign_up_page.select_personal_registration()
    sign_up_page.sign_up(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        password=config["users_password"],
        phone="1234567890",
        job_title="Software Engineer",
        discovery_way="Google",
        organization_name="Some fake organization",
        zip="123456"
    )

    expect(page).to_have_url(re.compile(r".*successful-registration.*"))

    # Test teardown

    auth.authenticate(config["admin_username"], config["admin_password"])

    user = user_operations.get_user_by_username("john.doe@example.com")

    contact_operations.delete_contact(
        payload={
            "contactId": user["contact"]["id"],
        }
    )

    user_operations.delete_users(
        payload={
            "userNames": ["john.doe@example.com"],
        }
    )

    auth.clear_token()

'''
@pytest.mark.e2e
@pytest.mark.skip(reason="not needed on opus")
@allure.feature("Sign up organization account (E2E)")
def test_e2e_sign_up_organization_account(
    config: Dict[str, Any], page: Page, auth: Auth, graphql_client: GraphQLClient
):
    print(f"{os.linesep}Running E2E test to sign up organization account...", end=" ")

    sign_up_page = SignUpPage(config, page)
    successful_registration_page = SuccessfulRegistrationPage(config, page)
    contact_operations = ContactOperations(graphql_client)
    user_operations = UserOperations(graphql_client)

    sign_up_page.navigate()

    sign_up_page.select_organization_registration()
    sign_up_page.sign_up(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        password=config["users_password"],
        organization_name="Some fake organization",
    )

    expect(page).to_have_url(successful_registration_page.url)

    # Test teardown

    auth.authenticate(config["admin_username"], config["admin_password"])

    user = user_operations.get_user_by_username("john.doe@example.com")

    contact_operations.delete_contact(
        payload={
            "contactId": user["contact"]["id"],
        }
    )

    user_operations.delete_users(
        payload={
            "userNames": ["john.doe@example.com"],
        }
    )

    auth.clear_token()
'''