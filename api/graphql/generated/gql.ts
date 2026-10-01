/* eslint-disable */
import * as types from "./graphql";

/**
 * Map of all GraphQL operations in the project.
 *
 * This map has several performance disadvantages:
 * 1. It is not tree-shakeable, so it will include all operations in the project.
 * 2. It is not minifiable, so the string of a GraphQL query will be multiple times inside the bundle.
 * 3. It does not support dead code elimination, so it will add unused operations.
 *
 * Therefore it is highly recommended to use the babel or swc plugin for production.
 * Learn more about it here: https://the-guild.dev/graphql/codegen/plugins/presets/preset-client#reducing-bundle-size
 */
type Documents = {
  "fragment CartAddress on CartAddressType {\n  id\n  key\n  city\n  countryCode\n  countryName\n  email\n  firstName\n  middleName\n  lastName\n  line1\n  line2\n  name\n  organization\n  phone\n  postalCode\n  regionId\n  regionName\n  zip\n  outerId\n  description\n  addressType\n}": typeof types.CartAddressFragmentDoc;
  "fragment CartConfigurationItem on CartConfigurationItemType {\n  id\n  sectionId\n  type\n  productId\n  name\n  sku\n  imageUrl\n  quantity\n  customText\n  selectedForCheckout\n}": typeof types.CartConfigurationItemFragmentDoc;
  "fragment CartWithList on CartWithListType {\n  cart {\n    ...Cart\n  }\n  list {\n    ...Cart\n  }\n}": typeof types.CartWithListFragmentDoc;
  "fragment Cart on CartType {\n  id\n  storeId\n  isAnonymous\n  hasPhysicalProducts\n  customerId\n  itemsCount\n  itemsQuantity\n  total {\n    ...Money\n  }\n  subTotal {\n    ...Money\n  }\n  subTotalDiscount {\n    ...Money\n  }\n  shippingTotal {\n    ...Money\n  }\n  items {\n    ...LineItem\n  }\n  payments {\n    ...Payment\n  }\n  shipments {\n    ...Shipment\n  }\n  coupons {\n    ...Coupon\n  }\n  gifts {\n    ...GiftItem\n  }\n  addresses {\n    ...CartAddress\n  }\n  validationErrors {\n    errorCode\n    errorMessage\n    errorParameters {\n      key\n      value\n    }\n    objectType\n    objectId\n  }\n}": typeof types.CartFragmentDoc;
  "fragment Category on Category {\n  id\n  code\n  name\n  outline\n  slug\n}": typeof types.CategoryFragmentDoc;
  "fragment ConfigurationLineItem on ConfigurationLineItemType {\n  id\n  text\n  quantity\n  product {\n    ...Product\n  }\n  listPrice {\n    ...Money\n  }\n  salePrice {\n    ...Money\n  }\n  extendedPrice {\n    ...Money\n  }\n  discountAmount {\n    ...Money\n  }\n}": typeof types.ConfigurationLineItemFragmentDoc;
  "fragment Contact on ContactType {\n  id\n  firstName\n  lastName\n  fullName\n  status\n  organizationId\n  organizationsIds\n  securityAccounts {\n    ...User\n  }\n}": typeof types.ContactFragmentDoc;
  "fragment Coupon on CouponType {\n  code\n  isAppliedSuccessfully\n}": typeof types.CouponFragmentDoc;
  "fragment Currency on CurrencyType {\n  code\n}": typeof types.CurrencyFragmentDoc;
  "fragment CustomIdentityResult on CustomIdentityResultType {\n  succeeded\n  errors {\n    code\n    parameter\n    description\n  }\n}": typeof types.CustomIdentityResultFragmentDoc;
  "fragment GiftItem on GiftItemType {\n  id\n  quantity\n  productId\n  name\n  lineItemId\n}": typeof types.GiftItemFragmentDoc;
  "fragment IdentityResult on IdentityResultType {\n  succeeded\n  errors {\n    code\n    description\n  }\n}": typeof types.IdentityResultFragmentDoc;
  "fragment Language on LanguageType {\n  cultureName\n  nativeName\n}": typeof types.LanguageFragmentDoc;
  "fragment LineItem on LineItemType {\n  id\n  sku\n  productId\n  name\n  quantity\n  listPrice {\n    ...Money\n  }\n  salePrice {\n    ...Money\n  }\n  placedPrice {\n    ...Money\n  }\n  extendedPrice {\n    ...Money\n  }\n  discountAmount {\n    ...Money\n  }\n  selectedForCheckout\n  isValid\n  validationErrors {\n    errorCode\n    errorMessage\n    errorParameters {\n      key\n      value\n    }\n    objectType\n    objectId\n  }\n  configurationItems {\n    ...CartConfigurationItem\n  }\n}": typeof types.LineItemFragmentDoc;
  "fragment MemberAddress on MemberAddressType {\n  id\n  key\n  isDefault\n  isFavorite\n  city\n  countryCode\n  countryName\n  email\n  firstName\n  middleName\n  lastName\n  line1\n  line2\n  name\n  organization\n  phone\n  postalCode\n  regionId\n  regionName\n  zip\n  outerId\n  description\n  addressType\n}": typeof types.MemberAddressFragmentDoc;
  "fragment MenuLink on MenuLinkType {\n  title\n  url\n  priority\n}": typeof types.MenuLinkFragmentDoc;
  "fragment Money on MoneyType {\n  amount\n  formattedAmount\n}": typeof types.MoneyFragmentDoc;
  "fragment OrderLineItem on OrderLineItemType {\n  id\n  name\n  sku\n  productId\n  quantity\n  price {\n    ...Money\n  }\n  extendedPrice {\n    ...Money\n  }\n}": typeof types.OrderLineItemFragmentDoc;
  "fragment OrderPayment on PaymentInType {\n  id\n  number\n  gatewayCode\n  status\n  sum {\n    ...Money\n  }\n}": typeof types.OrderPaymentFragmentDoc;
  "fragment OrderShipment on OrderShipmentType {\n  id\n  number\n  shipmentMethodCode\n  shipmentMethodOption\n  status\n  total {\n    ...Money\n  }\n}": typeof types.OrderShipmentFragmentDoc;
  "fragment Order on CustomerOrderType {\n  id\n  number\n  status\n  createdDate\n  total {\n    ...Money\n  }\n  items {\n    ...OrderLineItem\n  }\n  inPayments {\n    ...OrderPayment\n  }\n  shipments {\n    ...OrderShipment\n  }\n}": typeof types.OrderFragmentDoc;
  "fragment PageContext on PageContextResponseType {\n  slugInfo {\n    ...SlugInfo\n  }\n  store {\n    ...StoreInfo\n  }\n  whiteLabelingSettings {\n    ...WhiteLabelingSettings\n  }\n  user {\n    ...User\n  }\n}": typeof types.PageContextFragmentDoc;
  "fragment Payment on PaymentType {\n  id\n  outerId\n  paymentGatewayCode\n  currency {\n    ...Currency\n  }\n  total {\n    ...Money\n  }\n  billingAddress {\n    ...CartAddress\n  }\n}": typeof types.PaymentFragmentDoc;
  "fragment PickupAddress on PickupAddressType {\n  id\n  key\n  name\n  organization\n  countryCode\n  countryName\n  city\n  postalCode\n  line1\n  line2\n  regionId\n  regionName\n  phone\n  email\n  outerId\n  description\n  addressType\n}": typeof types.PickupAddressFragmentDoc;
  "fragment PickupLocationAddress on PickupLocationAddressType {\n  id\n  key\n  name\n  organization\n  countryCode\n  countryName\n  city\n  postalCode\n  line1\n  line2\n  regionId\n  regionName\n  phone\n  email\n  outerId\n  description\n  addressType\n}": typeof types.PickupLocationAddressFragmentDoc;
  "fragment PickupLocation on PickupLocationType {\n  id\n  isActive\n  name\n  description\n  contactEmail\n  contactPhone\n  workingHours\n  geoLocation\n  address {\n    ...PickupAddress\n  }\n}": typeof types.PickupLocationFragmentDoc;
  "fragment ProductConfiguration on ConfigurationQueryResponseType {\n  configurationSections {\n    id\n    name\n    description\n    isRequired\n    type\n    allowCustomText\n    allowTextOptions\n    maxLength\n    options {\n      ...ConfigurationLineItem\n    }\n  }\n}": typeof types.ProductConfigurationFragmentDoc;
  "fragment ProductPickupLocation on ProductPickupLocation {\n  id\n  isActive\n  name\n  description\n  contactEmail\n  contactPhone\n  workingHours\n  deliveryDays\n  storageDays\n  geoLocation\n  address {\n    ...PickupLocationAddress\n  }\n  availabilityType\n  availabilityNote\n  availableQuantity\n}": typeof types.ProductPickupLocationFragmentDoc;
  "fragment ProductPrice on PriceType {\n  list {\n    ...Money\n  }\n  actual {\n    ...Money\n  }\n}": typeof types.ProductPriceFragmentDoc;
  "fragment Product on Product {\n  id\n  code\n  productType\n  isConfigurable\n  name\n  vendor {\n    ...Vendor\n  }\n  price {\n    ...ProductPrice\n  }\n}": typeof types.ProductFragmentDoc;
  "fragment QuoteAddress on QuoteAddressType {\n  addressType\n  city\n  countryCode\n  countryName\n  line1\n  postalCode\n  regionId\n  regionName\n}": typeof types.QuoteAddressFragmentDoc;
  "fragment QuoteItem on QuoteItemType {\n  id\n  name\n  sku\n  productId\n  quantity\n  listPrice {\n    ...Money\n  }\n  salePrice {\n    ...Money\n  }\n  proposalPrices {\n    quantity\n    price {\n      ...Money\n    }\n  }\n}": typeof types.QuoteItemFragmentDoc;
  "fragment QuoteTotals on QuoteTotalsType {\n  originalSubTotalExlTax {\n    ...Money\n  }\n  subTotalExlTax {\n    ...Money\n  }\n  shippingTotal {\n    ...Money\n  }\n  discountTotal {\n    ...Money\n  }\n  taxTotal {\n    ...Money\n  }\n  grandTotalExlTax {\n    ...Money\n  }\n  grandTotalInclTax {\n    ...Money\n  }\n}": typeof types.QuoteTotalsFragmentDoc;
  "fragment Quote on QuoteType {\n  id\n  number\n  status\n  storeId\n  customerId\n  comment\n  isAnonymous\n  isCancelled\n  totals {\n    ...QuoteTotals\n  }\n  items {\n    ...QuoteItem\n  }\n}": typeof types.QuoteFragmentDoc;
  "fragment Role on RoleType {\n  id\n  name\n  normalizedName\n}": typeof types.RoleFragmentDoc;
  "fragment SeoInfo on SeoInfo {\n  id\n  name\n  semanticUrl\n  outline\n  pageTitle\n  metaDescription\n  imageAltDescription\n  metaKeywords\n  storeId\n  objectId\n  objectType\n  isActive\n  languageCode\n}": typeof types.SeoInfoFragmentDoc;
  "fragment Shipment on ShipmentType {\n  id\n  shipmentMethodCode\n  shipmentMethodOption\n  fulfillmentCenterId\n  price {\n    ...Money\n  }\n  currency {\n    ...Currency\n  }\n  deliveryAddress {\n    ...CartAddress\n  }\n}": typeof types.ShipmentFragmentDoc;
  "fragment ShoppingList on WishlistType {\n  id\n  name\n  storeId\n  customerId\n  customerName\n  items {\n    ...WishlistLineItem\n  }\n  itemsCount\n  description\n  subTotal {\n    ...Money\n  }\n  sharingSetting {\n    id\n    scope\n  }\n}": typeof types.ShoppingListFragmentDoc;
  "fragment SlugInfo on SlugInfoResponseType {\n  entityInfo {\n    ...SeoInfo\n  }\n  redirectUrl\n}": typeof types.SlugInfoFragmentDoc;
  "fragment StoreInfo on StoreResponseType {\n  storeId\n  storeName\n  catalogId\n  storeUrl\n  defaultLanguage {\n    ...Language\n  }\n  availableLanguages {\n    ...Language\n  }\n  defaultCurrency {\n    ...Currency\n  }\n  availableCurrencies {\n    ...Currency\n  }\n  settings {\n    ...StoreSettings\n  }\n}": typeof types.StoreInfoFragmentDoc;
  "fragment StoreSettings on StoreSettingsType {\n  anonymousUsersAllowed\n  taxCalculationEnabled\n  seoLinkType\n}": typeof types.StoreSettingsFragmentDoc;
  "fragment User on UserType {\n  id\n  userName\n  email\n  emailConfirmed\n  isAdministrator\n  memberId\n  storeId\n  roles {\n    ...Role\n  }\n}": typeof types.UserFragmentDoc;
  "fragment Vendor on CommonVendor {\n  id\n  name\n}": typeof types.VendorFragmentDoc;
  "fragment WhiteLabelingSettings on WhiteLabelingSettingsType {\n  logoUrl\n  secondaryLogoUrl\n  faviconUrl\n  themePresetName\n  footerLinks {\n    ...MenuLink\n  }\n  mainMenuLinks {\n    ...MenuLink\n  }\n}": typeof types.WhiteLabelingSettingsFragmentDoc;
  "fragment WishlistLineItem on LineItemType {\n  id\n  sku\n  productId\n  name\n  quantity\n}": typeof types.WishlistLineItemFragmentDoc;
  "mutation AddBulkItemsCart($command: InputAddBulkItemsType!) {\n  addBulkItemsCart(command: $command) {\n    cart {\n      ...Cart\n    }\n    errors {\n      errorCode\n      errorMessage\n      objectId\n    }\n  }\n}": typeof types.AddBulkItemsCartDocument;
  "mutation AddCoupon($command: InputAddCouponType!) {\n  addCoupon(command: $command) {\n    ...Cart\n  }\n}": typeof types.AddCouponDocument;
  "mutation AddItem($command: InputAddItemType!) {\n  addItem(command: $command) {\n    ...Cart\n  }\n}": typeof types.AddItemDocument;
  "mutation AddItemsCart($command: InputAddItemsType!) {\n  addItemsCart(command: $command) {\n    ...Cart\n  }\n}": typeof types.AddItemsCartDocument;
  "mutation AddOrUpdateCartPayment($command: InputAddOrUpdateCartPaymentType!) {\n  addOrUpdateCartPayment(command: $command) {\n    ...Cart\n  }\n}": typeof types.AddOrUpdateCartPaymentDocument;
  "mutation AddOrUpdateCartShipment($command: InputAddOrUpdateCartShipmentType!) {\n  addOrUpdateCartShipment(command: $command) {\n    ...Cart\n  }\n}": typeof types.AddOrUpdateCartShipmentDocument;
  "mutation ChangeCartConfiguredItem($command: InputChangeCartConfiguredItemType!) {\n  changeCartConfiguredItem(command: $command) {\n    ...Cart\n  }\n}": typeof types.ChangeCartConfiguredItemDocument;
  "mutation ClearCart($command: InputClearCartType!) {\n  clearCart(command: $command) {\n    ...Cart\n  }\n}": typeof types.ClearCartDocument;
  "mutation CreateOrderFromCart($command: InputCreateOrderFromCartType!) {\n  createOrderFromCart(command: $command) {\n    ...Order\n  }\n}": typeof types.CreateOrderFromCartDocument;
  "query GetCartLineValidation($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String!, $cartId: String) {\n  cart(\n    storeId: $storeId\n    userId: $userId\n    currencyCode: $currencyCode\n    cultureName: $cultureName\n    cartId: $cartId\n  ) {\n    itemsCount\n    items {\n      id\n      sku\n      productId\n      quantity\n      isValid\n      validationErrors {\n        errorCode\n        objectType\n        objectId\n        errorMessage\n      }\n    }\n  }\n}": typeof types.GetCartLineValidationDocument;
  "query GetCartValidationAliased($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String!, $ruleSetA: String, $ruleSetB: String, $cartId: String) {\n  cart(\n    storeId: $storeId\n    userId: $userId\n    currencyCode: $currencyCode\n    cultureName: $cultureName\n    cartId: $cartId\n  ) {\n    itemsCount\n    errorsA: validationErrors(ruleSet: $ruleSetA) {\n      errorCode\n      objectType\n      objectId\n      errorMessage\n    }\n    errorsB: validationErrors(ruleSet: $ruleSetB) {\n      errorCode\n      objectType\n      objectId\n      errorMessage\n    }\n  }\n}": typeof types.GetCartValidationAliasedDocument;
  "query GetCartValidation($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String!, $ruleSet: String, $cartId: String) {\n  cart(\n    storeId: $storeId\n    userId: $userId\n    currencyCode: $currencyCode\n    cultureName: $cultureName\n    cartId: $cartId\n  ) {\n    itemsCount\n    validationErrors(ruleSet: $ruleSet) {\n      errorCode\n      objectType\n      objectId\n      errorMessage\n    }\n    items {\n      id\n      sku\n      productId\n      quantity\n      isValid\n      validationErrors {\n        errorCode\n        objectType\n        objectId\n        errorMessage\n      }\n    }\n  }\n}": typeof types.GetCartValidationDocument;
  "query GetCart($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String!, $cartId: String, $cartName: String) {\n  cart(\n    storeId: $storeId\n    userId: $userId\n    currencyCode: $currencyCode\n    cultureName: $cultureName\n    cartId: $cartId\n    cartName: $cartName\n  ) {\n    ...Cart\n  }\n}": typeof types.GetCartDocument;
  "mutation MergeCart($command: InputMergeCartType!) {\n  mergeCart(command: $command) {\n    ...Cart\n  }\n}": typeof types.MergeCartDocument;
  "mutation RemoveCartItem($command: InputRemoveItemType!) {\n  removeCartItem(command: $command) {\n    ...Cart\n  }\n}": typeof types.RemoveCartItemDocument;
  "mutation RemoveCart($command: InputRemoveCartType!) {\n  removeCart(command: $command)\n}": typeof types.RemoveCartDocument;
  "mutation RemoveCoupon($command: InputRemoveCouponType!) {\n  removeCoupon(command: $command) {\n    ...Cart\n  }\n}": typeof types.RemoveCouponDocument;
  "mutation SelectCartItems($command: InputChangeCartItemsSelectedType!) {\n  selectCartItems(command: $command) {\n    ...Cart\n  }\n}": typeof types.SelectCartItemsDocument;
  "mutation UnSelectAllCartItems($command: InputChangeAllCartItemsSelectedType!) {\n  unSelectAllCartItems(command: $command) {\n    ...Cart\n  }\n}": typeof types.UnSelectAllCartItemsDocument;
  "mutation UnSelectCartItems($command: InputChangeCartItemsSelectedType!) {\n  unSelectCartItems(command: $command) {\n    ...Cart\n  }\n}": typeof types.UnSelectCartItemsDocument;
  "mutation UpdateCartQuantity($command: InputUpdateCartQuantity!) {\n  updateCartQuantity(command: $command) {\n    ...Cart\n  }\n}": typeof types.UpdateCartQuantityDocument;
  "query Categories($storeId: String!, $userId: String, $cultureName: String, $currencyCode: String, $filter: String, $first: Int) {\n  categories(\n    storeId: $storeId\n    userId: $userId\n    cultureName: $cultureName\n    currencyCode: $currencyCode\n    filter: $filter\n    first: $first\n  ) {\n    totalCount\n    items {\n      ...Category\n    }\n  }\n}": typeof types.CategoriesDocument;
  "query Category($id: String!, $storeId: String!, $userId: String, $cultureName: String, $currencyCode: String) {\n  category(\n    id: $id\n    storeId: $storeId\n    userId: $userId\n    cultureName: $cultureName\n    currencyCode: $currencyCode\n  ) {\n    ...Category\n  }\n}": typeof types.CategoryDocument;
  "mutation AddAddressToFavorites($command: AddAddressToFavoritesCommandType!) {\n  addAddressToFavorites(command: $command)\n}": typeof types.AddAddressToFavoritesDocument;
  "mutation ChangeOrganizationContactRole($command: InputChangeOrganizationContactRoleType!) {\n  changeOrganizationContactRole(command: $command) {\n    ...CustomIdentityResult\n  }\n}": typeof types.ChangeOrganizationContactRoleDocument;
  "mutation DeleteContact($command: InputDeleteContactType!) {\n  deleteContact(command: $command)\n}": typeof types.DeleteContactDocument;
  "mutation DeleteMemberAddresses($command: InputDeleteMemberAddressType!) {\n  deleteMemberAddresses(command: $command) {\n    addresses {\n      items {\n        ...MemberAddress\n      }\n    }\n  }\n}": typeof types.DeleteMemberAddressesDocument;
  "query GetContactAddresses($id: String!) {\n  contact(id: $id) {\n    addresses {\n      items {\n        ...MemberAddress\n      }\n    }\n  }\n}": typeof types.GetContactAddressesDocument;
  "query GetContactLockStatus($id: String!) {\n  contact(id: $id) {\n    isLockedInOrganization\n  }\n}": typeof types.GetContactLockStatusDocument;
  "query GetContactRolesInOrganization($id: String!) {\n  contact(id: $id) {\n    rolesInOrganization {\n      id\n      name\n    }\n  }\n}": typeof types.GetContactRolesInOrganizationDocument;
  "query GetContact($id: String!) {\n  contact(id: $id) {\n    ...Contact\n  }\n}": typeof types.GetContactDocument;
  "query GetCurrentCustomerAddresses($after: String, $first: Int, $countryCodes: [String], $regionIds: [String], $cities: [String], $keyword: String, $sort: String) {\n  currentCustomerAddresses(\n    after: $after\n    first: $first\n    countryCodes: $countryCodes\n    regionIds: $regionIds\n    cities: $cities\n    keyword: $keyword\n    sort: $sort\n  ) {\n    totalCount\n    items {\n      ...MemberAddress\n    }\n  }\n}": typeof types.GetCurrentCustomerAddressesDocument;
  "query GetCurrentOrganizationAddresses($after: String, $first: Int, $countryCodes: [String], $regionIds: [String], $cities: [String], $keyword: String, $sort: String) {\n  currentOrganizationAddresses(\n    after: $after\n    first: $first\n    countryCodes: $countryCodes\n    regionIds: $regionIds\n    cities: $cities\n    keyword: $keyword\n    sort: $sort\n  ) {\n    totalCount\n    items {\n      ...MemberAddress\n    }\n  }\n}": typeof types.GetCurrentOrganizationAddressesDocument;
  "query GetOrganizationContacts($organizationId: String!, $searchPhrase: String, $sort: String, $first: Int, $after: String) {\n  organization(id: $organizationId) {\n    contacts(searchPhrase: $searchPhrase, sort: $sort, first: $first, after: $after) {\n      items {\n        ...Contact\n      }\n    }\n  }\n}": typeof types.GetOrganizationContactsDocument;
  "query GetOrganizations($after: String, $first: Int, $sort: String, $searchPhrase: String, $statuses: [String]) {\n  me {\n    contact {\n      organizations(\n        after: $after\n        first: $first\n        sort: $sort\n        searchPhrase: $searchPhrase\n        statuses: $statuses\n      ) {\n        items {\n          id\n          name\n          isLockedForCurrentUser\n        }\n        totalCount\n        pageInfo {\n          hasNextPage\n          endCursor\n        }\n      }\n    }\n  }\n}": typeof types.GetOrganizationsDocument;
  "mutation LockOrganizationContact($command: InputLockUnlockOrganizationContactType!) {\n  lockOrganizationContact(command: $command) {\n    ...Contact\n  }\n}": typeof types.LockOrganizationContactDocument;
  "mutation RemoveAddressFromFavorites($command: RemoveAddressFromFavoritesCommandType!) {\n  removeAddressFromFavorites(command: $command)\n}": typeof types.RemoveAddressFromFavoritesDocument;
  "mutation RequestRegistration($command: InputRequestRegistrationType!) {\n  requestRegistration(command: $command) {\n    contact {\n      id\n      firstName\n      lastName\n      status\n    }\n    organization {\n      id\n      name\n      status\n      ownerId\n    }\n    account {\n      id\n      username\n      email\n      status\n    }\n    result {\n      succeeded\n      requireEmailVerification\n    }\n  }\n}": typeof types.RequestRegistrationDocument;
  "mutation UnlockOrganizationContact($command: InputLockUnlockOrganizationContactType!) {\n  unlockOrganizationContact(command: $command) {\n    ...Contact\n  }\n}": typeof types.UnlockOrganizationContactDocument;
  "mutation UpdateMemberAddresses($command: InputUpdateMemberAddressType!) {\n  updateMemberAddresses(command: $command) {\n    addresses {\n      items {\n        ...MemberAddress\n      }\n    }\n  }\n}": typeof types.UpdateMemberAddressesDocument;
  "query Order($number: String, $cultureName: String) {\n  order(number: $number, cultureName: $cultureName) {\n    ...Order\n  }\n}": typeof types.OrderDocument;
  "query Orders($userId: String, $filter: String, $sort: String, $cultureName: String, $first: Int, $after: String) {\n  orders(\n    userId: $userId\n    filter: $filter\n    sort: $sort\n    cultureName: $cultureName\n    first: $first\n    after: $after\n  ) {\n    items {\n      ...Order\n    }\n  }\n}": typeof types.OrdersDocument;
  "query OrganizationOrders($organizationId: String, $filter: String, $sort: String, $cultureName: String, $first: Int, $after: String) {\n  organizationOrders(\n    organizationId: $organizationId\n    filter: $filter\n    sort: $sort\n    cultureName: $cultureName\n    first: $first\n    after: $after\n  ) {\n    items {\n      ...Order\n    }\n  }\n}": typeof types.OrganizationOrdersDocument;
  "query PageContext($storeId: String, $userId: String, $cultureName: String, $permalink: String, $organizationId: String) {\n  pageContext(\n    storeId: $storeId\n    userId: $userId\n    cultureName: $cultureName\n    permalink: $permalink\n    organizationId: $organizationId\n  ) {\n    ...PageContext\n  }\n}": typeof types.PageContextDocument;
  "query CartPickupLocations($cartId: String!, $storeId: String!, $cultureName: String!, $keyword: String, $sort: String, $first: Int, $after: String, $facet: String, $filter: String) {\n  cartPickupLocations(\n    cartId: $cartId\n    storeId: $storeId\n    cultureName: $cultureName\n    keyword: $keyword\n    sort: $sort\n    first: $first\n    after: $after\n    facet: $facet\n    filter: $filter\n  ) {\n    items {\n      ...ProductPickupLocation\n    }\n  }\n}": typeof types.CartPickupLocationsDocument;
  "query PickupLocations($storeId: String, $keyword: String, $sort: String, $first: Int, $after: String) {\n  pickupLocations(\n    storeId: $storeId\n    keyword: $keyword\n    sort: $sort\n    first: $first\n    after: $after\n  ) {\n    items {\n      ...PickupLocation\n    }\n  }\n}": typeof types.PickupLocationsDocument;
  "query ProductPickupLocations($productId: String!, $storeId: String!, $cultureName: String!, $keyword: String, $sort: String, $first: Int, $after: String) {\n  productPickupLocations(\n    productId: $productId\n    storeId: $storeId\n    cultureName: $cultureName\n    keyword: $keyword\n    sort: $sort\n    first: $first\n    after: $after\n  ) {\n    items {\n      ...ProductPickupLocation\n    }\n  }\n}": typeof types.ProductPickupLocationsDocument;
  "mutation CreateConfiguredLineItem($command: InputCreateConfiguredLineItemCommand!) {\n  createConfiguredLineItem(command: $command) {\n    ...ConfigurationLineItem\n  }\n}": typeof types.CreateConfiguredLineItemDocument;
  "query ProductConfiguration($configurableProductId: String!, $storeId: String!, $userId: String, $cultureName: String, $currencyCode: String) {\n  productConfiguration(\n    configurableProductId: $configurableProductId\n    storeId: $storeId\n    userId: $userId\n    cultureName: $cultureName\n    currencyCode: $currencyCode\n  ) {\n    ...ProductConfiguration\n  }\n}": typeof types.ProductConfigurationDocument;
  "query Product($id: String!, $storeId: String!, $userId: String, $cultureName: String, $currencyCode: String) {\n  product(\n    id: $id\n    storeId: $storeId\n    userId: $userId\n    cultureName: $cultureName\n    currencyCode: $currencyCode\n  ) {\n    ...Product\n  }\n}": typeof types.ProductDocument;
  "query Products($storeId: String!, $userId: String, $cultureName: String, $currencyCode: String, $query: String, $filter: String, $sort: String, $first: Int, $after: String) {\n  products(\n    storeId: $storeId\n    userId: $userId\n    cultureName: $cultureName\n    currencyCode: $currencyCode\n    query: $query\n    filter: $filter\n    sort: $sort\n    first: $first\n    after: $after\n  ) {\n    items {\n      ...Product\n    }\n  }\n}": typeof types.ProductsDocument;
  "mutation CancelQuoteRequest($command: CancelQuoteCommandType!) {\n  cancelQuoteRequest(command: $command) {\n    ...Quote\n  }\n}": typeof types.CancelQuoteRequestDocument;
  "mutation ChangeQuoteComment($command: ChangeQuoteCommentCommandType!) {\n  changeQuoteComment(command: $command) {\n    ...Quote\n  }\n}": typeof types.ChangeQuoteCommentDocument;
  "mutation ChangeQuoteItemQuantity($command: ChangeQuoteItemQuantityCommandType!) {\n  changeQuoteItemQuantity(command: $command) {\n    ...Quote\n  }\n}": typeof types.ChangeQuoteItemQuantityDocument;
  "mutation CreateQuoteFromCart($command: CreateQuoteFromCartCommandType!) {\n  createQuoteFromCart(command: $command) {\n    ...Quote\n  }\n}": typeof types.CreateQuoteFromCartDocument;
  "mutation CreateQuote($command: CreateQuoteCommandType!) {\n  createQuote(command: $command) {\n    ...Quote\n  }\n}": typeof types.CreateQuoteDocument;
  "query GetQuote($id: String!, $storeId: String, $userId: String, $cultureName: String, $currencyCode: String) {\n  quote(\n    id: $id\n    storeId: $storeId\n    userId: $userId\n    cultureName: $cultureName\n    currencyCode: $currencyCode\n  ) {\n    ...Quote\n    addresses {\n      ...QuoteAddress\n    }\n  }\n}": typeof types.GetQuoteDocument;
  "mutation RemoveQuoteItem($command: RemoveQuoteItemCommandType!) {\n  removeQuoteItem(command: $command) {\n    ...Quote\n  }\n}": typeof types.RemoveQuoteItemDocument;
  "mutation SubmitQuoteRequest($command: SubmitQuoteCommandType!) {\n  submitQuoteRequest(command: $command) {\n    ...Quote\n  }\n}": typeof types.SubmitQuoteRequestDocument;
  "mutation UpdateQuoteAddresses($command: UpdateQuoteAddressesCommandType!) {\n  updateQuoteAddresses(command: $command) {\n    ...Quote\n    addresses {\n      ...QuoteAddress\n    }\n  }\n}": typeof types.UpdateQuoteAddressesDocument;
  "query GetSavedForLater($storeId: String!, $userId: String!, $currencyCode: String, $cultureName: String) {\n  getSavedForLater(\n    storeId: $storeId\n    userId: $userId\n    currencyCode: $currencyCode\n    cultureName: $cultureName\n  ) {\n    ...Cart\n  }\n}": typeof types.GetSavedForLaterDocument;
  "mutation MoveFromSavedForLater($command: InputSaveForLaterType!) {\n  moveFromSavedForLater(command: $command) {\n    ...CartWithList\n  }\n}": typeof types.MoveFromSavedForLaterDocument;
  "mutation MoveToSavedForLater($command: InputSaveForLaterType!) {\n  moveToSavedForLater(command: $command) {\n    ...CartWithList\n  }\n}": typeof types.MoveToSavedForLaterDocument;
  "query SlugInfo($storeId: String, $slug: String, $permalink: String, $userId: String, $cultureName: String) {\n  slugInfo(\n    storeId: $storeId\n    slug: $slug\n    permalink: $permalink\n    userId: $userId\n    cultureName: $cultureName\n  ) {\n    ...SlugInfo\n  }\n}": typeof types.SlugInfoDocument;
  "mutation AddBulkItemToShoppingList($command: InputAddWishlistBulkItemType!) {\n  addWishlistBulkItem(command: $command) {\n    wishlists {\n      ...ShoppingList\n    }\n  }\n}": typeof types.AddBulkItemToShoppingListDocument;
  "mutation AddItemsToShoppingList($command: InputAddWishlistItemsType!) {\n  addWishlistItems(command: $command) {\n    ...ShoppingList\n  }\n}": typeof types.AddItemsToShoppingListDocument;
  "mutation ChangeShoppingList($command: InputChangeWishlistType!) {\n  changeWishlist(command: $command) {\n    ...ShoppingList\n  }\n}": typeof types.ChangeShoppingListDocument;
  "mutation CreateShoppingList($command: InputCreateWishlistType!) {\n  createWishlist(command: $command) {\n    ...ShoppingList\n  }\n}": typeof types.CreateShoppingListDocument;
  "mutation DeleteShoppingList($command: InputRemoveWishlistType!) {\n  removeWishlist(command: $command)\n}": typeof types.DeleteShoppingListDocument;
  "query GetShoppingList($listId: String!, $cultureName: String) {\n  wishlist(listId: $listId, cultureName: $cultureName) {\n    ...ShoppingList\n  }\n}": typeof types.GetShoppingListDocument;
  "query GetShoppingLists($storeId: String, $userId: String, $currencyCode: String, $cultureName: String) {\n  wishlists(\n    storeId: $storeId\n    userId: $userId\n    currencyCode: $currencyCode\n    cultureName: $cultureName\n  ) {\n    items {\n      ...ShoppingList\n    }\n  }\n}": typeof types.GetShoppingListsDocument;
  "mutation RemoveItemsFromShoppingList($command: InputRemoveWishlistItemsType!) {\n  removeWishlistItems(command: $command) {\n    ...ShoppingList\n  }\n}": typeof types.RemoveItemsFromShoppingListDocument;
  "mutation UpdateShoppingListItems($command: InputUpdateWishlistItemsType!) {\n  updateWishListItems(command: $command) {\n    ...ShoppingList\n  }\n}": typeof types.UpdateShoppingListItemsDocument;
  "mutation DeleteUsers($command: InputDeleteUserType!) {\n  deleteUsers(command: $command) {\n    ...IdentityResult\n  }\n}": typeof types.DeleteUsersDocument;
  "query GetMe {\n  me {\n    ...User\n  }\n}": typeof types.GetMeDocument;
  "query GetUser($userName: String, $email: String, $id: String) {\n  user(userName: $userName, email: $email, id: $id) {\n    ...User\n  }\n}": typeof types.GetUserDocument;
  "mutation InviteUser($command: InputInviteUserType!) {\n  inviteUser(command: $command) {\n    ...CustomIdentityResult\n  }\n}": typeof types.InviteUserDocument;
  "mutation RegisterByInvitation($command: InputRegisterByInvitationType!) {\n  registerByInvitation(command: $command) {\n    ...CustomIdentityResult\n  }\n}": typeof types.RegisterByInvitationDocument;
  "mutation ResetPasswordByToken($command: InputResetPasswordByTokenType!) {\n  resetPasswordByToken(command: $command) {\n    ...CustomIdentityResult\n  }\n}": typeof types.ResetPasswordByTokenDocument;
  "mutation SendPasswordResetEmail($command: SendPasswordResetEmailCommandType!) {\n  sendPasswordResetEmail(command: $command)\n}": typeof types.SendPasswordResetEmailDocument;
};
const documents: Documents = {
  "fragment CartAddress on CartAddressType {\n  id\n  key\n  city\n  countryCode\n  countryName\n  email\n  firstName\n  middleName\n  lastName\n  line1\n  line2\n  name\n  organization\n  phone\n  postalCode\n  regionId\n  regionName\n  zip\n  outerId\n  description\n  addressType\n}":
    types.CartAddressFragmentDoc,
  "fragment CartConfigurationItem on CartConfigurationItemType {\n  id\n  sectionId\n  type\n  productId\n  name\n  sku\n  imageUrl\n  quantity\n  customText\n  selectedForCheckout\n}":
    types.CartConfigurationItemFragmentDoc,
  "fragment CartWithList on CartWithListType {\n  cart {\n    ...Cart\n  }\n  list {\n    ...Cart\n  }\n}":
    types.CartWithListFragmentDoc,
  "fragment Cart on CartType {\n  id\n  storeId\n  isAnonymous\n  hasPhysicalProducts\n  customerId\n  itemsCount\n  itemsQuantity\n  total {\n    ...Money\n  }\n  subTotal {\n    ...Money\n  }\n  subTotalDiscount {\n    ...Money\n  }\n  shippingTotal {\n    ...Money\n  }\n  items {\n    ...LineItem\n  }\n  payments {\n    ...Payment\n  }\n  shipments {\n    ...Shipment\n  }\n  coupons {\n    ...Coupon\n  }\n  gifts {\n    ...GiftItem\n  }\n  addresses {\n    ...CartAddress\n  }\n  validationErrors {\n    errorCode\n    errorMessage\n    errorParameters {\n      key\n      value\n    }\n    objectType\n    objectId\n  }\n}":
    types.CartFragmentDoc,
  "fragment Category on Category {\n  id\n  code\n  name\n  outline\n  slug\n}": types.CategoryFragmentDoc,
  "fragment ConfigurationLineItem on ConfigurationLineItemType {\n  id\n  text\n  quantity\n  product {\n    ...Product\n  }\n  listPrice {\n    ...Money\n  }\n  salePrice {\n    ...Money\n  }\n  extendedPrice {\n    ...Money\n  }\n  discountAmount {\n    ...Money\n  }\n}":
    types.ConfigurationLineItemFragmentDoc,
  "fragment Contact on ContactType {\n  id\n  firstName\n  lastName\n  fullName\n  status\n  organizationId\n  organizationsIds\n  securityAccounts {\n    ...User\n  }\n}":
    types.ContactFragmentDoc,
  "fragment Coupon on CouponType {\n  code\n  isAppliedSuccessfully\n}": types.CouponFragmentDoc,
  "fragment Currency on CurrencyType {\n  code\n}": types.CurrencyFragmentDoc,
  "fragment CustomIdentityResult on CustomIdentityResultType {\n  succeeded\n  errors {\n    code\n    parameter\n    description\n  }\n}":
    types.CustomIdentityResultFragmentDoc,
  "fragment GiftItem on GiftItemType {\n  id\n  quantity\n  productId\n  name\n  lineItemId\n}":
    types.GiftItemFragmentDoc,
  "fragment IdentityResult on IdentityResultType {\n  succeeded\n  errors {\n    code\n    description\n  }\n}":
    types.IdentityResultFragmentDoc,
  "fragment Language on LanguageType {\n  cultureName\n  nativeName\n}": types.LanguageFragmentDoc,
  "fragment LineItem on LineItemType {\n  id\n  sku\n  productId\n  name\n  quantity\n  listPrice {\n    ...Money\n  }\n  salePrice {\n    ...Money\n  }\n  placedPrice {\n    ...Money\n  }\n  extendedPrice {\n    ...Money\n  }\n  discountAmount {\n    ...Money\n  }\n  selectedForCheckout\n  isValid\n  validationErrors {\n    errorCode\n    errorMessage\n    errorParameters {\n      key\n      value\n    }\n    objectType\n    objectId\n  }\n  configurationItems {\n    ...CartConfigurationItem\n  }\n}":
    types.LineItemFragmentDoc,
  "fragment MemberAddress on MemberAddressType {\n  id\n  key\n  isDefault\n  isFavorite\n  city\n  countryCode\n  countryName\n  email\n  firstName\n  middleName\n  lastName\n  line1\n  line2\n  name\n  organization\n  phone\n  postalCode\n  regionId\n  regionName\n  zip\n  outerId\n  description\n  addressType\n}":
    types.MemberAddressFragmentDoc,
  "fragment MenuLink on MenuLinkType {\n  title\n  url\n  priority\n}": types.MenuLinkFragmentDoc,
  "fragment Money on MoneyType {\n  amount\n  formattedAmount\n}": types.MoneyFragmentDoc,
  "fragment OrderLineItem on OrderLineItemType {\n  id\n  name\n  sku\n  productId\n  quantity\n  price {\n    ...Money\n  }\n  extendedPrice {\n    ...Money\n  }\n}":
    types.OrderLineItemFragmentDoc,
  "fragment OrderPayment on PaymentInType {\n  id\n  number\n  gatewayCode\n  status\n  sum {\n    ...Money\n  }\n}":
    types.OrderPaymentFragmentDoc,
  "fragment OrderShipment on OrderShipmentType {\n  id\n  number\n  shipmentMethodCode\n  shipmentMethodOption\n  status\n  total {\n    ...Money\n  }\n}":
    types.OrderShipmentFragmentDoc,
  "fragment Order on CustomerOrderType {\n  id\n  number\n  status\n  createdDate\n  total {\n    ...Money\n  }\n  items {\n    ...OrderLineItem\n  }\n  inPayments {\n    ...OrderPayment\n  }\n  shipments {\n    ...OrderShipment\n  }\n}":
    types.OrderFragmentDoc,
  "fragment PageContext on PageContextResponseType {\n  slugInfo {\n    ...SlugInfo\n  }\n  store {\n    ...StoreInfo\n  }\n  whiteLabelingSettings {\n    ...WhiteLabelingSettings\n  }\n  user {\n    ...User\n  }\n}":
    types.PageContextFragmentDoc,
  "fragment Payment on PaymentType {\n  id\n  outerId\n  paymentGatewayCode\n  currency {\n    ...Currency\n  }\n  total {\n    ...Money\n  }\n  billingAddress {\n    ...CartAddress\n  }\n}":
    types.PaymentFragmentDoc,
  "fragment PickupAddress on PickupAddressType {\n  id\n  key\n  name\n  organization\n  countryCode\n  countryName\n  city\n  postalCode\n  line1\n  line2\n  regionId\n  regionName\n  phone\n  email\n  outerId\n  description\n  addressType\n}":
    types.PickupAddressFragmentDoc,
  "fragment PickupLocationAddress on PickupLocationAddressType {\n  id\n  key\n  name\n  organization\n  countryCode\n  countryName\n  city\n  postalCode\n  line1\n  line2\n  regionId\n  regionName\n  phone\n  email\n  outerId\n  description\n  addressType\n}":
    types.PickupLocationAddressFragmentDoc,
  "fragment PickupLocation on PickupLocationType {\n  id\n  isActive\n  name\n  description\n  contactEmail\n  contactPhone\n  workingHours\n  geoLocation\n  address {\n    ...PickupAddress\n  }\n}":
    types.PickupLocationFragmentDoc,
  "fragment ProductConfiguration on ConfigurationQueryResponseType {\n  configurationSections {\n    id\n    name\n    description\n    isRequired\n    type\n    allowCustomText\n    allowTextOptions\n    maxLength\n    options {\n      ...ConfigurationLineItem\n    }\n  }\n}":
    types.ProductConfigurationFragmentDoc,
  "fragment ProductPickupLocation on ProductPickupLocation {\n  id\n  isActive\n  name\n  description\n  contactEmail\n  contactPhone\n  workingHours\n  deliveryDays\n  storageDays\n  geoLocation\n  address {\n    ...PickupLocationAddress\n  }\n  availabilityType\n  availabilityNote\n  availableQuantity\n}":
    types.ProductPickupLocationFragmentDoc,
  "fragment ProductPrice on PriceType {\n  list {\n    ...Money\n  }\n  actual {\n    ...Money\n  }\n}":
    types.ProductPriceFragmentDoc,
  "fragment Product on Product {\n  id\n  code\n  productType\n  isConfigurable\n  name\n  vendor {\n    ...Vendor\n  }\n  price {\n    ...ProductPrice\n  }\n}":
    types.ProductFragmentDoc,
  "fragment QuoteAddress on QuoteAddressType {\n  addressType\n  city\n  countryCode\n  countryName\n  line1\n  postalCode\n  regionId\n  regionName\n}":
    types.QuoteAddressFragmentDoc,
  "fragment QuoteItem on QuoteItemType {\n  id\n  name\n  sku\n  productId\n  quantity\n  listPrice {\n    ...Money\n  }\n  salePrice {\n    ...Money\n  }\n  proposalPrices {\n    quantity\n    price {\n      ...Money\n    }\n  }\n}":
    types.QuoteItemFragmentDoc,
  "fragment QuoteTotals on QuoteTotalsType {\n  originalSubTotalExlTax {\n    ...Money\n  }\n  subTotalExlTax {\n    ...Money\n  }\n  shippingTotal {\n    ...Money\n  }\n  discountTotal {\n    ...Money\n  }\n  taxTotal {\n    ...Money\n  }\n  grandTotalExlTax {\n    ...Money\n  }\n  grandTotalInclTax {\n    ...Money\n  }\n}":
    types.QuoteTotalsFragmentDoc,
  "fragment Quote on QuoteType {\n  id\n  number\n  status\n  storeId\n  customerId\n  comment\n  isAnonymous\n  isCancelled\n  totals {\n    ...QuoteTotals\n  }\n  items {\n    ...QuoteItem\n  }\n}":
    types.QuoteFragmentDoc,
  "fragment Role on RoleType {\n  id\n  name\n  normalizedName\n}": types.RoleFragmentDoc,
  "fragment SeoInfo on SeoInfo {\n  id\n  name\n  semanticUrl\n  outline\n  pageTitle\n  metaDescription\n  imageAltDescription\n  metaKeywords\n  storeId\n  objectId\n  objectType\n  isActive\n  languageCode\n}":
    types.SeoInfoFragmentDoc,
  "fragment Shipment on ShipmentType {\n  id\n  shipmentMethodCode\n  shipmentMethodOption\n  fulfillmentCenterId\n  price {\n    ...Money\n  }\n  currency {\n    ...Currency\n  }\n  deliveryAddress {\n    ...CartAddress\n  }\n}":
    types.ShipmentFragmentDoc,
  "fragment ShoppingList on WishlistType {\n  id\n  name\n  storeId\n  customerId\n  customerName\n  items {\n    ...WishlistLineItem\n  }\n  itemsCount\n  description\n  subTotal {\n    ...Money\n  }\n  sharingSetting {\n    id\n    scope\n  }\n}":
    types.ShoppingListFragmentDoc,
  "fragment SlugInfo on SlugInfoResponseType {\n  entityInfo {\n    ...SeoInfo\n  }\n  redirectUrl\n}":
    types.SlugInfoFragmentDoc,
  "fragment StoreInfo on StoreResponseType {\n  storeId\n  storeName\n  catalogId\n  storeUrl\n  defaultLanguage {\n    ...Language\n  }\n  availableLanguages {\n    ...Language\n  }\n  defaultCurrency {\n    ...Currency\n  }\n  availableCurrencies {\n    ...Currency\n  }\n  settings {\n    ...StoreSettings\n  }\n}":
    types.StoreInfoFragmentDoc,
  "fragment StoreSettings on StoreSettingsType {\n  anonymousUsersAllowed\n  taxCalculationEnabled\n  seoLinkType\n}":
    types.StoreSettingsFragmentDoc,
  "fragment User on UserType {\n  id\n  userName\n  email\n  emailConfirmed\n  isAdministrator\n  memberId\n  storeId\n  roles {\n    ...Role\n  }\n}":
    types.UserFragmentDoc,
  "fragment Vendor on CommonVendor {\n  id\n  name\n}": types.VendorFragmentDoc,
  "fragment WhiteLabelingSettings on WhiteLabelingSettingsType {\n  logoUrl\n  secondaryLogoUrl\n  faviconUrl\n  themePresetName\n  footerLinks {\n    ...MenuLink\n  }\n  mainMenuLinks {\n    ...MenuLink\n  }\n}":
    types.WhiteLabelingSettingsFragmentDoc,
  "fragment WishlistLineItem on LineItemType {\n  id\n  sku\n  productId\n  name\n  quantity\n}":
    types.WishlistLineItemFragmentDoc,
  "mutation AddBulkItemsCart($command: InputAddBulkItemsType!) {\n  addBulkItemsCart(command: $command) {\n    cart {\n      ...Cart\n    }\n    errors {\n      errorCode\n      errorMessage\n      objectId\n    }\n  }\n}":
    types.AddBulkItemsCartDocument,
  "mutation AddCoupon($command: InputAddCouponType!) {\n  addCoupon(command: $command) {\n    ...Cart\n  }\n}":
    types.AddCouponDocument,
  "mutation AddItem($command: InputAddItemType!) {\n  addItem(command: $command) {\n    ...Cart\n  }\n}":
    types.AddItemDocument,
  "mutation AddItemsCart($command: InputAddItemsType!) {\n  addItemsCart(command: $command) {\n    ...Cart\n  }\n}":
    types.AddItemsCartDocument,
  "mutation AddOrUpdateCartPayment($command: InputAddOrUpdateCartPaymentType!) {\n  addOrUpdateCartPayment(command: $command) {\n    ...Cart\n  }\n}":
    types.AddOrUpdateCartPaymentDocument,
  "mutation AddOrUpdateCartShipment($command: InputAddOrUpdateCartShipmentType!) {\n  addOrUpdateCartShipment(command: $command) {\n    ...Cart\n  }\n}":
    types.AddOrUpdateCartShipmentDocument,
  "mutation ChangeCartConfiguredItem($command: InputChangeCartConfiguredItemType!) {\n  changeCartConfiguredItem(command: $command) {\n    ...Cart\n  }\n}":
    types.ChangeCartConfiguredItemDocument,
  "mutation ClearCart($command: InputClearCartType!) {\n  clearCart(command: $command) {\n    ...Cart\n  }\n}":
    types.ClearCartDocument,
  "mutation CreateOrderFromCart($command: InputCreateOrderFromCartType!) {\n  createOrderFromCart(command: $command) {\n    ...Order\n  }\n}":
    types.CreateOrderFromCartDocument,
  "query GetCartLineValidation($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String!, $cartId: String) {\n  cart(\n    storeId: $storeId\n    userId: $userId\n    currencyCode: $currencyCode\n    cultureName: $cultureName\n    cartId: $cartId\n  ) {\n    itemsCount\n    items {\n      id\n      sku\n      productId\n      quantity\n      isValid\n      validationErrors {\n        errorCode\n        objectType\n        objectId\n        errorMessage\n      }\n    }\n  }\n}":
    types.GetCartLineValidationDocument,
  "query GetCartValidationAliased($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String!, $ruleSetA: String, $ruleSetB: String, $cartId: String) {\n  cart(\n    storeId: $storeId\n    userId: $userId\n    currencyCode: $currencyCode\n    cultureName: $cultureName\n    cartId: $cartId\n  ) {\n    itemsCount\n    errorsA: validationErrors(ruleSet: $ruleSetA) {\n      errorCode\n      objectType\n      objectId\n      errorMessage\n    }\n    errorsB: validationErrors(ruleSet: $ruleSetB) {\n      errorCode\n      objectType\n      objectId\n      errorMessage\n    }\n  }\n}":
    types.GetCartValidationAliasedDocument,
  "query GetCartValidation($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String!, $ruleSet: String, $cartId: String) {\n  cart(\n    storeId: $storeId\n    userId: $userId\n    currencyCode: $currencyCode\n    cultureName: $cultureName\n    cartId: $cartId\n  ) {\n    itemsCount\n    validationErrors(ruleSet: $ruleSet) {\n      errorCode\n      objectType\n      objectId\n      errorMessage\n    }\n    items {\n      id\n      sku\n      productId\n      quantity\n      isValid\n      validationErrors {\n        errorCode\n        objectType\n        objectId\n        errorMessage\n      }\n    }\n  }\n}":
    types.GetCartValidationDocument,
  "query GetCart($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String!, $cartId: String, $cartName: String) {\n  cart(\n    storeId: $storeId\n    userId: $userId\n    currencyCode: $currencyCode\n    cultureName: $cultureName\n    cartId: $cartId\n    cartName: $cartName\n  ) {\n    ...Cart\n  }\n}":
    types.GetCartDocument,
  "mutation MergeCart($command: InputMergeCartType!) {\n  mergeCart(command: $command) {\n    ...Cart\n  }\n}":
    types.MergeCartDocument,
  "mutation RemoveCartItem($command: InputRemoveItemType!) {\n  removeCartItem(command: $command) {\n    ...Cart\n  }\n}":
    types.RemoveCartItemDocument,
  "mutation RemoveCart($command: InputRemoveCartType!) {\n  removeCart(command: $command)\n}": types.RemoveCartDocument,
  "mutation RemoveCoupon($command: InputRemoveCouponType!) {\n  removeCoupon(command: $command) {\n    ...Cart\n  }\n}":
    types.RemoveCouponDocument,
  "mutation SelectCartItems($command: InputChangeCartItemsSelectedType!) {\n  selectCartItems(command: $command) {\n    ...Cart\n  }\n}":
    types.SelectCartItemsDocument,
  "mutation UnSelectAllCartItems($command: InputChangeAllCartItemsSelectedType!) {\n  unSelectAllCartItems(command: $command) {\n    ...Cart\n  }\n}":
    types.UnSelectAllCartItemsDocument,
  "mutation UnSelectCartItems($command: InputChangeCartItemsSelectedType!) {\n  unSelectCartItems(command: $command) {\n    ...Cart\n  }\n}":
    types.UnSelectCartItemsDocument,
  "mutation UpdateCartQuantity($command: InputUpdateCartQuantity!) {\n  updateCartQuantity(command: $command) {\n    ...Cart\n  }\n}":
    types.UpdateCartQuantityDocument,
  "query Categories($storeId: String!, $userId: String, $cultureName: String, $currencyCode: String, $filter: String, $first: Int) {\n  categories(\n    storeId: $storeId\n    userId: $userId\n    cultureName: $cultureName\n    currencyCode: $currencyCode\n    filter: $filter\n    first: $first\n  ) {\n    totalCount\n    items {\n      ...Category\n    }\n  }\n}":
    types.CategoriesDocument,
  "query Category($id: String!, $storeId: String!, $userId: String, $cultureName: String, $currencyCode: String) {\n  category(\n    id: $id\n    storeId: $storeId\n    userId: $userId\n    cultureName: $cultureName\n    currencyCode: $currencyCode\n  ) {\n    ...Category\n  }\n}":
    types.CategoryDocument,
  "mutation AddAddressToFavorites($command: AddAddressToFavoritesCommandType!) {\n  addAddressToFavorites(command: $command)\n}":
    types.AddAddressToFavoritesDocument,
  "mutation ChangeOrganizationContactRole($command: InputChangeOrganizationContactRoleType!) {\n  changeOrganizationContactRole(command: $command) {\n    ...CustomIdentityResult\n  }\n}":
    types.ChangeOrganizationContactRoleDocument,
  "mutation DeleteContact($command: InputDeleteContactType!) {\n  deleteContact(command: $command)\n}":
    types.DeleteContactDocument,
  "mutation DeleteMemberAddresses($command: InputDeleteMemberAddressType!) {\n  deleteMemberAddresses(command: $command) {\n    addresses {\n      items {\n        ...MemberAddress\n      }\n    }\n  }\n}":
    types.DeleteMemberAddressesDocument,
  "query GetContactAddresses($id: String!) {\n  contact(id: $id) {\n    addresses {\n      items {\n        ...MemberAddress\n      }\n    }\n  }\n}":
    types.GetContactAddressesDocument,
  "query GetContactLockStatus($id: String!) {\n  contact(id: $id) {\n    isLockedInOrganization\n  }\n}":
    types.GetContactLockStatusDocument,
  "query GetContactRolesInOrganization($id: String!) {\n  contact(id: $id) {\n    rolesInOrganization {\n      id\n      name\n    }\n  }\n}":
    types.GetContactRolesInOrganizationDocument,
  "query GetContact($id: String!) {\n  contact(id: $id) {\n    ...Contact\n  }\n}": types.GetContactDocument,
  "query GetCurrentCustomerAddresses($after: String, $first: Int, $countryCodes: [String], $regionIds: [String], $cities: [String], $keyword: String, $sort: String) {\n  currentCustomerAddresses(\n    after: $after\n    first: $first\n    countryCodes: $countryCodes\n    regionIds: $regionIds\n    cities: $cities\n    keyword: $keyword\n    sort: $sort\n  ) {\n    totalCount\n    items {\n      ...MemberAddress\n    }\n  }\n}":
    types.GetCurrentCustomerAddressesDocument,
  "query GetCurrentOrganizationAddresses($after: String, $first: Int, $countryCodes: [String], $regionIds: [String], $cities: [String], $keyword: String, $sort: String) {\n  currentOrganizationAddresses(\n    after: $after\n    first: $first\n    countryCodes: $countryCodes\n    regionIds: $regionIds\n    cities: $cities\n    keyword: $keyword\n    sort: $sort\n  ) {\n    totalCount\n    items {\n      ...MemberAddress\n    }\n  }\n}":
    types.GetCurrentOrganizationAddressesDocument,
  "query GetOrganizationContacts($organizationId: String!, $searchPhrase: String, $sort: String, $first: Int, $after: String) {\n  organization(id: $organizationId) {\n    contacts(searchPhrase: $searchPhrase, sort: $sort, first: $first, after: $after) {\n      items {\n        ...Contact\n      }\n    }\n  }\n}":
    types.GetOrganizationContactsDocument,
  "query GetOrganizations($after: String, $first: Int, $sort: String, $searchPhrase: String, $statuses: [String]) {\n  me {\n    contact {\n      organizations(\n        after: $after\n        first: $first\n        sort: $sort\n        searchPhrase: $searchPhrase\n        statuses: $statuses\n      ) {\n        items {\n          id\n          name\n          isLockedForCurrentUser\n        }\n        totalCount\n        pageInfo {\n          hasNextPage\n          endCursor\n        }\n      }\n    }\n  }\n}":
    types.GetOrganizationsDocument,
  "mutation LockOrganizationContact($command: InputLockUnlockOrganizationContactType!) {\n  lockOrganizationContact(command: $command) {\n    ...Contact\n  }\n}":
    types.LockOrganizationContactDocument,
  "mutation RemoveAddressFromFavorites($command: RemoveAddressFromFavoritesCommandType!) {\n  removeAddressFromFavorites(command: $command)\n}":
    types.RemoveAddressFromFavoritesDocument,
  "mutation RequestRegistration($command: InputRequestRegistrationType!) {\n  requestRegistration(command: $command) {\n    contact {\n      id\n      firstName\n      lastName\n      status\n    }\n    organization {\n      id\n      name\n      status\n      ownerId\n    }\n    account {\n      id\n      username\n      email\n      status\n    }\n    result {\n      succeeded\n      requireEmailVerification\n    }\n  }\n}":
    types.RequestRegistrationDocument,
  "mutation UnlockOrganizationContact($command: InputLockUnlockOrganizationContactType!) {\n  unlockOrganizationContact(command: $command) {\n    ...Contact\n  }\n}":
    types.UnlockOrganizationContactDocument,
  "mutation UpdateMemberAddresses($command: InputUpdateMemberAddressType!) {\n  updateMemberAddresses(command: $command) {\n    addresses {\n      items {\n        ...MemberAddress\n      }\n    }\n  }\n}":
    types.UpdateMemberAddressesDocument,
  "query Order($number: String, $cultureName: String) {\n  order(number: $number, cultureName: $cultureName) {\n    ...Order\n  }\n}":
    types.OrderDocument,
  "query Orders($userId: String, $filter: String, $sort: String, $cultureName: String, $first: Int, $after: String) {\n  orders(\n    userId: $userId\n    filter: $filter\n    sort: $sort\n    cultureName: $cultureName\n    first: $first\n    after: $after\n  ) {\n    items {\n      ...Order\n    }\n  }\n}":
    types.OrdersDocument,
  "query OrganizationOrders($organizationId: String, $filter: String, $sort: String, $cultureName: String, $first: Int, $after: String) {\n  organizationOrders(\n    organizationId: $organizationId\n    filter: $filter\n    sort: $sort\n    cultureName: $cultureName\n    first: $first\n    after: $after\n  ) {\n    items {\n      ...Order\n    }\n  }\n}":
    types.OrganizationOrdersDocument,
  "query PageContext($storeId: String, $userId: String, $cultureName: String, $permalink: String, $organizationId: String) {\n  pageContext(\n    storeId: $storeId\n    userId: $userId\n    cultureName: $cultureName\n    permalink: $permalink\n    organizationId: $organizationId\n  ) {\n    ...PageContext\n  }\n}":
    types.PageContextDocument,
  "query CartPickupLocations($cartId: String!, $storeId: String!, $cultureName: String!, $keyword: String, $sort: String, $first: Int, $after: String, $facet: String, $filter: String) {\n  cartPickupLocations(\n    cartId: $cartId\n    storeId: $storeId\n    cultureName: $cultureName\n    keyword: $keyword\n    sort: $sort\n    first: $first\n    after: $after\n    facet: $facet\n    filter: $filter\n  ) {\n    items {\n      ...ProductPickupLocation\n    }\n  }\n}":
    types.CartPickupLocationsDocument,
  "query PickupLocations($storeId: String, $keyword: String, $sort: String, $first: Int, $after: String) {\n  pickupLocations(\n    storeId: $storeId\n    keyword: $keyword\n    sort: $sort\n    first: $first\n    after: $after\n  ) {\n    items {\n      ...PickupLocation\n    }\n  }\n}":
    types.PickupLocationsDocument,
  "query ProductPickupLocations($productId: String!, $storeId: String!, $cultureName: String!, $keyword: String, $sort: String, $first: Int, $after: String) {\n  productPickupLocations(\n    productId: $productId\n    storeId: $storeId\n    cultureName: $cultureName\n    keyword: $keyword\n    sort: $sort\n    first: $first\n    after: $after\n  ) {\n    items {\n      ...ProductPickupLocation\n    }\n  }\n}":
    types.ProductPickupLocationsDocument,
  "mutation CreateConfiguredLineItem($command: InputCreateConfiguredLineItemCommand!) {\n  createConfiguredLineItem(command: $command) {\n    ...ConfigurationLineItem\n  }\n}":
    types.CreateConfiguredLineItemDocument,
  "query ProductConfiguration($configurableProductId: String!, $storeId: String!, $userId: String, $cultureName: String, $currencyCode: String) {\n  productConfiguration(\n    configurableProductId: $configurableProductId\n    storeId: $storeId\n    userId: $userId\n    cultureName: $cultureName\n    currencyCode: $currencyCode\n  ) {\n    ...ProductConfiguration\n  }\n}":
    types.ProductConfigurationDocument,
  "query Product($id: String!, $storeId: String!, $userId: String, $cultureName: String, $currencyCode: String) {\n  product(\n    id: $id\n    storeId: $storeId\n    userId: $userId\n    cultureName: $cultureName\n    currencyCode: $currencyCode\n  ) {\n    ...Product\n  }\n}":
    types.ProductDocument,
  "query Products($storeId: String!, $userId: String, $cultureName: String, $currencyCode: String, $query: String, $filter: String, $sort: String, $first: Int, $after: String) {\n  products(\n    storeId: $storeId\n    userId: $userId\n    cultureName: $cultureName\n    currencyCode: $currencyCode\n    query: $query\n    filter: $filter\n    sort: $sort\n    first: $first\n    after: $after\n  ) {\n    items {\n      ...Product\n    }\n  }\n}":
    types.ProductsDocument,
  "mutation CancelQuoteRequest($command: CancelQuoteCommandType!) {\n  cancelQuoteRequest(command: $command) {\n    ...Quote\n  }\n}":
    types.CancelQuoteRequestDocument,
  "mutation ChangeQuoteComment($command: ChangeQuoteCommentCommandType!) {\n  changeQuoteComment(command: $command) {\n    ...Quote\n  }\n}":
    types.ChangeQuoteCommentDocument,
  "mutation ChangeQuoteItemQuantity($command: ChangeQuoteItemQuantityCommandType!) {\n  changeQuoteItemQuantity(command: $command) {\n    ...Quote\n  }\n}":
    types.ChangeQuoteItemQuantityDocument,
  "mutation CreateQuoteFromCart($command: CreateQuoteFromCartCommandType!) {\n  createQuoteFromCart(command: $command) {\n    ...Quote\n  }\n}":
    types.CreateQuoteFromCartDocument,
  "mutation CreateQuote($command: CreateQuoteCommandType!) {\n  createQuote(command: $command) {\n    ...Quote\n  }\n}":
    types.CreateQuoteDocument,
  "query GetQuote($id: String!, $storeId: String, $userId: String, $cultureName: String, $currencyCode: String) {\n  quote(\n    id: $id\n    storeId: $storeId\n    userId: $userId\n    cultureName: $cultureName\n    currencyCode: $currencyCode\n  ) {\n    ...Quote\n    addresses {\n      ...QuoteAddress\n    }\n  }\n}":
    types.GetQuoteDocument,
  "mutation RemoveQuoteItem($command: RemoveQuoteItemCommandType!) {\n  removeQuoteItem(command: $command) {\n    ...Quote\n  }\n}":
    types.RemoveQuoteItemDocument,
  "mutation SubmitQuoteRequest($command: SubmitQuoteCommandType!) {\n  submitQuoteRequest(command: $command) {\n    ...Quote\n  }\n}":
    types.SubmitQuoteRequestDocument,
  "mutation UpdateQuoteAddresses($command: UpdateQuoteAddressesCommandType!) {\n  updateQuoteAddresses(command: $command) {\n    ...Quote\n    addresses {\n      ...QuoteAddress\n    }\n  }\n}":
    types.UpdateQuoteAddressesDocument,
  "query GetSavedForLater($storeId: String!, $userId: String!, $currencyCode: String, $cultureName: String) {\n  getSavedForLater(\n    storeId: $storeId\n    userId: $userId\n    currencyCode: $currencyCode\n    cultureName: $cultureName\n  ) {\n    ...Cart\n  }\n}":
    types.GetSavedForLaterDocument,
  "mutation MoveFromSavedForLater($command: InputSaveForLaterType!) {\n  moveFromSavedForLater(command: $command) {\n    ...CartWithList\n  }\n}":
    types.MoveFromSavedForLaterDocument,
  "mutation MoveToSavedForLater($command: InputSaveForLaterType!) {\n  moveToSavedForLater(command: $command) {\n    ...CartWithList\n  }\n}":
    types.MoveToSavedForLaterDocument,
  "query SlugInfo($storeId: String, $slug: String, $permalink: String, $userId: String, $cultureName: String) {\n  slugInfo(\n    storeId: $storeId\n    slug: $slug\n    permalink: $permalink\n    userId: $userId\n    cultureName: $cultureName\n  ) {\n    ...SlugInfo\n  }\n}":
    types.SlugInfoDocument,
  "mutation AddBulkItemToShoppingList($command: InputAddWishlistBulkItemType!) {\n  addWishlistBulkItem(command: $command) {\n    wishlists {\n      ...ShoppingList\n    }\n  }\n}":
    types.AddBulkItemToShoppingListDocument,
  "mutation AddItemsToShoppingList($command: InputAddWishlistItemsType!) {\n  addWishlistItems(command: $command) {\n    ...ShoppingList\n  }\n}":
    types.AddItemsToShoppingListDocument,
  "mutation ChangeShoppingList($command: InputChangeWishlistType!) {\n  changeWishlist(command: $command) {\n    ...ShoppingList\n  }\n}":
    types.ChangeShoppingListDocument,
  "mutation CreateShoppingList($command: InputCreateWishlistType!) {\n  createWishlist(command: $command) {\n    ...ShoppingList\n  }\n}":
    types.CreateShoppingListDocument,
  "mutation DeleteShoppingList($command: InputRemoveWishlistType!) {\n  removeWishlist(command: $command)\n}":
    types.DeleteShoppingListDocument,
  "query GetShoppingList($listId: String!, $cultureName: String) {\n  wishlist(listId: $listId, cultureName: $cultureName) {\n    ...ShoppingList\n  }\n}":
    types.GetShoppingListDocument,
  "query GetShoppingLists($storeId: String, $userId: String, $currencyCode: String, $cultureName: String) {\n  wishlists(\n    storeId: $storeId\n    userId: $userId\n    currencyCode: $currencyCode\n    cultureName: $cultureName\n  ) {\n    items {\n      ...ShoppingList\n    }\n  }\n}":
    types.GetShoppingListsDocument,
  "mutation RemoveItemsFromShoppingList($command: InputRemoveWishlistItemsType!) {\n  removeWishlistItems(command: $command) {\n    ...ShoppingList\n  }\n}":
    types.RemoveItemsFromShoppingListDocument,
  "mutation UpdateShoppingListItems($command: InputUpdateWishlistItemsType!) {\n  updateWishListItems(command: $command) {\n    ...ShoppingList\n  }\n}":
    types.UpdateShoppingListItemsDocument,
  "mutation DeleteUsers($command: InputDeleteUserType!) {\n  deleteUsers(command: $command) {\n    ...IdentityResult\n  }\n}":
    types.DeleteUsersDocument,
  "query GetMe {\n  me {\n    ...User\n  }\n}": types.GetMeDocument,
  "query GetUser($userName: String, $email: String, $id: String) {\n  user(userName: $userName, email: $email, id: $id) {\n    ...User\n  }\n}":
    types.GetUserDocument,
  "mutation InviteUser($command: InputInviteUserType!) {\n  inviteUser(command: $command) {\n    ...CustomIdentityResult\n  }\n}":
    types.InviteUserDocument,
  "mutation RegisterByInvitation($command: InputRegisterByInvitationType!) {\n  registerByInvitation(command: $command) {\n    ...CustomIdentityResult\n  }\n}":
    types.RegisterByInvitationDocument,
  "mutation ResetPasswordByToken($command: InputResetPasswordByTokenType!) {\n  resetPasswordByToken(command: $command) {\n    ...CustomIdentityResult\n  }\n}":
    types.ResetPasswordByTokenDocument,
  "mutation SendPasswordResetEmail($command: SendPasswordResetEmailCommandType!) {\n  sendPasswordResetEmail(command: $command)\n}":
    types.SendPasswordResetEmailDocument,
};

