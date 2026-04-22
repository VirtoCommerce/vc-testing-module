import pytest
from core.clients import GraphQLClient
from gql.operations import ContactOperations
from gql.types import MemberAddress
from tests.constants import TEST_ADDRESS
from tests.context import Context

from utils.address_utils import addresses_equal

_UPDATED_CITY = "Updated City"
_UPDATED_LINE1 = "2 Updated Street"

_USERNAME = "acme_store_employee_1@acme.com"


@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
def test_contact_add_personal_address(
    ctx: Context, graphql_client: GraphQLClient
) -> None:
    contact_ops = ContactOperations(client=graphql_client)
    added_address: MemberAddress | None = None

    assert ctx.contact_id is not None

    try:
        contact_addresses = contact_ops.update_member_addresses(
            member_id=ctx.contact_id, addresses=[TEST_ADDRESS]
        )
        added_address = next(
            a for a in contact_addresses if addresses_equal(a=a, b=TEST_ADDRESS)
        )

        assert added_address is not None
    finally:
        if added_address is not None:
            contact_ops.delete_member_addresses(
                member_id=ctx.contact_id, addresses=[added_address]
            )


@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
def test_contact_update_organization_address(
    ctx: Context, graphql_client: GraphQLClient
) -> None:
    contact_ops = ContactOperations(client=graphql_client)
    added_address: MemberAddress | None = None

    assert ctx.organization_id is not None

    try:
        addresses = contact_ops.update_member_addresses(
            member_id=ctx.organization_id, addresses=[TEST_ADDRESS]
        )
        added_address = next(
            a for a in addresses if addresses_equal(a=a, b=TEST_ADDRESS)
        )

        updated = added_address.model_copy(
            update={"city": _UPDATED_CITY, "line1": _UPDATED_LINE1}
        )
        addresses = contact_ops.update_member_addresses(
            member_id=ctx.organization_id, addresses=[updated]
        )
        result_address = next(
            (a for a in addresses if a.key == added_address.key), None
        )

        assert result_address is not None
        assert result_address.city == _UPDATED_CITY
        assert result_address.line1 == _UPDATED_LINE1
    finally:
        if added_address is not None:
            contact_ops.delete_member_addresses(
                member_id=ctx.organization_id, addresses=[added_address]
            )


@pytest.mark.graphql
@pytest.mark.with_user(_USERNAME)
def test_contact_add_organization_address(
    ctx: Context, graphql_client: GraphQLClient
) -> None:
    contact_ops = ContactOperations(client=graphql_client)
    added_address: MemberAddress | None = None

    assert ctx.organization_id is not None

    try:
        contact_addresses = contact_ops.update_member_addresses(
            member_id=ctx.organization_id, addresses=[TEST_ADDRESS]
        )
        added_address = next(
            a for a in contact_addresses if addresses_equal(a=a, b=TEST_ADDRESS)
        )

        assert added_address is not None
    finally:
        if added_address is not None:
            contact_ops.delete_member_addresses(
                member_id=ctx.organization_id, addresses=[added_address]
            )
