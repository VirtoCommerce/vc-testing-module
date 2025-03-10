from gql import gql

GET_FULL_CART = gql(
    """
query GetFullCart($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String) {
  cart(
    storeId: $storeId
    userId: $userId
    currencyCode: $currencyCode
    cultureName: $cultureName
  ) {
    ...fullCart
    __typename
  }
}

fragment currency on CurrencyType {
  code
  symbol
  __typename
}

fragment money on MoneyType {
  amount
  formattedAmount
  formattedAmountWithoutCurrency
  currency {
    ...currency
    __typename
  }
  __typename
}

fragment cartId on CartType {
  id
  __typename
}

fragment shortLineItem on LineItemType {
  id
  sku
  quantity
  productId
  extendedPrice {
    ...money
    __typename
  }
  __typename
}

fragment validationError on ValidationErrorType {
  errorCode
  errorMessage
  errorParameters {
    key
    value
    __typename
  }
  objectId
  objectType
  __typename
}

fragment shortCart on CartType {
  ...cartId
  itemsQuantity
  items {
    ...shortLineItem
    __typename
  }
  validationErrors(ruleSet: "*") {
    ...validationError
    __typename
  }
  warnings {
    ...validationError
    __typename
  }
  __typename
}

fragment gift on GiftItemType {
  id
  imageUrl
  name
  lineItemId
  quantity
  __typename
}

fragment shippingMethod on ShippingMethodType {
  id
  code
  logoUrl
  optionName
  optionDescription
  price {
    ...money
    __typename
  }
  vendorId
  name
  __typename
}

fragment paymentMethod on PaymentMethodType {
  code
  name
  description
  logoUrl
  paymentMethodGroupType
  __typename
}

fragment property on Property {
  name
  value
  propertyType
  hidden
  propertyValueType
  label
  displayOrder
  __typename
}

fragment availabilityData on AvailabilityData {
  isActive
  isAvailable
  isBuyable
  isInStock
  availableQuantity
  isEstimated
  restrictedRegions
  warnings
  __typename
}

fragment fullLineItemProduct on Product {
  id
  slug
  minQuantity
  maxQuantity
  masterVariation {
    id
    slug
    __typename
  }
  properties {
    ...property
    __typename
  }
  keyProperties {
    ...property
    __typename
  }
  availabilityData {
    ...availabilityData
    __typename
  }
  isConfigurable
  unitsPerPack
  __typename
}

fragment commonVendor on CommonVendor {
  id
  name
  rating {
    value
    reviewCount
    __typename
  }
  supplier {
    paymentMethods
    contractNumber
    isOrderAllowed
    isOrderSetupRequestRequired
    isRequestSetupAccountBillingAllowed
    outerId
    logo
    isPONumberMandatory
    pONumberMandatoryThreshold
    __typename
  }
  isNotAvailable
  __typename
}

fragment fullLineItem on LineItemType {
  ...shortLineItem
  name
  inStockQuantity
  imageUrl
  selectedForCheckout
  productType
  showPlacedPrice
  listTotal {
    ...money
    __typename
  }
  product {
    ...fullLineItemProduct
    __typename
  }
  vendor {
    ...commonVendor
    __typename
  }
  placedPrice {
    ...money
    __typename
  }
  listPrice {
    ...money
    __typename
  }
  salePrice {
    ...money
    __typename
  }
  discountTotal {
    ...money
    __typename
  }
  validationErrors {
    ...validationError
    __typename
  }
  configurationItems {
    id
    name
    __typename
  }
  __typename
}

fragment coupon on CouponType {
  code
  isAppliedSuccessfully
  __typename
}

fragment discount on DiscountType {
  description
  amount
  coupon
  __typename
}

fragment cartAddress on CartAddressType {
  id
  name
  organization
  firstName
  lastName
  line1
  line2
  city
  countryCode
  countryName
  regionId
  regionName
  postalCode
  phone
  email
  addressType
  description
  outerId
  parentId
  __typename
}

fragment shipment on ShipmentType {
  id
  shipmentMethodCode
  shipmentMethodOption
  deliveryAddress {
    ...cartAddress
    __typename
  }
  price {
    ...money
    __typename
  }
  discountAmount {
    ...money
    __typename
  }
  comment
  vendor {
    id
    __typename
  }
  fee {
    ...money
    __typename
  }
  feeWithTax {
    ...money
    __typename
  }
  contactPhoneNumber
  __typename
}

fragment payment on PaymentType {
  id
  paymentGatewayCode
  billingAddress {
    ...cartAddress
    __typename
  }
  vendor {
    id
    __typename
  }
  amount {
    amount
    __typename
  }
  comment
  requestSetupAccountBillingMethod
  generalLedgerNumber
  purchaseOrderNumber
  requisitionNumber
  dynamicProperties {
    name
    __typename
  }
  __typename
}

fragment vendorCart on CartVendorType {
  vendor {
    id
    supplier {
      paymentMethods
      isOrderAllowed
      isOrderSetupRequestRequired
      isRequestSetupAccountBillingAllowed
      outerId
      isPONumberMandatory
      pONumberMandatoryThreshold
      __typename
    }
    __typename
  }
  subTotal {
    ...money
    __typename
  }
  shippingTotal {
    ...money
    __typename
  }
  taxTotal {
    ...money
    __typename
  }
  shippingPrice {
    ...money
    __typename
  }
  fee {
    ...money
    __typename
  }
  feeTotal {
    ...money
    __typename
  }
  feeTotalWithTax {
    ...money
    __typename
  }
  feeWithTax {
    ...money
    __typename
  }
  total {
    ...money
    __typename
  }
  contractNumbers
  __typename
}

fragment fullCart on CartType {
  ...shortCart
  purchaseOrderNumber
  comment
  availableGifts {
    ...gift
    __typename
  }
  availableShippingMethods {
    ...shippingMethod
    __typename
  }
  availablePaymentMethods {
    ...paymentMethod
    __typename
  }
  items {
    ...fullLineItem
    __typename
  }
  gifts {
    ...gift
    __typename
  }
  coupons {
    ...coupon
    __typename
  }
  discounts {
    ...discount
    __typename
  }
  shipments {
    ...shipment
    __typename
  }
  payments {
    ...payment
    __typename
  }
  currency {
    ...currency
    __typename
  }
  total {
    ...money
    __typename
  }
  discountTotal {
    ...money
    __typename
  }
  subTotal {
    ...money
    __typename
  }
  shippingPrice {
    ...money
    __typename
  }
  shippingTotal {
    ...money
    __typename
  }
  taxTotal {
    ...money
    __typename
  }
  vendors {
    ...vendorCart
    __typename
  }
  approvalFlowType
  fee {
    ...money
    __typename
  }
  feeTotal {
    ...money
    __typename
  }
  feeWithTax {
    ...money
    __typename
  }
  feeTotalWithTax {
    ...money
    __typename
  }
  approvalFlowType
  __typename
}
"""
)
