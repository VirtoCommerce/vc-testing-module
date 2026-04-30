import allure
import pytest
from core.clients import GraphQLClient
from gql.operations import ContactOperations
from tests.context import Context

_MAINTAINER_USERNAME = "acme_store_maintainer_1@acme.com"
_TARGET_CONTACT_ID = "contact-acme-store-employee-1"
_ORIGINAL_ROLE = "org-employee"
_TARGET_ROLE = "purchasing-agent"


@pytest.mark.graphql
@pytest.mark.with_user(_MAINTAINER_USERNAME)
@allure.feature("Contact / Roles (GraphQL)")
@allure.title("Change an organization contact's role")
def test_contact_change_role(graphql_client: GraphQLClient, ctx: Context) -> None:
    contact_ops = ContactOperations(client=graphql_client)

    with allure.step(f"Fetch contact {_TARGET_CONTACT_ID}"):
        contact = contact_ops.get_contact(contact_id=_TARGET_CONTACT_ID)
        assert contact is not None and len(contact.security_accounts) == 1
        user_id = contact.security_accounts[0].id

    with allure.step(f"Change role to '{_TARGET_ROLE}' for user {user_id}"):
        result = contact_ops.change_organization_contact_role(
            user_id=user_id, role_ids=[_TARGET_ROLE]
        )
        assert result.succeeded is True

    with allure.step(f"Verify contact has role '{_TARGET_ROLE}'"):
        contact = contact_ops.get_contact(contact_id=_TARGET_CONTACT_ID)
        assert contact is not None

        user = contact.security_accounts[0]
        assert len(user.roles) == 1
        assert user.roles[0].id == _TARGET_ROLE

    with allure.step(f"Teardown: restore original role '{_ORIGINAL_ROLE}'"):
        contact_ops.change_organization_contact_role(
            user_id=user_id, role_ids=[_ORIGINAL_ROLE]
        )
