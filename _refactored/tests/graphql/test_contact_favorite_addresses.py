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
def test_contact_favorite_addresses(
    ctx: Context, graphql_client: GraphQLClient
) -> None:
    contact_ops = ContactOperations(client=graphql_client)
    address: MemberAddress | None = None

    assert ctx.contact_id is not None

    try:
        contact_addresses = contact_ops.update_member_addresses(
            member_id=ctx.contact_id, addresses=[TEST_ADDRESS]
        )
        address = next(
            a for a in contact_addresses if addresses_equal(a=a, b=TEST_ADDRESS)
        )
        assert address is not None
        assert address.id is not None

        result = contact_ops.add_address_to_favorites(address_id=address.id)
        assert result == True

        contact_addresses = contact_ops.get_contact_addresses(contact_id=ctx.contact_id)
        address = next(
            a for a in contact_addresses if addresses_equal(a=a, b=TEST_ADDRESS)
        )
        assert address is not None
        assert address.id is not None
        assert address.is_favorite is True

        result = contact_ops.remove_address_from_favorites(address_id=address.id)
        assert result == True

        contact_addresses = contact_ops.get_contact_addresses(contact_id=ctx.contact_id)
        address = next(
            a for a in contact_addresses if addresses_equal(a=a, b=TEST_ADDRESS)
        )
        assert address is not None
        assert address.id is not None
        assert address.is_favorite is False
    finally:
        if address is not None:
            contact_ops.delete_member_addresses(
                member_id=ctx.contact_id, addresses=[address]
            )
