import allure, os
from tests_graphql.operations.user.user_operations import UserOperations
from tests_graphql.operations.contact.contact_operations import ContactOperations
from tests_graphql.test_data.test_user import TEST_PERMANENT_CORPORATE_USER


@allure.feature("Change organization contact role (GraphQL)")
def test_change_organization_contact_role(user_service, graphql_client):
    print(f"{os.linesep}Running test to change organization contact role...", end=" ")

    user_operations = UserOperations(graphql_client)
    contact_operations = ContactOperations(graphql_client)

    user_service.sign_in(TEST_PERMANENT_CORPORATE_USER["username"], TEST_PERMANENT_CORPORATE_USER["password"])

    user = user_operations.get_user()

    organization_contact_to_change_role = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase="e2e-test-corporate-1@test.com",
    )["contacts"]["items"][0]

    result = contact_operations.change_organization_contact_role(
        payload={
            "roleIds": ["org-employee"],
            "userId": organization_contact_to_change_role["securityAccounts"][0]["id"],
        }
    )

    changed_contact = contact_operations.fetch_organization_contacts(
        organization_id=user["contact"]["organizationId"],
        user_id=user["id"],
        search_phrase="e2e-test-corporate-1@test.com",
    )["contacts"]["items"][0]

    # Test teardown
    contact_operations.change_organization_contact_role(
        payload={
            "roleIds": ["purchasing-agent"],
            "userId": organization_contact_to_change_role["securityAccounts"][0]["id"],
        }
    )

    user_service.sign_out()

    assert result["succeeded"] == True, "Contact role was not changed"
    assert changed_contact["securityAccounts"][0]["roles"][0]["id"] == "org-employee", "Contact role was not changed"
