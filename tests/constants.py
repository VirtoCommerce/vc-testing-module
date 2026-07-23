from gql.types.cart_address import CartAddress
from gql.types.member_address import MemberAddress

TEST_ADDRESS = MemberAddress(
    first_name="John",
    last_name="Doe",
    line1="1 Test Street",
    city="Test City",
    country_code="USA",
    country_name="United States of America",
    postal_code="10001",
    region_id="NY",
    region_name="New York",
    phone="+1 (555) 000-0000",
    email="john.doe@test.com",
    address_type=3,
)

TEST_CART_ADDRESS = CartAddress.model_validate(TEST_ADDRESS.model_dump())

# --- Coupon / promotion test data (seeded via dataset) ---
# SALE-001: list $29.99 / sale $19.99, used to prove percentage discounts are
# computed on the sale price base. The USD list/sale prices let E2E tests detect
# whether the storefront build actually applies the sale price before asserting
# sale-basis math (skip if the build ignores the sale price).
SALE_PRODUCT_ID = "sale-001"
SALE_PRODUCT_LIST_PRICE = "29.99"
SALE_PRODUCT_SALE_PRICE = "19.99"

# QA10OFF: 10%-of-subtotal cart coupon (RewardCartGetOfRelSubtotal, amount 10).
PERCENTAGE_COUPON_CODE = "QA10OFF"
PERCENTAGE_PCT = 10

# WELCOME20: $20 absolute-off cart coupon (RewardCartGetOfAbsSubtotal, amount 20).
FIXED_COUPON_CODE = "WELCOME20"
FIXED_COUPON_AMOUNT = 20

# Stored lowercase; guards coupon-code case fidelity (VCST-5233).
LOWERCASE_COUPON_CODE = "agenttestlc062"

# Coupon whose expiration date is in the past.
EXPIRED_COUPON_CODE = "QAEXPIRED"

# QAMINSUB100K: attached to a coupon-gated promotion whose $100,000 min-subtotal
# condition is unreachable for a normal cart. Proves an unmet condition leaves
# the coupon recorded but not applied (no discount). The promotion is non-public
# so it never surfaces in promotionCoupons / preset assertions.
MIN_SUBTOTAL_COUPON_CODE = "QAMINSUB100K"
