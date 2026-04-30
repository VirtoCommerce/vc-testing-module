import allure
import pytest
from core.auth import AuthProvider
from core.clients import GraphQLClient
from core.global_settings import GlobalSettings
from gql.operations import ContactOperations, UserOperations
from tests.context import Context

from utils.polling_utils import poll_until

_PERSONAL_FIRST_NAME = "John"
_PERSONAL_LAST_NAME = "Doe"
_PERSONAL_EMAIL = "test-register-personal@example.com"

_ORG_FIRST_NAME = "Jane"
_ORG_LAST_NAME = "Smith"
_ORG_EMAIL = "test-register-org@example.com"
_ORG_NAME = "Test Registration Org"

_STATUS_APPROVED = "Approved"


def _admin_client(global_settings: GlobalSettings) -> GraphQLClient:
    admin = AuthProvider(global_settings)
    admin.sign_in(global_settings.admin_username, global_settings.admin_password)
    return GraphQLClient(auth=admin, global_settings=global_settings)


@pytest.mark.graphql
@allure.feature("Contact / Registration (GraphQL)")
@allure.title("Register a personal (no-organization) contact")
def test_register_personal_contact(
    graphql_client: GraphQLClient, ctx: Context, global_settings: GlobalSettings
) -> None:
    with allure.step(f"Register personal contact with email '{_PERSONAL_EMAIL}'"):
        reg = ContactOperations(client=graphql_client).request_registration(
            store_id=ctx.store_id,
            language_code=ctx.culture_name,
            first_name=_PERSONAL_FIRST_NAME,
            last_name=_PERSONAL_LAST_NAME,
            email=_PERSONAL_EMAIL,
            password=global_settings.users_password.get_secret_value(),
        )

    with allure.step("Verify registration result"):
        assert reg.result.succeeded is True
        assert reg.organization is None
        assert reg.contact.first_name == _PERSONAL_FIRST_NAME
        assert reg.contact.last_name == _PERSONAL_LAST_NAME
        assert reg.account.email == _PERSONAL_EMAIL

    contact_id = reg.contact.id

    try:
        with allure.step(
            f"Verify contact {contact_id} exists with status '{_STATUS_APPROVED}'"
        ):
            with _admin_client(global_settings) as admin_client:
                admin_contact_ops = ContactOperations(client=admin_client)
                contact = poll_until(
                    fetch=lambda: admin_contact_ops.get_contact(contact_id),
                    predicate=lambda _: True,
                    attempts=global_settings.poll_attempts,
                    interval=global_settings.poll_interval,
                )

                assert (
                    contact is not None
                ), f"Contact '{contact_id}' not found after polling"
                assert contact.first_name == _PERSONAL_FIRST_NAME
                assert contact.last_name == _PERSONAL_LAST_NAME
                assert contact.status == _STATUS_APPROVED
                assert contact.organizations_ids == []
    finally:
        with allure.step(f"Teardown: delete user and contact for '{_PERSONAL_EMAIL}'"):
            with _admin_client(global_settings) as admin_client:
                UserOperations(client=admin_client).delete_users(
                    user_names=[_PERSONAL_EMAIL]
                )
                ContactOperations(client=admin_client).delete_contact(
                    contact_id=contact_id
                )


@pytest.mark.graphql
@allure.feature("Contact / Registration (GraphQL)")
@allure.title("Register a contact with a new organization")
def test_register_organization_contact(
    graphql_client: GraphQLClient, ctx: Context, global_settings: GlobalSettings
) -> None:
    with allure.step(
        f"Register organization '{_ORG_NAME}' with contact '{_ORG_EMAIL}'"
    ):
        reg = ContactOperations(client=graphql_client).request_registration(
            store_id=ctx.store_id,
            language_code=ctx.culture_name,
            first_name=_ORG_FIRST_NAME,
            last_name=_ORG_LAST_NAME,
            email=_ORG_EMAIL,
            password=global_settings.users_password.get_secret_value(),
            organization_name=_ORG_NAME,
        )

    with allure.step("Verify registration result includes organization"):
        assert reg.result.succeeded is True
        assert reg.organization is not None
        assert reg.organization.name == _ORG_NAME
        assert reg.contact.first_name == _ORG_FIRST_NAME
        assert reg.contact.last_name == _ORG_LAST_NAME
        assert reg.account.email == _ORG_EMAIL

    contact_id = reg.contact.id
    organization_id = reg.organization.id

    try:
        with allure.step(
            f"Verify contact {contact_id} belongs to organization {organization_id}"
        ):
            with _admin_client(global_settings) as admin_client:
                admin_contact_ops = ContactOperations(client=admin_client)
                contact = poll_until(
                    fetch=lambda: admin_contact_ops.get_contact(contact_id),
                    predicate=lambda c: organization_id in c.organizations_ids,
                    attempts=global_settings.poll_attempts,
                    interval=global_settings.poll_interval,
                )

                assert (
                    contact is not None
                ), f"Contact '{contact_id}' not found after polling"
                assert contact.first_name == _ORG_FIRST_NAME
                assert contact.last_name == _ORG_LAST_NAME
                assert contact.status == _STATUS_APPROVED
                assert organization_id in contact.organizations_ids
    finally:
        with allure.step(
            f"Teardown: delete user '{_ORG_EMAIL}', contact {contact_id}, organization {organization_id}"
        ):
            with _admin_client(global_settings) as admin_client:
                UserOperations(client=admin_client).delete_users(
                    user_names=[_ORG_EMAIL]
                )
                ContactOperations(client=admin_client).delete_contact(
                    contact_id=contact_id
                )
                ContactOperations(client=admin_client).delete_contact(
                    contact_id=organization_id
                )
