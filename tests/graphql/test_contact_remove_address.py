import allure
import pytest
from core.clients import GraphQLClient
from gql.operations import ContactOperations
from gql.types import MemberAddress
from tests.constants import TEST_ADDRESS
from tests.context import Context

from utils.address_utils import addresses_equal

_USERNAME = "acme_store_employee_1@acme.com"


@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
@allure.feature("Contact / Addresses (GraphQL)")
@allure.title("Remove a contact address")
def test_contact_remove_address(ctx: Context, graphql_client: GraphQLClient) -> None:
    contact_ops = ContactOperations(client=graphql_client)
    added_address: MemberAddress | None = None

    assert ctx.contact_id is not None

    try:
        with allure.step(f"Add address to contact {ctx.contact_id}"):
            contact_addresses = contact_ops.update_member_addresses(
                member_id=ctx.contact_id, addresses=[TEST_ADDRESS]
            )
            added_address = next(
                a for a in contact_addresses if addresses_equal(a=a, b=TEST_ADDRESS)
            )
            assert added_address is not None

        with allure.step(f"Remove address {added_address.id} from contact"):
            remaining_addresses = contact_ops.delete_member_addresses(
                member_id=ctx.contact_id, addresses=[added_address]
            )

        with allure.step("Verify the address is no longer in contact addresses"):
            assert not any(a.id == added_address.id for a in remaining_addresses)
    finally:
        if added_address is not None:
            with allure.step(
                f"Teardown: ensure address removed from contact {ctx.contact_id}"
            ):
                contact_ops.delete_member_addresses(
                    member_id=ctx.contact_id, addresses=[added_address]
                )
