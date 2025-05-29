import allure, os
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.operations.contact.contact_operations import ContactOperations
from tests_graphql.test_data.test_user import TEST_PERMANENT_CORPORATE_USER


@allure.title("Filter organization contacts by role (GraphQL)")
def test_filter_organization_contacts_by_role(user_service, graphql_client):
    print(f"{os.linesep}Running test to filter organization contacts by role...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    user_service.sign_in(TEST_PERMANENT_CORPORATE_USER["username"], TEST_PERMANENT_CORPORATE_USER["password"])

    user = user_operations.get_user()

    organization_maintainers = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"], user_id=user["id"], search_phrase="'roleId':'org-maintainer'"
    )

    organization_employees = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"], user_id=user["id"], search_phrase="'roleId':'org-employee'"
    )

    purchase_agents = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase="'roleId':'purchasing-agent'",
    )

    store_administrators = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"], user_id=user["id"], search_phrase="'roleId':'store-admin'"
    )

    store_managers = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"], user_id=user["id"], search_phrase="'roleId':'store-manager'"
    )

    user_service.sign_out()

    assert organization_maintainers["contacts"]["totalCount"] > 0, "Organization maintainers not found"
    assert organization_employees["contacts"]["totalCount"] > 0, "Organization employees not found"
    assert purchase_agents["contacts"]["totalCount"] > 0, "Purchase agents not found"
    assert store_administrators["contacts"]["totalCount"] > 0, "Store administrators not found"
    assert store_managers["contacts"]["totalCount"] > 0, "Store managers not found"


@allure.title("Filter organization contacts by status (GraphQL)")
def test_filter_organization_contacts_by_status(user_service, graphql_client):
    print(f"{os.linesep}Running test to filter organization contacts by status...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    user_service.sign_in(TEST_PERMANENT_CORPORATE_USER["username"], TEST_PERMANENT_CORPORATE_USER["password"])

    user = user_operations.get_user()

    active_contacts = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"], user_id=user["id"], search_phrase="'status':'Approved'"
    )

    invited_contacts = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"], user_id=user["id"], search_phrase="'status':'Invited'"
    )

    blocked_contacts = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"], user_id=user["id"], search_phrase="'status':'Locked'"
    )

    user_service.sign_out()

    assert active_contacts["contacts"]["totalCount"] > 0, "Active contacts not found"
    assert invited_contacts["contacts"]["totalCount"] > 0, "Invited contacts not found"
    assert blocked_contacts["contacts"]["totalCount"] > 0, "Blocked contacts not found"
