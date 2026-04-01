import time
import uuid

import pytest

from core.auth import AuthProvider
from core.clients import GraphQLClient
from core.global_settings import GlobalSettings
from gql.operations import ContactOperations, UserOperations
from tests.context import Context

_MAINTAINER = "acme_store_maintainer_1@acme.com"
_ROLE_EMPLOYEE = "org-employee"
_STATUS_INVITED = "Invited"

_POLL_INTERVAL = 2  # seconds between retries
_POLL_ATTEMPTS = 10  # max retries waiting for indexing


@pytest.mark.graphql
@pytest.mark.with_user(_MAINTAINER)
def test_user_invite(
    graphql_client: GraphQLClient, ctx: Context, global_settings: GlobalSettings
) -> None:
    email = f"test-invite-{uuid.uuid4().hex[:8]}@example.com"
    assert ctx.organization_id is not None

    user_ops = UserOperations(client=graphql_client)
    contact_ops = ContactOperations(client=graphql_client)

    result = user_ops.invite_user(
        store_id=ctx.store_id,
        emails=[email],
        organization_id=ctx.organization_id,
        role_ids=[_ROLE_EMPLOYEE],
    )
    assert result.succeeded is True

    try:
        invited_contact = None
        for _ in range(_POLL_ATTEMPTS):
            contacts = contact_ops.get_organization_contacts(
                organization_id=ctx.organization_id,
                search_phrase=email,
            )
            invited_contact = next(
                (
                    c
                    for c in contacts
                    if c.status == _STATUS_INVITED
                    and any(a.user_name == email for a in c.security_accounts)
                ),
                None,
            )
            if invited_contact is not None:
                break
            time.sleep(_POLL_INTERVAL)

        assert (
            invited_contact is not None
        ), f"Invited contact '{email}' not found after polling"
        assert invited_contact.status == _STATUS_INVITED
        assert any(a.user_name == email for a in invited_contact.security_accounts)
    finally:
        admin = AuthProvider(global_settings)
        admin.sign_in(global_settings.admin_username, global_settings.admin_password)
        with GraphQLClient(auth=admin, global_settings=global_settings) as admin_client:
            UserOperations(client=admin_client).delete_users(user_names=[email])
