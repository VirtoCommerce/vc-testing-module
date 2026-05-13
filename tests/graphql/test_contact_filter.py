import allure
import pytest
from core.clients import GraphQLClient
from gql.operations import ContactOperations
from tests.context import Context

_MAINTAINER = "acme_store_maintainer_1@acme.com"

_ROLE_MAINTAINER = "org-maintainer"
_ROLE_EMPLOYEE = "org-employee"
_ROLE_PURCHASING_AGENT = "purchasing-agent"
_ROLE_STORE_ADMIN = "store-admin"
_ROLE_STORE_MANAGER = "store-manager"

_STATUS_APPROVED = "Approved"
_STATUS_INVITED = "Invited"
_STATUS_LOCKED = "Locked"


@pytest.mark.graphql
@pytest.mark.with_user(_MAINTAINER)
@pytest.mark.flaky(retries=2, delay=3)
@pytest.mark.parametrize(
    "role_id",
    [
        _ROLE_MAINTAINER,
        _ROLE_EMPLOYEE,
        _ROLE_PURCHASING_AGENT,
        _ROLE_STORE_ADMIN,
        _ROLE_STORE_MANAGER,
    ],
)
@allure.feature("Contact / Search (GraphQL)")
@allure.title("Filter organization contacts by role")
@pytest.mark.flaky(retries=2, delay=3)
def test_contacts_filter_by_role(graphql_client: GraphQLClient, ctx: Context, role_id: str) -> None:
    assert ctx.organization_id is not None

    with allure.step(f"Search organization contacts by role '{role_id}'"):
        contacts = ContactOperations(client=graphql_client).get_organization_contacts(
            organization_id=ctx.organization_id,
            search_phrase=f"'roleId':'{role_id}'",
        )

    with allure.step(f"Verify all returned contacts have role '{role_id}'"):
        assert len(contacts) > 0
        assert all(
            any(role.id == role_id for account in c.security_accounts for role in account.roles) for c in contacts
        )


@pytest.mark.graphql
@pytest.mark.with_user(_MAINTAINER)
@pytest.mark.flaky(retries=2, delay=3)
@pytest.mark.parametrize(
    "status",
    [
        _STATUS_APPROVED,
        _STATUS_INVITED,
        _STATUS_LOCKED,
    ],
)
@allure.feature("Contact / Search (GraphQL)")
@allure.title("Filter organization contacts by status")
@pytest.mark.flaky(retries=2, delay=3)
def test_contacts_filter_by_status(graphql_client: GraphQLClient, ctx: Context, status: str) -> None:
    assert ctx.organization_id is not None

    with allure.step(f"Search organization contacts by status '{status}'"):
        contacts = ContactOperations(client=graphql_client).get_organization_contacts(
            organization_id=ctx.organization_id,
            search_phrase=f"'status':'{status}'",
        )

    with allure.step(f"Verify all returned contacts have status '{status}'"):
        assert len(contacts) > 0
        assert all(c.status == status for c in contacts)