/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment CartAddress on CartAddressType {\n  id\n  key\n  city\n  countryCode\n  countryName\n  email\n  firstName\n  middleName\n  lastName\n  line1\n  line2\n  name\n  organization\n  phone\n  postalCode\n  regionId\n  regionName\n  zip\n  outerId\n  description\n  addressType\n}",
): typeof import("./graphql").CartAddressFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment CartConfigurationItem on CartConfigurationItemType {\n  id\n  sectionId\n  type\n  productId\n  name\n  sku\n  imageUrl\n  quantity\n  customText\n  selectedForCheckout\n}",
): typeof import("./graphql").CartConfigurationItemFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment CartWithList on CartWithListType {\n  cart {\n    ...Cart\n  }\n  list {\n    ...Cart\n  }\n}",
): typeof import("./graphql").CartWithListFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment Cart on CartType {\n  id\n  storeId\n  isAnonymous\n  hasPhysicalProducts\n  customerId\n  itemsCount\n  itemsQuantity\n  total {\n    ...Money\n  }\n  subTotal {\n    ...Money\n  }\n  subTotalDiscount {\n    ...Money\n  }\n  shippingTotal {\n    ...Money\n  }\n  items {\n    ...LineItem\n  }\n  payments {\n    ...Payment\n  }\n  shipments {\n    ...Shipment\n  }\n  coupons {\n    ...Coupon\n  }\n  gifts {\n    ...GiftItem\n  }\n  addresses {\n    ...CartAddress\n  }\n  validationErrors {\n    errorCode\n    errorMessage\n    errorParameters {\n      key\n      value\n    }\n    objectType\n    objectId\n  }\n}",
): typeof import("./graphql").CartFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment Category on Category {\n  id\n  code\n  name\n  outline\n  slug\n}",
): typeof import("./graphql").CategoryFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment ConfigurationLineItem on ConfigurationLineItemType {\n  id\n  text\n  quantity\n  product {\n    ...Product\n  }\n  listPrice {\n    ...Money\n  }\n  salePrice {\n    ...Money\n  }\n  extendedPrice {\n    ...Money\n  }\n  discountAmount {\n    ...Money\n  }\n}",
): typeof import("./graphql").ConfigurationLineItemFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment Contact on ContactType {\n  id\n  firstName\n  lastName\n  fullName\n  status\n  organizationId\n  organizationsIds\n  securityAccounts {\n    ...User\n  }\n}",
): typeof import("./graphql").ContactFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment Coupon on CouponType {\n  code\n  isAppliedSuccessfully\n}",
): typeof import("./graphql").CouponFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment Currency on CurrencyType {\n  code\n}",
): typeof import("./graphql").CurrencyFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment CustomIdentityResult on CustomIdentityResultType {\n  succeeded\n  errors {\n    code\n    parameter\n    description\n  }\n}",
): typeof import("./graphql").CustomIdentityResultFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment GiftItem on GiftItemType {\n  id\n  quantity\n  productId\n  name\n  lineItemId\n}",
): typeof import("./graphql").GiftItemFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment IdentityResult on IdentityResultType {\n  succeeded\n  errors {\n    code\n    description\n  }\n}",
): typeof import("./graphql").IdentityResultFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment Language on LanguageType {\n  cultureName\n  nativeName\n}",
): typeof import("./graphql").LanguageFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment LineItem on LineItemType {\n  id\n  sku\n  productId\n  name\n  quantity\n  listPrice {\n    ...Money\n  }\n  salePrice {\n    ...Money\n  }\n  placedPrice {\n    ...Money\n  }\n  extendedPrice {\n    ...Money\n  }\n  discountAmount {\n    ...Money\n  }\n  selectedForCheckout\n  isValid\n  validationErrors {\n    errorCode\n    errorMessage\n    errorParameters {\n      key\n      value\n    }\n    objectType\n    objectId\n  }\n  configurationItems {\n    ...CartConfigurationItem\n  }\n}",
): typeof import("./graphql").LineItemFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment MemberAddress on MemberAddressType {\n  id\n  key\n  isDefault\n  isFavorite\n  city\n  countryCode\n  countryName\n  email\n  firstName\n  middleName\n  lastName\n  line1\n  line2\n  name\n  organization\n  phone\n  postalCode\n  regionId\n  regionName\n  zip\n  outerId\n  description\n  addressType\n}",
): typeof import("./graphql").MemberAddressFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment MenuLink on MenuLinkType {\n  title\n  url\n  priority\n}",
): typeof import("./graphql").MenuLinkFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment Money on MoneyType {\n  amount\n  formattedAmount\n}",
): typeof import("./graphql").MoneyFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment OrderLineItem on OrderLineItemType {\n  id\n  name\n  sku\n  productId\n  quantity\n  price {\n    ...Money\n  }\n  extendedPrice {\n    ...Money\n  }\n}",
): typeof import("./graphql").OrderLineItemFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment OrderPayment on PaymentInType {\n  id\n  number\n  gatewayCode\n  status\n  sum {\n    ...Money\n  }\n}",
): typeof import("./graphql").OrderPaymentFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment OrderShipment on OrderShipmentType {\n  id\n  number\n  shipmentMethodCode\n  shipmentMethodOption\n  status\n  total {\n    ...Money\n  }\n}",
): typeof import("./graphql").OrderShipmentFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment Order on CustomerOrderType {\n  id\n  number\n  status\n  createdDate\n  total {\n    ...Money\n  }\n  items {\n    ...OrderLineItem\n  }\n  inPayments {\n    ...OrderPayment\n  }\n  shipments {\n    ...OrderShipment\n  }\n}",
): typeof import("./graphql").OrderFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment PageContext on PageContextResponseType {\n  slugInfo {\n    ...SlugInfo\n  }\n  store {\n    ...StoreInfo\n  }\n  whiteLabelingSettings {\n    ...WhiteLabelingSettings\n  }\n  user {\n    ...User\n  }\n}",
): typeof import("./graphql").PageContextFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment Payment on PaymentType {\n  id\n  outerId\n  paymentGatewayCode\n  currency {\n    ...Currency\n  }\n  total {\n    ...Money\n  }\n  billingAddress {\n    ...CartAddress\n  }\n}",
): typeof import("./graphql").PaymentFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment PickupAddress on PickupAddressType {\n  id\n  key\n  name\n  organization\n  countryCode\n  countryName\n  city\n  postalCode\n  line1\n  line2\n  regionId\n  regionName\n  phone\n  email\n  outerId\n  description\n  addressType\n}",
): typeof import("./graphql").PickupAddressFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment PickupLocationAddress on PickupLocationAddressType {\n  id\n  key\n  name\n  organization\n  countryCode\n  countryName\n  city\n  postalCode\n  line1\n  line2\n  regionId\n  regionName\n  phone\n  email\n  outerId\n  description\n  addressType\n}",
): typeof import("./graphql").PickupLocationAddressFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment PickupLocation on PickupLocationType {\n  id\n  isActive\n  name\n  description\n  contactEmail\n  contactPhone\n  workingHours\n  geoLocation\n  address {\n    ...PickupAddress\n  }\n}",
): typeof import("./graphql").PickupLocationFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment ProductConfiguration on ConfigurationQueryResponseType {\n  configurationSections {\n    id\n    name\n    description\n    isRequired\n    type\n    allowCustomText\n    allowTextOptions\n    maxLength\n    options {\n      ...ConfigurationLineItem\n    }\n  }\n}",
): typeof import("./graphql").ProductConfigurationFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment ProductPickupLocation on ProductPickupLocation {\n  id\n  isActive\n  name\n  description\n  contactEmail\n  contactPhone\n  workingHours\n  deliveryDays\n  storageDays\n  geoLocation\n  address {\n    ...PickupLocationAddress\n  }\n  availabilityType\n  availabilityNote\n  availableQuantity\n}",
): typeof import("./graphql").ProductPickupLocationFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment ProductPrice on PriceType {\n  list {\n    ...Money\n  }\n  actual {\n    ...Money\n  }\n}",
): typeof import("./graphql").ProductPriceFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment Product on Product {\n  id\n  code\n  productType\n  isConfigurable\n  name\n  vendor {\n    ...Vendor\n  }\n  price {\n    ...ProductPrice\n  }\n}",
): typeof import("./graphql").ProductFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment QuoteAddress on QuoteAddressType {\n  addressType\n  city\n  countryCode\n  countryName\n  line1\n  postalCode\n  regionId\n  regionName\n}",
): typeof import("./graphql").QuoteAddressFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment QuoteItem on QuoteItemType {\n  id\n  name\n  sku\n  productId\n  quantity\n  listPrice {\n    ...Money\n  }\n  salePrice {\n    ...Money\n  }\n  proposalPrices {\n    quantity\n    price {\n      ...Money\n    }\n  }\n}",
): typeof import("./graphql").QuoteItemFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment QuoteTotals on QuoteTotalsType {\n  originalSubTotalExlTax {\n    ...Money\n  }\n  subTotalExlTax {\n    ...Money\n  }\n  shippingTotal {\n    ...Money\n  }\n  discountTotal {\n    ...Money\n  }\n  taxTotal {\n    ...Money\n  }\n  grandTotalExlTax {\n    ...Money\n  }\n  grandTotalInclTax {\n    ...Money\n  }\n}",
): typeof import("./graphql").QuoteTotalsFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment Quote on QuoteType {\n  id\n  number\n  status\n  storeId\n  customerId\n  comment\n  isAnonymous\n  isCancelled\n  totals {\n    ...QuoteTotals\n  }\n  items {\n    ...QuoteItem\n  }\n}",
): typeof import("./graphql").QuoteFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment Role on RoleType {\n  id\n  name\n  normalizedName\n}",
): typeof import("./graphql").RoleFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment SeoInfo on SeoInfo {\n  id\n  name\n  semanticUrl\n  outline\n  pageTitle\n  metaDescription\n  imageAltDescription\n  metaKeywords\n  storeId\n  objectId\n  objectType\n  isActive\n  languageCode\n}",
): typeof import("./graphql").SeoInfoFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment Shipment on ShipmentType {\n  id\n  shipmentMethodCode\n  shipmentMethodOption\n  fulfillmentCenterId\n  price {\n    ...Money\n  }\n  currency {\n    ...Currency\n  }\n  deliveryAddress {\n    ...CartAddress\n  }\n}",
): typeof import("./graphql").ShipmentFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment ShoppingList on WishlistType {\n  id\n  name\n  storeId\n  customerId\n  customerName\n  items {\n    ...WishlistLineItem\n  }\n  itemsCount\n  description\n  subTotal {\n    ...Money\n  }\n  sharingSetting {\n    id\n    scope\n  }\n}",
): typeof import("./graphql").ShoppingListFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment SlugInfo on SlugInfoResponseType {\n  entityInfo {\n    ...SeoInfo\n  }\n  redirectUrl\n}",
): typeof import("./graphql").SlugInfoFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment StoreInfo on StoreResponseType {\n  storeId\n  storeName\n  catalogId\n  storeUrl\n  defaultLanguage {\n    ...Language\n  }\n  availableLanguages {\n    ...Language\n  }\n  defaultCurrency {\n    ...Currency\n  }\n  availableCurrencies {\n    ...Currency\n  }\n  settings {\n    ...StoreSettings\n  }\n}",
): typeof import("./graphql").StoreInfoFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment StoreSettings on StoreSettingsType {\n  anonymousUsersAllowed\n  taxCalculationEnabled\n  seoLinkType\n}",
): typeof import("./graphql").StoreSettingsFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment User on UserType {\n  id\n  userName\n  email\n  emailConfirmed\n  isAdministrator\n  memberId\n  storeId\n  roles {\n    ...Role\n  }\n}",
): typeof import("./graphql").UserFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment Vendor on CommonVendor {\n  id\n  name\n}",
): typeof import("./graphql").VendorFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment WhiteLabelingSettings on WhiteLabelingSettingsType {\n  logoUrl\n  secondaryLogoUrl\n  faviconUrl\n  themePresetName\n  footerLinks {\n    ...MenuLink\n  }\n  mainMenuLinks {\n    ...MenuLink\n  }\n}",
): typeof import("./graphql").WhiteLabelingSettingsFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "fragment WishlistLineItem on LineItemType {\n  id\n  sku\n  productId\n  name\n  quantity\n}",
): typeof import("./graphql").WishlistLineItemFragmentDoc;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation AddBulkItemsCart($command: InputAddBulkItemsType!) {\n  addBulkItemsCart(command: $command) {\n    cart {\n      ...Cart\n    }\n    errors {\n      errorCode\n      errorMessage\n      objectId\n    }\n  }\n}",
): typeof import("./graphql").AddBulkItemsCartDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation AddCoupon($command: InputAddCouponType!) {\n  addCoupon(command: $command) {\n    ...Cart\n  }\n}",
): typeof import("./graphql").AddCouponDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation AddItem($command: InputAddItemType!) {\n  addItem(command: $command) {\n    ...Cart\n  }\n}",
): typeof import("./graphql").AddItemDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation AddItemsCart($command: InputAddItemsType!) {\n  addItemsCart(command: $command) {\n    ...Cart\n  }\n}",
): typeof import("./graphql").AddItemsCartDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation AddOrUpdateCartPayment($command: InputAddOrUpdateCartPaymentType!) {\n  addOrUpdateCartPayment(command: $command) {\n    ...Cart\n  }\n}",
): typeof import("./graphql").AddOrUpdateCartPaymentDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation AddOrUpdateCartShipment($command: InputAddOrUpdateCartShipmentType!) {\n  addOrUpdateCartShipment(command: $command) {\n    ...Cart\n  }\n}",
): typeof import("./graphql").AddOrUpdateCartShipmentDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation ChangeCartConfiguredItem($command: InputChangeCartConfiguredItemType!) {\n  changeCartConfiguredItem(command: $command) {\n    ...Cart\n  }\n}",
): typeof import("./graphql").ChangeCartConfiguredItemDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation ClearCart($command: InputClearCartType!) {\n  clearCart(command: $command) {\n    ...Cart\n  }\n}",
): typeof import("./graphql").ClearCartDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation CreateOrderFromCart($command: InputCreateOrderFromCartType!) {\n  createOrderFromCart(command: $command) {\n    ...Order\n  }\n}",
): typeof import("./graphql").CreateOrderFromCartDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query GetCartLineValidation($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String!, $cartId: String) {\n  cart(\n    storeId: $storeId\n    userId: $userId\n    currencyCode: $currencyCode\n    cultureName: $cultureName\n    cartId: $cartId\n  ) {\n    itemsCount\n    items {\n      id\n      sku\n      productId\n      quantity\n      isValid\n      validationErrors {\n        errorCode\n        objectType\n        objectId\n        errorMessage\n      }\n    }\n  }\n}",
): typeof import("./graphql").GetCartLineValidationDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query GetCartValidationAliased($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String!, $ruleSetA: String, $ruleSetB: String, $cartId: String) {\n  cart(\n    storeId: $storeId\n    userId: $userId\n    currencyCode: $currencyCode\n    cultureName: $cultureName\n    cartId: $cartId\n  ) {\n    itemsCount\n    errorsA: validationErrors(ruleSet: $ruleSetA) {\n      errorCode\n      objectType\n      objectId\n      errorMessage\n    }\n    errorsB: validationErrors(ruleSet: $ruleSetB) {\n      errorCode\n      objectType\n      objectId\n      errorMessage\n    }\n  }\n}",
): typeof import("./graphql").GetCartValidationAliasedDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query GetCartValidation($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String!, $ruleSet: String, $cartId: String) {\n  cart(\n    storeId: $storeId\n    userId: $userId\n    currencyCode: $currencyCode\n    cultureName: $cultureName\n    cartId: $cartId\n  ) {\n    itemsCount\n    validationErrors(ruleSet: $ruleSet) {\n      errorCode\n      objectType\n      objectId\n      errorMessage\n    }\n    items {\n      id\n      sku\n      productId\n      quantity\n      isValid\n      validationErrors {\n        errorCode\n        objectType\n        objectId\n        errorMessage\n      }\n    }\n  }\n}",
): typeof import("./graphql").GetCartValidationDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query GetCart($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String!, $cartId: String, $cartName: String) {\n  cart(\n    storeId: $storeId\n    userId: $userId\n    currencyCode: $currencyCode\n    cultureName: $cultureName\n    cartId: $cartId\n    cartName: $cartName\n  ) {\n    ...Cart\n  }\n}",
): typeof import("./graphql").GetCartDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation MergeCart($command: InputMergeCartType!) {\n  mergeCart(command: $command) {\n    ...Cart\n  }\n}",
): typeof import("./graphql").MergeCartDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation RemoveCartItem($command: InputRemoveItemType!) {\n  removeCartItem(command: $command) {\n    ...Cart\n  }\n}",
): typeof import("./graphql").RemoveCartItemDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation RemoveCart($command: InputRemoveCartType!) {\n  removeCart(command: $command)\n}",
): typeof import("./graphql").RemoveCartDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation RemoveCoupon($command: InputRemoveCouponType!) {\n  removeCoupon(command: $command) {\n    ...Cart\n  }\n}",
): typeof import("./graphql").RemoveCouponDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation SelectCartItems($command: InputChangeCartItemsSelectedType!) {\n  selectCartItems(command: $command) {\n    ...Cart\n  }\n}",
): typeof import("./graphql").SelectCartItemsDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation UnSelectAllCartItems($command: InputChangeAllCartItemsSelectedType!) {\n  unSelectAllCartItems(command: $command) {\n    ...Cart\n  }\n}",
): typeof import("./graphql").UnSelectAllCartItemsDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation UnSelectCartItems($command: InputChangeCartItemsSelectedType!) {\n  unSelectCartItems(command: $command) {\n    ...Cart\n  }\n}",
): typeof import("./graphql").UnSelectCartItemsDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation UpdateCartQuantity($command: InputUpdateCartQuantity!) {\n  updateCartQuantity(command: $command) {\n    ...Cart\n  }\n}",
): typeof import("./graphql").UpdateCartQuantityDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query Categories($storeId: String!, $userId: String, $cultureName: String, $currencyCode: String, $filter: String, $first: Int) {\n  categories(\n    storeId: $storeId\n    userId: $userId\n    cultureName: $cultureName\n    currencyCode: $currencyCode\n    filter: $filter\n    first: $first\n  ) {\n    totalCount\n    items {\n      ...Category\n    }\n  }\n}",
): typeof import("./graphql").CategoriesDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query Category($id: String!, $storeId: String!, $userId: String, $cultureName: String, $currencyCode: String) {\n  category(\n    id: $id\n    storeId: $storeId\n    userId: $userId\n    cultureName: $cultureName\n    currencyCode: $currencyCode\n  ) {\n    ...Category\n  }\n}",
): typeof import("./graphql").CategoryDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation AddAddressToFavorites($command: AddAddressToFavoritesCommandType!) {\n  addAddressToFavorites(command: $command)\n}",
): typeof import("./graphql").AddAddressToFavoritesDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation ChangeOrganizationContactRole($command: InputChangeOrganizationContactRoleType!) {\n  changeOrganizationContactRole(command: $command) {\n    ...CustomIdentityResult\n  }\n}",
): typeof import("./graphql").ChangeOrganizationContactRoleDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation DeleteContact($command: InputDeleteContactType!) {\n  deleteContact(command: $command)\n}",
): typeof import("./graphql").DeleteContactDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation DeleteMemberAddresses($command: InputDeleteMemberAddressType!) {\n  deleteMemberAddresses(command: $command) {\n    addresses {\n      items {\n        ...MemberAddress\n      }\n    }\n  }\n}",
): typeof import("./graphql").DeleteMemberAddressesDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query GetContactAddresses($id: String!) {\n  contact(id: $id) {\n    addresses {\n      items {\n        ...MemberAddress\n      }\n    }\n  }\n}",
): typeof import("./graphql").GetContactAddressesDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query GetContactLockStatus($id: String!) {\n  contact(id: $id) {\n    isLockedInOrganization\n  }\n}",
): typeof import("./graphql").GetContactLockStatusDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query GetContactRolesInOrganization($id: String!) {\n  contact(id: $id) {\n    rolesInOrganization {\n      id\n      name\n    }\n  }\n}",
): typeof import("./graphql").GetContactRolesInOrganizationDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query GetContact($id: String!) {\n  contact(id: $id) {\n    ...Contact\n  }\n}",
): typeof import("./graphql").GetContactDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query GetCurrentCustomerAddresses($after: String, $first: Int, $countryCodes: [String], $regionIds: [String], $cities: [String], $keyword: String, $sort: String) {\n  currentCustomerAddresses(\n    after: $after\n    first: $first\n    countryCodes: $countryCodes\n    regionIds: $regionIds\n    cities: $cities\n    keyword: $keyword\n    sort: $sort\n  ) {\n    totalCount\n    items {\n      ...MemberAddress\n    }\n  }\n}",
): typeof import("./graphql").GetCurrentCustomerAddressesDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query GetCurrentOrganizationAddresses($after: String, $first: Int, $countryCodes: [String], $regionIds: [String], $cities: [String], $keyword: String, $sort: String) {\n  currentOrganizationAddresses(\n    after: $after\n    first: $first\n    countryCodes: $countryCodes\n    regionIds: $regionIds\n    cities: $cities\n    keyword: $keyword\n    sort: $sort\n  ) {\n    totalCount\n    items {\n      ...MemberAddress\n    }\n  }\n}",
): typeof import("./graphql").GetCurrentOrganizationAddressesDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query GetOrganizationContacts($organizationId: String!, $searchPhrase: String, $sort: String, $first: Int, $after: String) {\n  organization(id: $organizationId) {\n    contacts(searchPhrase: $searchPhrase, sort: $sort, first: $first, after: $after) {\n      items {\n        ...Contact\n      }\n    }\n  }\n}",
): typeof import("./graphql").GetOrganizationContactsDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query GetOrganizations($after: String, $first: Int, $sort: String, $searchPhrase: String, $statuses: [String]) {\n  me {\n    contact {\n      organizations(\n        after: $after\n        first: $first\n        sort: $sort\n        searchPhrase: $searchPhrase\n        statuses: $statuses\n      ) {\n        items {\n          id\n          name\n          isLockedForCurrentUser\n        }\n        totalCount\n        pageInfo {\n          hasNextPage\n          endCursor\n        }\n      }\n    }\n  }\n}",
): typeof import("./graphql").GetOrganizationsDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation LockOrganizationContact($command: InputLockUnlockOrganizationContactType!) {\n  lockOrganizationContact(command: $command) {\n    ...Contact\n  }\n}",
): typeof import("./graphql").LockOrganizationContactDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation RemoveAddressFromFavorites($command: RemoveAddressFromFavoritesCommandType!) {\n  removeAddressFromFavorites(command: $command)\n}",
): typeof import("./graphql").RemoveAddressFromFavoritesDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation RequestRegistration($command: InputRequestRegistrationType!) {\n  requestRegistration(command: $command) {\n    contact {\n      id\n      firstName\n      lastName\n      status\n    }\n    organization {\n      id\n      name\n      status\n      ownerId\n    }\n    account {\n      id\n      username\n      email\n      status\n    }\n    result {\n      succeeded\n      requireEmailVerification\n    }\n  }\n}",
): typeof import("./graphql").RequestRegistrationDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation UnlockOrganizationContact($command: InputLockUnlockOrganizationContactType!) {\n  unlockOrganizationContact(command: $command) {\n    ...Contact\n  }\n}",
): typeof import("./graphql").UnlockOrganizationContactDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation UpdateMemberAddresses($command: InputUpdateMemberAddressType!) {\n  updateMemberAddresses(command: $command) {\n    addresses {\n      items {\n        ...MemberAddress\n      }\n    }\n  }\n}",
): typeof import("./graphql").UpdateMemberAddressesDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query Order($number: String, $cultureName: String) {\n  order(number: $number, cultureName: $cultureName) {\n    ...Order\n  }\n}",
): typeof import("./graphql").OrderDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query Orders($userId: String, $filter: String, $sort: String, $cultureName: String, $first: Int, $after: String) {\n  orders(\n    userId: $userId\n    filter: $filter\n    sort: $sort\n    cultureName: $cultureName\n    first: $first\n    after: $after\n  ) {\n    items {\n      ...Order\n    }\n  }\n}",
): typeof import("./graphql").OrdersDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query OrganizationOrders($organizationId: String, $filter: String, $sort: String, $cultureName: String, $first: Int, $after: String) {\n  organizationOrders(\n    organizationId: $organizationId\n    filter: $filter\n    sort: $sort\n    cultureName: $cultureName\n    first: $first\n    after: $after\n  ) {\n    items {\n      ...Order\n    }\n  }\n}",
): typeof import("./graphql").OrganizationOrdersDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query PageContext($storeId: String, $userId: String, $cultureName: String, $permalink: String, $organizationId: String) {\n  pageContext(\n    storeId: $storeId\n    userId: $userId\n    cultureName: $cultureName\n    permalink: $permalink\n    organizationId: $organizationId\n  ) {\n    ...PageContext\n  }\n}",
): typeof import("./graphql").PageContextDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query CartPickupLocations($cartId: String!, $storeId: String!, $cultureName: String!, $keyword: String, $sort: String, $first: Int, $after: String, $facet: String, $filter: String) {\n  cartPickupLocations(\n    cartId: $cartId\n    storeId: $storeId\n    cultureName: $cultureName\n    keyword: $keyword\n    sort: $sort\n    first: $first\n    after: $after\n    facet: $facet\n    filter: $filter\n  ) {\n    items {\n      ...ProductPickupLocation\n    }\n  }\n}",
): typeof import("./graphql").CartPickupLocationsDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query PickupLocations($storeId: String, $keyword: String, $sort: String, $first: Int, $after: String) {\n  pickupLocations(\n    storeId: $storeId\n    keyword: $keyword\n    sort: $sort\n    first: $first\n    after: $after\n  ) {\n    items {\n      ...PickupLocation\n    }\n  }\n}",
): typeof import("./graphql").PickupLocationsDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query ProductPickupLocations($productId: String!, $storeId: String!, $cultureName: String!, $keyword: String, $sort: String, $first: Int, $after: String) {\n  productPickupLocations(\n    productId: $productId\n    storeId: $storeId\n    cultureName: $cultureName\n    keyword: $keyword\n    sort: $sort\n    first: $first\n    after: $after\n  ) {\n    items {\n      ...ProductPickupLocation\n    }\n  }\n}",
): typeof import("./graphql").ProductPickupLocationsDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation CreateConfiguredLineItem($command: InputCreateConfiguredLineItemCommand!) {\n  createConfiguredLineItem(command: $command) {\n    ...ConfigurationLineItem\n  }\n}",
): typeof import("./graphql").CreateConfiguredLineItemDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query ProductConfiguration($configurableProductId: String!, $storeId: String!, $userId: String, $cultureName: String, $currencyCode: String) {\n  productConfiguration(\n    configurableProductId: $configurableProductId\n    storeId: $storeId\n    userId: $userId\n    cultureName: $cultureName\n    currencyCode: $currencyCode\n  ) {\n    ...ProductConfiguration\n  }\n}",
): typeof import("./graphql").ProductConfigurationDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query Product($id: String!, $storeId: String!, $userId: String, $cultureName: String, $currencyCode: String) {\n  product(\n    id: $id\n    storeId: $storeId\n    userId: $userId\n    cultureName: $cultureName\n    currencyCode: $currencyCode\n  ) {\n    ...Product\n  }\n}",
): typeof import("./graphql").ProductDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query Products($storeId: String!, $userId: String, $cultureName: String, $currencyCode: String, $query: String, $filter: String, $sort: String, $first: Int, $after: String) {\n  products(\n    storeId: $storeId\n    userId: $userId\n    cultureName: $cultureName\n    currencyCode: $currencyCode\n    query: $query\n    filter: $filter\n    sort: $sort\n    first: $first\n    after: $after\n  ) {\n    items {\n      ...Product\n    }\n  }\n}",
): typeof import("./graphql").ProductsDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation CancelQuoteRequest($command: CancelQuoteCommandType!) {\n  cancelQuoteRequest(command: $command) {\n    ...Quote\n  }\n}",
): typeof import("./graphql").CancelQuoteRequestDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation ChangeQuoteComment($command: ChangeQuoteCommentCommandType!) {\n  changeQuoteComment(command: $command) {\n    ...Quote\n  }\n}",
): typeof import("./graphql").ChangeQuoteCommentDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation ChangeQuoteItemQuantity($command: ChangeQuoteItemQuantityCommandType!) {\n  changeQuoteItemQuantity(command: $command) {\n    ...Quote\n  }\n}",
): typeof import("./graphql").ChangeQuoteItemQuantityDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation CreateQuoteFromCart($command: CreateQuoteFromCartCommandType!) {\n  createQuoteFromCart(command: $command) {\n    ...Quote\n  }\n}",
): typeof import("./graphql").CreateQuoteFromCartDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation CreateQuote($command: CreateQuoteCommandType!) {\n  createQuote(command: $command) {\n    ...Quote\n  }\n}",
): typeof import("./graphql").CreateQuoteDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query GetQuote($id: String!, $storeId: String, $userId: String, $cultureName: String, $currencyCode: String) {\n  quote(\n    id: $id\n    storeId: $storeId\n    userId: $userId\n    cultureName: $cultureName\n    currencyCode: $currencyCode\n  ) {\n    ...Quote\n    addresses {\n      ...QuoteAddress\n    }\n  }\n}",
): typeof import("./graphql").GetQuoteDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation RemoveQuoteItem($command: RemoveQuoteItemCommandType!) {\n  removeQuoteItem(command: $command) {\n    ...Quote\n  }\n}",
): typeof import("./graphql").RemoveQuoteItemDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation SubmitQuoteRequest($command: SubmitQuoteCommandType!) {\n  submitQuoteRequest(command: $command) {\n    ...Quote\n  }\n}",
): typeof import("./graphql").SubmitQuoteRequestDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation UpdateQuoteAddresses($command: UpdateQuoteAddressesCommandType!) {\n  updateQuoteAddresses(command: $command) {\n    ...Quote\n    addresses {\n      ...QuoteAddress\n    }\n  }\n}",
): typeof import("./graphql").UpdateQuoteAddressesDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query GetSavedForLater($storeId: String!, $userId: String!, $currencyCode: String, $cultureName: String) {\n  getSavedForLater(\n    storeId: $storeId\n    userId: $userId\n    currencyCode: $currencyCode\n    cultureName: $cultureName\n  ) {\n    ...Cart\n  }\n}",
): typeof import("./graphql").GetSavedForLaterDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation MoveFromSavedForLater($command: InputSaveForLaterType!) {\n  moveFromSavedForLater(command: $command) {\n    ...CartWithList\n  }\n}",
): typeof import("./graphql").MoveFromSavedForLaterDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation MoveToSavedForLater($command: InputSaveForLaterType!) {\n  moveToSavedForLater(command: $command) {\n    ...CartWithList\n  }\n}",
): typeof import("./graphql").MoveToSavedForLaterDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query SlugInfo($storeId: String, $slug: String, $permalink: String, $userId: String, $cultureName: String) {\n  slugInfo(\n    storeId: $storeId\n    slug: $slug\n    permalink: $permalink\n    userId: $userId\n    cultureName: $cultureName\n  ) {\n    ...SlugInfo\n  }\n}",
): typeof import("./graphql").SlugInfoDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation AddBulkItemToShoppingList($command: InputAddWishlistBulkItemType!) {\n  addWishlistBulkItem(command: $command) {\n    wishlists {\n      ...ShoppingList\n    }\n  }\n}",
): typeof import("./graphql").AddBulkItemToShoppingListDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation AddItemsToShoppingList($command: InputAddWishlistItemsType!) {\n  addWishlistItems(command: $command) {\n    ...ShoppingList\n  }\n}",
): typeof import("./graphql").AddItemsToShoppingListDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation ChangeShoppingList($command: InputChangeWishlistType!) {\n  changeWishlist(command: $command) {\n    ...ShoppingList\n  }\n}",
): typeof import("./graphql").ChangeShoppingListDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation CreateShoppingList($command: InputCreateWishlistType!) {\n  createWishlist(command: $command) {\n    ...ShoppingList\n  }\n}",
): typeof import("./graphql").CreateShoppingListDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation DeleteShoppingList($command: InputRemoveWishlistType!) {\n  removeWishlist(command: $command)\n}",
): typeof import("./graphql").DeleteShoppingListDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query GetShoppingList($listId: String!, $cultureName: String) {\n  wishlist(listId: $listId, cultureName: $cultureName) {\n    ...ShoppingList\n  }\n}",
): typeof import("./graphql").GetShoppingListDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query GetShoppingLists($storeId: String, $userId: String, $currencyCode: String, $cultureName: String) {\n  wishlists(\n    storeId: $storeId\n    userId: $userId\n    currencyCode: $currencyCode\n    cultureName: $cultureName\n  ) {\n    items {\n      ...ShoppingList\n    }\n  }\n}",
): typeof import("./graphql").GetShoppingListsDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation RemoveItemsFromShoppingList($command: InputRemoveWishlistItemsType!) {\n  removeWishlistItems(command: $command) {\n    ...ShoppingList\n  }\n}",
): typeof import("./graphql").RemoveItemsFromShoppingListDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation UpdateShoppingListItems($command: InputUpdateWishlistItemsType!) {\n  updateWishListItems(command: $command) {\n    ...ShoppingList\n  }\n}",
): typeof import("./graphql").UpdateShoppingListItemsDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation DeleteUsers($command: InputDeleteUserType!) {\n  deleteUsers(command: $command) {\n    ...IdentityResult\n  }\n}",
): typeof import("./graphql").DeleteUsersDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(source: "query GetMe {\n  me {\n    ...User\n  }\n}"): typeof import("./graphql").GetMeDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "query GetUser($userName: String, $email: String, $id: String) {\n  user(userName: $userName, email: $email, id: $id) {\n    ...User\n  }\n}",
): typeof import("./graphql").GetUserDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation InviteUser($command: InputInviteUserType!) {\n  inviteUser(command: $command) {\n    ...CustomIdentityResult\n  }\n}",
): typeof import("./graphql").InviteUserDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation RegisterByInvitation($command: InputRegisterByInvitationType!) {\n  registerByInvitation(command: $command) {\n    ...CustomIdentityResult\n  }\n}",
): typeof import("./graphql").RegisterByInvitationDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation ResetPasswordByToken($command: InputResetPasswordByTokenType!) {\n  resetPasswordByToken(command: $command) {\n    ...CustomIdentityResult\n  }\n}",
): typeof import("./graphql").ResetPasswordByTokenDocument;
/**
 * The graphql function is used to parse GraphQL queries into a document that can be used by GraphQL clients.
 */
export function graphql(
  source: "mutation SendPasswordResetEmail($command: SendPasswordResetEmailCommandType!) {\n  sendPasswordResetEmail(command: $command)\n}",
): typeof import("./graphql").SendPasswordResetEmailDocument;

export function graphql(source: string) {
  return (documents as any)[source] ?? {};
}
