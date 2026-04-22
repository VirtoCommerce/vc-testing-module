import pytest
from core.clients import GraphQLClient
from gql.operations import ContactOperations

_MAINTAINER = "acme_store_maintainer_1@acme.com"
_TARGET_CONTACT_ID = "contact-acme-store-employee-1"

_STATUS_APPROVED = "Approved"
_STATUS_LOCKED = "Locked"


@pytest.mark.graphql
@pytest.mark.with_user(_MAINTAINER)
def test_contact_lock_unlock(graphql_client: GraphQLClient) -> None:
    contact_ops = ContactOperations(client=graphql_client)

    try:
        locked = contact_ops.lock_organization_contact(contact_id=_TARGET_CONTACT_ID)
        assert locked.status == _STATUS_LOCKED

        unlocked = contact_ops.unlock_organization_contact(
            contact_id=_TARGET_CONTACT_ID
        )
        assert unlocked.status == _STATUS_APPROVED
    finally:
        contact_ops.unlock_organization_contact(contact_id=_TARGET_CONTACT_ID)
