import allure
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
@allure.feature("Contact / Search (GraphQL)")
@allure.title("Search organization contacts by full name")
def test_contacts_search_by_name(graphql_client: GraphQLClient, ctx: Context) -> None:
    assert ctx.organization_id is not None

    with allure.step(f"Search organization contacts by name '{_CONTACT_FULL_NAME}'"):
        contacts = ContactOperations(client=graphql_client).get_organization_contacts(
            organization_id=ctx.organization_id,
            search_phrase=_CONTACT_FULL_NAME,
        )

    with allure.step(
        f"Verify all returned contacts include '{_CONTACT_FULL_NAME}' and {_CONTACT_ID} is found"
    ):
        target = next((c for c in contacts if c.id == _CONTACT_ID), None)
        assert target is not None, f"Search did not return {_CONTACT_ID}"
        assert _CONTACT_FULL_NAME in target.full_name


@pytest.mark.graphql
@pytest.mark.with_user(_MAINTAINER)
@allure.feature("Contact / Search (GraphQL)")
@allure.title("Search organization contacts by email")
def test_contacts_search_by_email(graphql_client: GraphQLClient, ctx: Context) -> None:
    assert ctx.organization_id is not None

    with allure.step(f"Search organization contacts by email '{_CONTACT_EMAIL}'"):
        contacts = ContactOperations(client=graphql_client).get_organization_contacts(
            organization_id=ctx.organization_id,
            search_phrase=_CONTACT_EMAIL,
        )

    with allure.step(f"Verify a contact with email '{_CONTACT_EMAIL}' is found"):
        assert len(contacts) > 0
        assert any(
            any(a.user_name == _CONTACT_EMAIL for a in c.security_accounts)
            for c in contacts
        )
        assert any(c.id == _CONTACT_ID for c in contacts)
