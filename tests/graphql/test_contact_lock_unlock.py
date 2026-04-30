import allure
import pytest
from core.clients import GraphQLClient
from gql.operations import ContactOperations

_MAINTAINER = "acme_store_maintainer_1@acme.com"
_TARGET_CONTACT_ID = "contact-acme-store-employee-1"

_STATUS_APPROVED = "Approved"
_STATUS_LOCKED = "Locked"


@pytest.mark.graphql
@pytest.mark.with_user(_MAINTAINER)
@allure.feature("Contact / Lock (GraphQL)")
@allure.title("Lock and unlock an organization contact")
def test_contact_lock_unlock(graphql_client: GraphQLClient) -> None:
    contact_ops = ContactOperations(client=graphql_client)

    try:
        with allure.step(f"Lock contact {_TARGET_CONTACT_ID}"):
            locked = contact_ops.lock_organization_contact(
                contact_id=_TARGET_CONTACT_ID
            )

        with allure.step(f"Verify contact status is '{_STATUS_LOCKED}'"):
            assert locked.status == _STATUS_LOCKED

        with allure.step(f"Unlock contact {_TARGET_CONTACT_ID}"):
            unlocked = contact_ops.unlock_organization_contact(
                contact_id=_TARGET_CONTACT_ID
            )

        with allure.step(f"Verify contact status is back to '{_STATUS_APPROVED}'"):
            assert unlocked.status == _STATUS_APPROVED
    finally:
        with allure.step(f"Teardown: ensure contact {_TARGET_CONTACT_ID} is unlocked"):
            contact_ops.unlock_organization_contact(contact_id=_TARGET_CONTACT_ID)
