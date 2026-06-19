import allure
import pytest
from core.clients import GraphQLClient
from gql.operations import ContactOperations

_MAINTAINER = "acme_store_maintainer_1@acme.com"
_TARGET_CONTACT_ID = "contact-acme-store-employee-1"
_ORGANIZATION_ID = "organization-acme-store"


@pytest.mark.graphql
@pytest.mark.optional
@pytest.mark.with_user(_MAINTAINER)
@allure.feature("Contact / Lock (GraphQL)")
@allure.title("Lock and unlock an organization contact")
def test_contact_lock_unlock(graphql_client: GraphQLClient) -> None:
    contact_ops = ContactOperations(client=graphql_client)

    try:
        with allure.step(f"Lock contact {_TARGET_CONTACT_ID}"):
            contact_ops.lock_organization_contact(member_id=_TARGET_CONTACT_ID)

        with allure.step(f"Verify contact is locked in organization {_ORGANIZATION_ID}"):
            assert (
                contact_ops.get_contact_lock_status(contact_id=_TARGET_CONTACT_ID, organization_id=_ORGANIZATION_ID)
                is True
            )

        with allure.step(f"Unlock contact {_TARGET_CONTACT_ID}"):
            contact_ops.unlock_organization_contact(member_id=_TARGET_CONTACT_ID)

        with allure.step(f"Verify contact is unlocked in organization {_ORGANIZATION_ID}"):
            assert (
                contact_ops.get_contact_lock_status(contact_id=_TARGET_CONTACT_ID, organization_id=_ORGANIZATION_ID)
                is False
            )
    finally:
        with allure.step(f"Teardown: ensure contact {_TARGET_CONTACT_ID} is unlocked"):
            contact_ops.unlock_organization_contact(member_id=_TARGET_CONTACT_ID)
