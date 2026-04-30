import pytest
from core.clients import GraphQLClient
from gql.operations import ContactOperations
from tests.context import Context

_MAINTAINER = "acme_store_maintainer_1@acme.com"
_CONTACT_ID = "contact-acme-store-employee-1"
_CONTACT_FULL_NAME = "ACME Employee A"
_CONTACT_EMAIL = "acme_store_employee_1@acme.com"


@pytest.mark.graphql
@pytest.mark.with_user(_MAINTAINER)
def test_contacts_search_by_name(graphql_client: GraphQLClient, ctx: Context) -> None:
    assert ctx.organization_id is not None
    contacts = ContactOperations(client=graphql_client).get_organization_contacts(
        organization_id=ctx.organization_id,
        search_phrase=_CONTACT_FULL_NAME,
    )

    assert len(contacts) > 0
    assert all(_CONTACT_FULL_NAME in c.full_name for c in contacts)
    assert any(c.id == _CONTACT_ID for c in contacts)


@pytest.mark.graphql
@pytest.mark.with_user(_MAINTAINER)
def test_contacts_search_by_email(graphql_client: GraphQLClient, ctx: Context) -> None:
    assert ctx.organization_id is not None
    contacts = ContactOperations(client=graphql_client).get_organization_contacts(
        organization_id=ctx.organization_id,
        search_phrase=_CONTACT_EMAIL,
    )

    assert len(contacts) > 0
    assert any(any(a.user_name == _CONTACT_EMAIL for a in c.security_accounts) for c in contacts)
    assert any(c.id == _CONTACT_ID for c in contacts)
