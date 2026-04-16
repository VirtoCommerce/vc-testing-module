from gql.types.cart_address import CartAddress
from gql.types.member_address import MemberAddress

TEST_ADDRESS = MemberAddress(
    first_name="John",
    last_name="Doe",
    line1="1 Test Street",
    city="Test City",
    country_code="US",
    country_name="United States of America",
    postal_code="10001",
    region_id="US-NY",
    region_name="New York",
    phone="+1 (555) 000-0000",
    email="john.doe@test.com",
    address_type=0,
)

TEST_CART_ADDRESS = CartAddress.model_validate(TEST_ADDRESS.model_dump())
