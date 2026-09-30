/* eslint-disable */
/* tslint:disable */
// @ts-nocheck
/*
 * ---------------------------------------------------------------
 * ## THIS FILE WAS GENERATED VIA SWAGGER-TYPESCRIPT-API        ##
 * ##                                                           ##
 * ## AUTHOR: acacode                                           ##
 * ## SOURCE: https://github.com/acacode/swagger-typescript-api ##
 * ---------------------------------------------------------------
 */

export interface AssetEntrySearchCriteria {
  group?: string | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
  tenants?: VirtoCommercePlatformCoreCommonTenantIdentity[] | null;
}

export interface CartAddress {
  line1?: string | null;
  line2?: string | null;
  addressType?: VirtoCommerceCoreModuleCoreCommonAddressType;
  city?: string | null;
  countryCode?: string | null;
  countryName?: string | null;
  description?: string | null;
  email?: string | null;
  firstName?: string | null;
  isDefault?: boolean;
  key?: string | null;
  lastName?: string | null;
  middleName?: string | null;
  name?: string | null;
  organization?: string | null;
  outerId?: string | null;
  phone?: string | null;
  postalCode?: string | null;
  regionId?: string | null;
  regionName?: string | null;
  zip?: string | null;
}

export interface CartConfigurationItem {
  catalogId?: string | null;
  categoryId?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  customText?: string | null;
  /** @format double */
  readonly extendedPrice?: number;
  files?: CartConfigurationItemFile[] | null;
  id?: string | null;
  imageUrl?: string | null;
  lineItemId?: string | null;
  /** @format double */
  listPrice?: number;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  productId?: string | null;
  /** @format int32 */
  quantity?: number;
  /** @format double */
  salePrice?: number;
  sectionId?: string | null;
  sectionName?: string | null;
  selectedForCheckout?: boolean;
  sku?: string | null;
  type?: string | null;
}

export interface CartConfigurationItemFile {
  contentType?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  /** @format int64 */
  size?: number;
  url?: string | null;
}

export interface CartLineItem {
  catalogId?: string | null;
  categoryId?: string | null;
  configurationItems?: CartConfigurationItem[] | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  currency?: string | null;
  /** @format double */
  discountAmount?: number;
  /** @format double */
  discountAmountWithTax?: number;
  /** @format double */
  discountTotal?: number;
  /** @format double */
  discountTotalWithTax?: number;
  discounts?: VirtoCommerceCoreModuleCoreCommonDiscount[] | null;
  dynamicProperties?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicObjectProperty[]
    | null;
  /** @format double */
  extendedPrice?: number;
  /** @format double */
  extendedPriceWithTax?: number;
  /** @format double */
  fee?: number;
  /** @format double */
  feeWithTax?: number;
  fulfillmentCenterId?: string | null;
  fulfillmentCenterName?: string | null;
  fulfillmentLocationCode?: string | null;
  /** @format double */
  height?: number | null;
  id?: string | null;
  imageUrl?: string | null;
  isConfigured?: boolean;
  isDiscountAmountRounded?: boolean;
  isGift?: boolean;
  isReadOnly?: boolean;
  isReccuring?: boolean;
  isRejected?: boolean;
  languageCode?: string | null;
  /** @format double */
  length?: number | null;
  /** @format double */
  listPrice?: number;
  /** @format double */
  listPriceWithTax?: number;
  /** @format double */
  listTotal?: number;
  /** @format double */
  listTotalWithTax?: number;
  measureUnit?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  note?: string | null;
  readonly objectType?: string | null;
  /** @format double */
  placedPrice?: number;
  /** @format double */
  placedPriceWithTax?: number;
  priceId?: string | null;
  productId?: string | null;
  productOuterId?: string | null;
  productType?: string | null;
  /** @format int32 */
  quantity?: number;
  requiredShipping?: boolean;
  /** @format double */
  salePrice?: number;
  /** @format double */
  salePriceWithTax?: number;
  selectedForCheckout?: boolean;
  shipmentMethodCode?: string | null;
  sku?: string | null;
  taxDetails?: VirtoCommerceCoreModuleCoreTaxTaxDetail[] | null;
  taxIncluded?: boolean;
  /** @format double */
  taxPercentRate?: number;
  /** @format double */
  taxTotal?: number;
  taxType?: string | null;
  thumbnailImageUrl?: string | null;
  validationType?: string | null;
  vendorId?: string | null;
  /** @format double */
  volumetricWeight?: number | null;
  /** @format double */
  weight?: number | null;
  weightUnit?: string | null;
  /** @format double */
  width?: number | null;
}

export interface CartShipment {
  comment?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  currency?: string | null;
  deliveryAddress?: CartAddress | null;
  /** @format double */
  discountAmount?: number;
  /** @format double */
  discountAmountWithTax?: number;
  discounts?: VirtoCommerceCoreModuleCoreCommonDiscount[] | null;
  dynamicProperties?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicObjectProperty[]
    | null;
  /** @format double */
  fee?: number;
  /** @format double */
  feeWithTax?: number;
  fulfillmentCenterId?: string | null;
  fulfillmentCenterName?: string | null;
  /** @format double */
  height?: number | null;
  id?: string | null;
  items?: CartShipmentItem[] | null;
  /** @format double */
  length?: number | null;
  measureUnit?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  readonly objectType?: string | null;
  pickupLocationId?: string | null;
  /** @format double */
  price?: number;
  /** @format double */
  priceWithTax?: number;
  shipmentMethodCode?: string | null;
  shipmentMethodOption?: string | null;
  taxDetails?: VirtoCommerceCoreModuleCoreTaxTaxDetail[] | null;
  /** @format double */
  taxPercentRate?: number;
  /** @format double */
  taxTotal?: number;
  taxType?: string | null;
  /** @format double */
  total?: number;
  /** @format double */
  totalWithTax?: number;
  vendorId?: string | null;
  /** @format double */
  volumetricWeight?: number | null;
  warehouseLocation?: string | null;
  /** @format double */
  weight?: number | null;
  weightUnit?: string | null;
  /** @format double */
  width?: number | null;
}

export interface CartShipmentItem {
  barCode?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  lineItem?: CartLineItem | null;
  lineItemId?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  /** @format int32 */
  quantity?: number;
}

/** Notification for catalog data import job. */
export interface CatalogCsvImportNotification {
  /** @format date-time */
  created?: string;
  creator?: string | null;
  description?: string | null;
  /**
   * Gets the count of errors during processing.
   * @format int64
   */
  readonly errorCount?: number;
  /** Gets or sets the errors that has occurred during processing. */
  errors?: string[] | null;
  /**
   * Gets or sets the job finish date and time.
   * @format date-time
   */
  finished?: string | null;
  id?: string | null;
  isNew?: boolean;
  notifyType?: string | null;
  /**
   * Gets or sets the count of processed objects.
   * @format int64
   */
  processedCount?: number;
  /** @format int32 */
  repeatCount?: number;
  serverId?: string | null;
  title?: string | null;
  /**
   * Gets or sets the total count of objects to process.
   * @format int64
   */
  totalCount?: number;
}

export interface CustomerAddress {
  line1?: string | null;
  line2?: string | null;
  addressType?: VirtoCommerceCoreModuleCoreCommonAddressType;
  city?: string | null;
  countryCode?: string | null;
  countryName?: string | null;
  description?: string | null;
  email?: string | null;
  firstName?: string | null;
  id?: string | null;
  isDefault?: boolean;
  key?: string | null;
  lastName?: string | null;
  middleName?: string | null;
  name?: string | null;
  organization?: string | null;
  outerId?: string | null;
  phone?: string | null;
  postalCode?: string | null;
  regionId?: string | null;
  regionName?: string | null;
  zip?: string | null;
}

export interface FluentValidationResultsValidationFailure {
  attemptedValue?: object | null;
  customState?: object | null;
  errorCode?: string | null;
  errorMessage?: string | null;
  formattedMessagePlaceholderValues?: Record<string, object | null>;
  propertyName?: string | null;
  severity?: FluentValidationSeverity;
}

export interface FluentValidationResultsValidationResult {
  errors?: FluentValidationResultsValidationFailure[] | null;
  readonly isValid?: boolean;
  ruleSetsExecuted?: string[] | null;
}

export type FluentValidationSeverity = "Error" | "Warning" | "Info";

export interface InventoryAddress {
  line1?: string | null;
  line2?: string | null;
  addressType?: VirtoCommerceCoreModuleCoreCommonAddressType;
  city?: string | null;
  countryCode?: string | null;
  countryName?: string | null;
  description?: string | null;
  email?: string | null;
  firstName?: string | null;
  isDefault?: boolean;
  key?: string | null;
  lastName?: string | null;
  middleName?: string | null;
  name?: string | null;
  organization?: string | null;
  outerId?: string | null;
  phone?: string | null;
  postalCode?: string | null;
  regionId?: string | null;
  regionName?: string | null;
  zip?: string | null;
}

export interface MicrosoftAspNetCoreIdentityIdentityError {
  code?: string | null;
  description?: string | null;
}

export interface MicrosoftAspNetCoreIdentityIdentityResult {
  readonly errors?: MicrosoftAspNetCoreIdentityIdentityError[] | null;
  readonly succeeded?: boolean;
}

export interface MicrosoftAspNetCoreIdentitySignInResult {
  readonly isLockedOut?: boolean;
  readonly isNotAllowed?: boolean;
  readonly requiresTwoFactor?: boolean;
  readonly succeeded?: boolean;
}

export interface MicrosoftAspNetCoreJsonPatchJsonPatchDocument {
  operations?: MicrosoftAspNetCoreJsonPatchOperationsOperation[] | null;
}

export interface MicrosoftAspNetCoreJsonPatchOperationsOperation {
  from?: string | null;
  op?: string | null;
  path?: string | null;
  value?: object | null;
}

export interface MicrosoftAspNetCoreMvcProblemDetails {
  detail?: string | null;
  instance?: string | null;
  /** @format int32 */
  status?: number | null;
  title?: string | null;
  type?: string | null;
  [key: string]: any;
}

export type MicrosoftIdentityModelTokensCryptoProviderCache = object;

export interface MicrosoftIdentityModelTokensCryptoProviderFactory {
  /** @default false */
  cacheCustomProviders?: boolean;
  /** @default true */
  cacheSignatureProviders?: boolean;
  readonly cryptoProviderCache?: MicrosoftIdentityModelTokensCryptoProviderCache | null;
  customCryptoProvider?: MicrosoftIdentityModelTokensICryptoProvider | null;
  /** @format int32 */
  signatureProviderObjectPoolCacheSize?: number;
}

export type MicrosoftIdentityModelTokensICryptoProvider = object;

export interface MicrosoftIdentityModelTokensJsonWebKey {
  readonly x5c?: string[] | null;
  x5t?: string | null;
  x5tS256?: string | null;
  x5u?: string | null;
  readonly additionalData?: Record<string, object | null>;
  alg?: string | null;
  crv?: string | null;
  cryptoProviderFactory?: MicrosoftIdentityModelTokensCryptoProviderFactory | null;
  d?: string | null;
  dp?: string | null;
  dq?: string | null;
  e?: string | null;
  readonly hasPrivateKey?: boolean;
  k?: string | null;
  keyId?: string | null;
  readonly keyOps?: string[] | null;
  /** @format int32 */
  readonly keySize?: number;
  kid?: string | null;
  kty?: string | null;
  n?: string | null;
  readonly oth?: string[] | null;
  p?: string | null;
  priv?: string | null;
  pub?: string | null;
  q?: string | null;
  qi?: string | null;
  use?: string | null;
  x?: string | null;
  y?: string | null;
}

export interface MicrosoftIdentityModelTokensJsonWebKeySet {
  readonly additionalData?: Record<string, object | null>;
  jsonData?: string | null;
  readonly keys?: MicrosoftIdentityModelTokensJsonWebKey[] | null;
  /** @default true */
  skipUnresolvedJsonWebKeys?: boolean;
}

export interface OpenIddictAbstractionsOpenIddictApplicationDescriptor {
  applicationType?: string | null;
  clientId?: string | null;
  clientSecret?: string | null;
  clientType?: string | null;
  consentType?: string | null;
  displayName?: string | null;
  readonly displayNames?: Record<string, string> | null;
  jsonWebKeySet?: MicrosoftIdentityModelTokensJsonWebKeySet | null;
  /** @uniqueItems true */
  readonly permissions?: string[] | null;
  /** @uniqueItems true */
  readonly postLogoutRedirectUris?: string[] | null;
  readonly properties?: Record<string, SystemTextJsonJsonElement> | null;
  /** @uniqueItems true */
  readonly redirectUris?: string[] | null;
  /** @uniqueItems true */
  readonly requirements?: string[] | null;
  readonly settings?: Record<string, string> | null;
}

export interface OpenIddictAbstractionsOpenIddictResponse {
  accessToken?: string | null;
  code?: string | null;
  /** @format int32 */
  readonly count?: number;
  deviceCode?: string | null;
  error?: string | null;
  errorDescription?: string | null;
  errorUri?: string | null;
  /** @format int64 */
  expiresIn?: number | null;
  idToken?: string | null;
  iss?: string | null;
  issuedTokenType?: string | null;
  refreshToken?: string | null;
  requestUri?: string | null;
  scope?: string | null;
  state?: string | null;
  tokenType?: string | null;
  userCode?: string | null;
  verificationUri?: string | null;
  verificationUriComplete?: string | null;
}

export interface OrderAddress {
  line1?: string | null;
  line2?: string | null;
  addressType?: VirtoCommerceCoreModuleCoreCommonAddressType;
  city?: string | null;
  countryCode?: string | null;
  countryName?: string | null;
  description?: string | null;
  email?: string | null;
  firstName?: string | null;
  isDefault?: boolean;
  key?: string | null;
  lastName?: string | null;
  middleName?: string | null;
  name?: string | null;
  organization?: string | null;
  outerId?: string | null;
  phone?: string | null;
  postalCode?: string | null;
  regionId?: string | null;
  regionName?: string | null;
  zip?: string | null;
}

export interface OrderConfigurationItem {
  catalogId?: string | null;
  categoryId?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  customText?: string | null;
  /** Not mapped for updates: updates to this property are ignored by CRUD services. */
  readonly customerOrderId?: string | null;
  /** @format double */
  readonly extendedPrice?: number;
  files?: OrderConfigurationItemFile[] | null;
  id?: string | null;
  imageUrl?: string | null;
  lineItemId?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  /** @format double */
  price?: number;
  productId?: string | null;
  /** @format int32 */
  quantity?: number;
  /** @format double */
  salePrice?: number;
  sectionId?: string | null;
  sectionName?: string | null;
  sku?: string | null;
  type?: string | null;
}

export interface OrderConfigurationItemFile {
  contentType?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  /** @format int64 */
  size?: number;
  url?: string | null;
}

export interface OrderLineItem {
  cancelReason?: string | null;
  /** @format date-time */
  cancelledDate?: string | null;
  catalogId?: string | null;
  categoryId?: string | null;
  comment?: string | null;
  configurationItems?: OrderConfigurationItem[] | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  currency?: string | null;
  /** Not mapped for updates: updates to this property are ignored by CRUD services. */
  readonly customerOrderId?: string | null;
  /**
   * Gets the value of the single qty line item discount amount
   * @format double
   */
  discountAmount?: number;
  /** @format double */
  discountAmountWithTax?: number;
  /** @format double */
  discountTotal?: number;
  /** @format double */
  discountTotalWithTax?: number;
  discounts?: VirtoCommerceCoreModuleCoreCommonDiscount[] | null;
  dynamicProperties?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicObjectProperty[]
    | null;
  /** @format double */
  extendedPrice?: number;
  /** @format double */
  extendedPriceWithTax?: number;
  /** @format double */
  fee?: number;
  feeDetails?: VirtoCommerceOrdersModuleCoreModelFeeDetail[] | null;
  /** @format double */
  feeWithTax?: number;
  fulfillmentCenterId?: string | null;
  fulfillmentCenterName?: string | null;
  fulfillmentLocationCode?: string | null;
  /** @format double */
  height?: number | null;
  id?: string | null;
  imageUrl?: string | null;
  isCancelled?: boolean;
  isConfigured?: boolean;
  /**
   * Indicates whether the discount amount per item was rounded according to the currency settings.
   * If false, DiscountAmount and PlacedPrice should not be visible to the customer, as these values may be incorrect;
   * in this case, DiscountTotal and ExtendedPrice should be used.
   */
  isDiscountAmountRounded?: boolean;
  isGift?: boolean | null;
  /** @format double */
  length?: number | null;
  /** @format double */
  listTotal?: number;
  /** @format double */
  listTotalWithTax?: number;
  measureUnit?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  readonly objectType?: string | null;
  outerId?: string | null;
  /**
   * Resulting price with discount for one unit
   * @format double
   */
  placedPrice?: number;
  /** @format double */
  placedPriceWithTax?: number;
  /**
   * unit price without discount and tax
   * @format double
   */
  price?: number;
  /** Price id */
  priceId?: string | null;
  /** @format double */
  priceWithTax?: number;
  productId?: string | null;
  productOuterId?: string | null;
  productType?: string | null;
  /** @format int32 */
  quantity?: number;
  /**
   * Reserve quantity
   * @format int32
   */
  reserveQuantity?: number;
  shippingMethodCode?: string | null;
  sku?: string | null;
  status?: string | null;
  taxDetails?: VirtoCommerceCoreModuleCoreTaxTaxDetail[] | null;
  /** @format double */
  taxPercentRate?: number;
  /** @format double */
  taxTotal?: number;
  /** Tax category or type */
  taxType?: string | null;
  vendorId?: string | null;
  /** @format double */
  weight?: number | null;
  weightUnit?: string | null;
  /** @format double */
  width?: number | null;
}

export interface OrderShipment {
  cancelReason?: string | null;
  /** @format date-time */
  cancelledDate?: string | null;
  /** For system use to handle canellation flow */
  cancelledState?: VirtoCommerceOrdersModuleCoreModelCancelledState;
  comment?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  currency?: string | null;
  customerOrder?: VirtoCommerceOrdersModuleCoreModelCustomerOrder | null;
  customerOrderId?: string | null;
  deliveryAddress?: OrderAddress | null;
  /** @format date-time */
  deliveryDate?: string | null;
  /** @format double */
  discountAmount?: number;
  /** @format double */
  discountAmountWithTax?: number;
  discounts?: VirtoCommerceCoreModuleCoreCommonDiscount[] | null;
  dynamicProperties?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicObjectProperty[]
    | null;
  employeeId?: string | null;
  employeeName?: string | null;
  /** @format double */
  fee?: number;
  feeDetails?: VirtoCommerceOrdersModuleCoreModelFeeDetail[] | null;
  /** @format double */
  feeWithTax?: number;
  fulfillmentCenterId?: string | null;
  fulfillmentCenterName?: string | null;
  /** @format double */
  height?: number | null;
  id?: string | null;
  inPayments?: VirtoCommerceOrdersModuleCoreModelPaymentIn[] | null;
  isApproved?: boolean;
  /** Used by payment provides to indicate that cancellation operation has completed */
  isCancelled?: boolean;
  items?: OrderShipmentItem[] | null;
  /** @format double */
  length?: number | null;
  measureUnit?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  number?: string | null;
  objectType?: string | null;
  operationType?: string | null;
  operationsLog?: VirtoCommercePlatformCoreChangeLogOperationLog[] | null;
  organizationId?: string | null;
  organizationName?: string | null;
  outerId?: string | null;
  packages?: VirtoCommerceOrdersModuleCoreModelShipmentPackage[] | null;
  parentOperationId?: string | null;
  pickupLocationId?: string | null;
  /** @format double */
  price?: number;
  /** @format double */
  priceWithTax?: number;
  /** Current shipment method code */
  shipmentMethodCode?: string | null;
  /** Current shipment option code */
  shipmentMethodOption?: string | null;
  /** Shipment method contains additional shipment method information */
  shippingMethod?: VirtoCommerceShippingModuleCoreModelShippingMethod | null;
  status?: string | null;
  /** @format double */
  sum?: number;
  taxDetails?: VirtoCommerceCoreModuleCoreTaxTaxDetail[] | null;
  /** @format double */
  taxPercentRate?: number;
  /** @format double */
  taxTotal?: number;
  /** Tax category or type */
  taxType?: string | null;
  /** @format double */
  total?: number;
  /** @format double */
  totalWithTax?: number;
  /** Tracking information */
  trackingNumber?: string | null;
  trackingUrl?: string | null;
  vendorId?: string | null;
  /** @format double */
  weight?: number | null;
  weightUnit?: string | null;
  /** @format double */
  width?: number | null;
  withPrices?: boolean;
}

export interface OrderShipmentItem {
  barCode?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  lineItem?: OrderLineItem | null;
  lineItemId?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  outerId?: string | null;
  /** @format int32 */
  quantity?: number;
  status?: string | null;
}

export interface QuoteAddress {
  line1?: string | null;
  line2?: string | null;
  addressType?: VirtoCommerceCoreModuleCoreCommonAddressType;
  city?: string | null;
  countryCode?: string | null;
  countryName?: string | null;
  description?: string | null;
  email?: string | null;
  firstName?: string | null;
  id?: string | null;
  isDefault?: boolean;
  key?: string | null;
  lastName?: string | null;
  middleName?: string | null;
  name?: string | null;
  organization?: string | null;
  outerId?: string | null;
  phone?: string | null;
  postalCode?: string | null;
  regionId?: string | null;
  regionName?: string | null;
  zip?: string | null;
}

export interface SystemSecurityClaimsClaim {
  issuer?: string | null;
  originalIssuer?: string | null;
  readonly properties?: Record<string, string> | null;
  subject?: SystemSecurityClaimsClaimsIdentity | null;
  type?: string | null;
  value?: string | null;
  valueType?: string | null;
}

export interface SystemSecurityClaimsClaimsIdentity {
  actor?: SystemSecurityClaimsClaimsIdentity | null;
  authenticationType?: string | null;
  bootstrapContext?: object | null;
  claims?: SystemSecurityClaimsClaim[] | null;
  readonly isAuthenticated?: boolean;
  label?: string | null;
  readonly name?: string | null;
  readonly nameClaimType?: string | null;
  readonly roleClaimType?: string | null;
}

export interface SystemTextJsonJsonElement {
  readonly valueKind?: SystemTextJsonJsonValueKind;
}

export type SystemTextJsonJsonValueKind =
  | "Undefined"
  | "Object"
  | "Array"
  | "String"
  | "Number"
  | "True"
  | "False"
  | "Null";

export interface TaxAddress {
  line1?: string | null;
  line2?: string | null;
  addressType?: VirtoCommerceCoreModuleCoreCommonAddressType;
  city?: string | null;
  countryCode?: string | null;
  countryName?: string | null;
  description?: string | null;
  email?: string | null;
  firstName?: string | null;
  isDefault?: boolean;
  key?: string | null;
  lastName?: string | null;
  middleName?: string | null;
  name?: string | null;
  organization?: string | null;
  outerId?: string | null;
  phone?: string | null;
  postalCode?: string | null;
  regionId?: string | null;
  regionName?: string | null;
  zip?: string | null;
}

export interface TaxCustomer {
  addresses?: TaxAddress[] | null;
  /** @format date-time */
  birthDate?: string | null;
  defaultLanguage?: string | null;
  emails?: string[] | null;
  firstName?: string | null;
  groups?: string[] | null;
  id?: string | null;
  lastName?: string | null;
  middleName?: string | null;
  name?: string | null;
  organizations?: string[] | null;
  outerId?: string | null;
  phones?: string[] | null;
  taxPayerId?: string | null;
  timeZone?: string | null;
}

export interface TaxStore {
  country?: string | null;
  defaultCurrency?: string | null;
  defaultLanguage?: string | null;
  id?: string | null;
  name?: string | null;
  outerId?: string | null;
  region?: string | null;
  timeZone?: string | null;
}

export interface VirtoCommerceAssetsModuleCoreAssetsAssetEntry {
  blobInfo?: VirtoCommerceAssetsModuleCoreAssetsBlobInfo | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  /** User defined grouping (optional) */
  group?: string | null;
  id?: string | null;
  /** Asset language */
  languageCode?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  tenant?: VirtoCommercePlatformCoreCommonTenantIdentity | null;
}

export interface VirtoCommerceAssetsModuleCoreAssetsAssetEntrySearchResult {
  results?: VirtoCommerceAssetsModuleCoreAssetsAssetEntry[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceAssetsModuleCoreAssetsBlobEntry {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  relativeUrl?: string | null;
  type?: string | null;
  url?: string | null;
}

export interface VirtoCommerceAssetsModuleCoreAssetsBlobEntrySearchResult {
  results?: VirtoCommerceAssetsModuleCoreAssetsBlobEntry[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceAssetsModuleCoreAssetsBlobFolder {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  parentUrl?: string | null;
  relativeUrl?: string | null;
  type?: string | null;
  url?: string | null;
}

export interface VirtoCommerceAssetsModuleCoreAssetsBlobInfo {
  contentType?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  /** Relative url */
  key?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  relativeUrl?: string | null;
  /** @format int64 */
  size?: number;
  type?: string | null;
  url?: string | null;
}

/** A recurring/scheduled job with its effective schedule and last/next run, for the admin view. */
export interface VirtoCommerceBackgroundJobsCoreAdminRecurringJobInfo {
  /** Effective cron expression (fixed, or resolved from settings); null when unset/disabled. */
  cron?: string | null;
  /** Whether the schedule is currently enabled. */
  enabled?: boolean;
  /** Handler type name the schedule runs, when known. */
  handlerType?: string | null;
  /** Stable recurring-job id. */
  id: string | null;
  /**
   * Last enqueued occurrence (UTC), when the engine's state store tracks it; null otherwise.
   * @format date-time
   */
  lastRunUtc?: string | null;
  /**
   * Next computed occurrence (UTC) for the effective cron; null when disabled or cron invalid.
   * @format date-time
   */
  nextRunUtc?: string | null;
  /** Payload type name the schedule enqueues, when known. */
  payloadType?: string | null;
  /** True when the schedule (enabler + cron) is driven by module settings rather than a fixed cron. */
  settingDriven?: boolean;
  /** IANA/Windows time-zone id the cron is evaluated in. */
  timeZone?: string | null;
}

/** A registered background-job handler, as shown in the admin troubleshooting view. */
export interface VirtoCommerceBackgroundJobsCoreAdminRegisteredJobInfo {
  /** Handler type full name. */
  handlerType: string | null;
  /** Friendly, addressable name (used by the execute-by-name endpoint). */
  name: string | null;
  /** Payload contract type full name. */
  payloadType: string | null;
  /** Whether this job can be triggered on demand by name via the execute endpoint (false for internal plumbing). */
  triggerable?: boolean;
}

/** Request body for triggering a registered background job by name over REST. */
export interface VirtoCommerceBackgroundJobsWebModelsEnqueueJobRequest {
  /** Registered job name (see `GET api/background-jobs/registered`). */
  name?: string | null;
  /** Optional enqueue options (queue, title, progress, retries, unique key). */
  options?: VirtoCommercePlatformCoreJobsEnqueueOptions | null;
  /** The job payload as JSON; bound to the handler's payload type. Omit for a parameterless payload. */
  payload?: SystemTextJsonJsonElement;
}

export interface VirtoCommerceBulkActionsModuleCoreModelsBulkActionsBulkActionContext {
  /** Gets or sets the action name. */
  actionName?: string | null;
  /** Gets the context type name. */
  readonly contextTypeName?: string | null;
}

export interface VirtoCommerceBulkActionsModuleCoreModelsBulkActionsBulkActionPushNotification {
  /** @format date-time */
  created?: string;
  creator?: string | null;
  description?: string | null;
  /**
   * Gets error count.
   * @format int64
   */
  readonly errorCount?: number;
  /** Gets or sets the errors. */
  errors?: string[] | null;
  /**
   * Gets or sets the finished.
   * @format date-time
   */
  finished?: string | null;
  id?: string | null;
  isNew?: boolean;
  /** Gets or sets the job id. */
  jobId?: string | null;
  notifyType?: string | null;
  /**
   * Gets or sets the processed count.
   * @format int32
   */
  processedCount?: number | null;
  /** @format int32 */
  repeatCount?: number;
  serverId?: string | null;
  title?: string | null;
  /**
   * Gets or sets the total count.
   * @format int32
   */
  totalCount?: number | null;
}

export type VirtoCommerceBulkActionsModuleCoreServicesIBulkActionFactory =
  object;

export interface VirtoCommerceBulkActionsModuleCoreServicesIBulkActionProvider {
  applicableTypes?: string[] | null;
  bulkActionFactory?: VirtoCommerceBulkActionsModuleCoreServicesIBulkActionFactory | null;
  contextTypeName?: string | null;
  dataSourceFactory?: VirtoCommerceBulkActionsModuleCoreServicesIDataSourceFactory | null;
  name?: string | null;
  permissions?: string[] | null;
}

export type VirtoCommerceBulkActionsModuleCoreServicesIDataSourceFactory =
  object;

export interface VirtoCommerceCartModuleCoreModelCartSharingSetting {
  access?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  scope?: string | null;
  sharedWithId?: string | null;
  shoppingCartId?: string | null;
}

export interface VirtoCommerceCartModuleCoreModelCartTotal {
  currencyCode?: string | null;
  /** @format double */
  discountTotal?: number;
  /** @format double */
  subTotal?: number;
  /** @format double */
  taxTotal?: number;
  /** @format double */
  total?: number;
}

export interface VirtoCommerceCartModuleCoreModelPayment {
  /** @format double */
  amount?: number;
  billingAddress?: CartAddress | null;
  comment?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  currency?: string | null;
  /** @format double */
  discountAmount?: number;
  /** @format double */
  discountAmountWithTax?: number;
  discounts?: VirtoCommerceCoreModuleCoreCommonDiscount[] | null;
  dynamicProperties?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicObjectProperty[]
    | null;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  readonly objectType?: string | null;
  outerId?: string | null;
  paymentGatewayCode?: string | null;
  /** @format double */
  price?: number;
  /** @format double */
  priceWithTax?: number;
  purpose?: string | null;
  taxDetails?: VirtoCommerceCoreModuleCoreTaxTaxDetail[] | null;
  /** @format double */
  taxPercentRate?: number;
  /** @format double */
  taxTotal?: number;
  taxType?: string | null;
  /** @format double */
  total?: number;
  /** @format double */
  totalWithTax?: number;
  vendorId?: string | null;
}

export interface VirtoCommerceCartModuleCoreModelSearchShoppingCartSearchCriteria {
  /** @format date-time */
  abandonmentNotificationEndDate?: string | null;
  /** @format date-time */
  abandonmentNotificationStartDate?: string | null;
  /** @format date-time */
  createdEndDate?: string | null;
  /** @format date-time */
  createdStartDate?: string | null;
  currency?: string | null;
  customerId?: string | null;
  customerIds?: string[] | null;
  customerOrOrganization?: boolean;
  hasAbandonmentNotification?: boolean | null;
  hasLineItems?: boolean | null;
  isAnonymous?: boolean | null;
  keyword?: string | null;
  languageCode?: string | null;
  /** @format date-time */
  modifiedEndDate?: string | null;
  /** @format date-time */
  modifiedStartDate?: string | null;
  name?: string | null;
  notType?: string | null;
  notTypes?: string[] | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  organizationId?: string | null;
  organizationIdIsEmpty?: boolean;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  sharingKey?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  status?: string | null;
  storeId?: string | null;
  /** @format int32 */
  take?: number;
  type?: string | null;
  types?: string[] | null;
}

export interface VirtoCommerceCartModuleCoreModelSearchShoppingCartSearchResult {
  results?: VirtoCommerceCartModuleCoreModelShoppingCart[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceCartModuleCoreModelShippingEvaluationContext {
  currency?: string | null;
  shoppingCart?: VirtoCommerceCartModuleCoreModelShoppingCart | null;
}

export interface VirtoCommerceCartModuleCoreModelShoppingCart {
  /** @format date-time */
  abandonmentNotificationDate?: string | null;
  addresses?: CartAddress[] | null;
  cartTotals?: VirtoCommerceCartModuleCoreModelCartTotal[] | null;
  channelId?: string | null;
  checkoutId?: string | null;
  comment?: string | null;
  coupon?: string | null;
  coupons?: string[] | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  currency?: string | null;
  customerId?: string | null;
  customerName?: string | null;
  description?: string | null;
  /** @format double */
  discountAmount?: number;
  /** @format double */
  discountAmountWithTax?: number;
  /** @format double */
  discountTotal?: number;
  /** @format double */
  discountTotalWithTax?: number;
  discounts?: VirtoCommerceCoreModuleCoreCommonDiscount[] | null;
  dynamicProperties?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicObjectProperty[]
    | null;
  /** @format double */
  fee?: number;
  /** @format double */
  feeTotal?: number;
  /** @format double */
  feeTotalWithTax?: number;
  /** @format double */
  feeWithTax?: number;
  /** @format double */
  handlingTotal?: number;
  /** @format double */
  handlingTotalWithTax?: number;
  id?: string | null;
  isAnonymous?: boolean;
  isRecuring?: boolean | null;
  items?: CartLineItem[] | null;
  languageCode?: string | null;
  /** @format int32 */
  lineItemsCount?: number;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  readonly objectType?: string | null;
  organizationId?: string | null;
  organizationName?: string | null;
  /** @format double */
  paymentDiscountTotal?: number;
  /** @format double */
  paymentDiscountTotalWithTax?: number;
  /** @format double */
  paymentSubTotal?: number;
  /** @format double */
  paymentSubTotalWithTax?: number;
  /** @format double */
  paymentTotal?: number;
  /** @format double */
  paymentTotalWithTax?: number;
  payments?: VirtoCommerceCartModuleCoreModelPayment[] | null;
  purchaseOrderNumber?: string | null;
  sharingSettings?: VirtoCommerceCartModuleCoreModelCartSharingSetting[] | null;
  shipments?: CartShipment[] | null;
  /** @format double */
  shippingDiscountTotal?: number;
  /** @format double */
  shippingDiscountTotalWithTax?: number;
  /** @format double */
  shippingSubTotal?: number;
  /** @format double */
  shippingSubTotalWithTax?: number;
  /** @format double */
  shippingTotal?: number;
  /** @format double */
  shippingTotalWithTax?: number;
  status?: string | null;
  storeId?: string | null;
  /** @format double */
  subTotal?: number;
  /** @format double */
  subTotalDiscount?: number;
  /** @format double */
  subTotalDiscountWithTax?: number;
  /** @format double */
  subTotalWithTax?: number;
  taxDetails?: VirtoCommerceCoreModuleCoreTaxTaxDetail[] | null;
  taxIncluded?: boolean | null;
  /** @format double */
  taxPercentRate?: number;
  /** @format double */
  taxTotal?: number;
  taxType?: string | null;
  /** @format double */
  total?: number;
  type?: string | null;
  validationType?: string | null;
  /** @format double */
  volumetricWeight?: number | null;
  /** @format double */
  weight?: number | null;
  weightUnit?: string | null;
}

export interface VirtoCommerceCatalogCsvImportModuleCoreModelCsvExportInfo {
  catalogId?: string | null;
  categoryIds?: string[] | null;
  configuration?: VirtoCommerceCatalogCsvImportModuleCoreModelCsvProductMappingConfiguration | null;
  currency?: string | null;
  fulfilmentCenterId?: string | null;
  priceListId?: string | null;
  productIds?: string[] | null;
}

export interface VirtoCommerceCatalogCsvImportModuleCoreModelCsvImportInfo {
  catalogId?: string | null;
  configuration?: VirtoCommerceCatalogCsvImportModuleCoreModelCsvProductMappingConfiguration | null;
  fileUrl?: string | null;
}

export interface VirtoCommerceCatalogCsvImportModuleCoreModelCsvProductMappingConfiguration {
  csvColumns?: string[] | null;
  delimiter?: string | null;
  eTag?: string | null;
  propertyCsvColumns?: string[] | null;
  propertyMaps?:
    | VirtoCommerceCatalogCsvImportModuleCoreModelCsvProductPropertyMap[]
    | null;
}

export interface VirtoCommerceCatalogCsvImportModuleCoreModelCsvProductPropertyMap {
  csvColumnName?: string | null;
  customValue?: string | null;
  entityColumnName?: string | null;
  isRequired?: boolean;
  isSystemProperty?: boolean;
  locale?: string | null;
  stringFormat?: string | null;
}

/** Notification for catalog data export job. */
export interface VirtoCommerceCatalogCsvImportModuleWebModelPushNotificationsExportNotification {
  /** @format date-time */
  created?: string;
  creator?: string | null;
  description?: string | null;
  /** Gets or sets the URL for downloading exported data. */
  downloadUrl?: string | null;
  /**
   * Gets the count of errors during processing.
   * @format int64
   */
  readonly errorCount?: number;
  /** Gets or sets the errors that has occurred during processing. */
  errors?: string[] | null;
  /**
   * Gets or sets the job finish date and time.
   * @format date-time
   */
  finished?: string | null;
  id?: string | null;
  isNew?: boolean;
  notifyType?: string | null;
  /**
   * Gets or sets the count of processed objects.
   * @format int64
   */
  processedCount?: number;
  /** @format int32 */
  repeatCount?: number;
  serverId?: string | null;
  title?: string | null;
  /**
   * Gets or sets the total count of objects to process.
   * @format int64
   */
  totalCount?: number;
}

export interface VirtoCommerceCatalogModuleCoreModelAsset {
  /** @format byte */
  binaryData?: Blob | null;
  /**
   * Gets or sets the transient relative reference to binary data in a catalog backup package.
   * The property is populated only while a backup is exported or restored and is not persisted.
   */
  binaryDataReference?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  description?: string | null;
  /** Gets or sets the asset group name. */
  group?: string | null;
  id?: string | null;
  /** System flag used to mark that object was inherited from other */
  readonly isInherited?: boolean;
  /** Gets or sets the asset language. */
  languageCode?: string | null;
  mimeType?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  /** Gets or sets the asset name. */
  name?: string | null;
  outerId?: string | null;
  readonly readableSize?: string | null;
  relativeUrl?: string | null;
  seoInfos?: VirtoCommerceSeoCoreModelsSeoInfo[] | null;
  readonly seoObjectType?: string | null;
  /** @format int64 */
  size?: number;
  /** @format int32 */
  sortOrder?: number;
  /** Gets or sets the asset type identifier. */
  typeId?: string | null;
  url?: string | null;
}

export interface VirtoCommerceCatalogModuleCoreModelAutomaticLinkQuery {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  sourceCatalogId?: string | null;
  sourceCatalogQuery?: string | null;
  targetCategoryId?: string | null;
}

export interface VirtoCommerceCatalogModuleCoreModelBrandStoreSetting {
  brandCatalogId?: string | null;
  brandPropertyName?: string | null;
  brandsEnabled?: boolean;
  store?: VirtoCommerceStoreModuleCoreModelStore | null;
  storeId?: string | null;
}

export interface VirtoCommerceCatalogModuleCoreModelCatalog {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  readonly defaultLanguage?: VirtoCommerceCatalogModuleCoreModelCatalogLanguage | null;
  id?: string | null;
  isVirtual?: boolean;
  languages?: VirtoCommerceCatalogModuleCoreModelCatalogLanguage[] | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  outerId?: string | null;
  properties?: VirtoCommerceCatalogModuleCoreModelProperty[] | null;
  propertyGroups?: VirtoCommerceCatalogModuleCoreModelPropertyGroup[] | null;
  seoInfos?: VirtoCommerceSeoCoreModelsSeoInfo[] | null;
  readonly seoObjectType?: string | null;
}

export interface VirtoCommerceCatalogModuleCoreModelCatalogLanguage {
  catalogId?: string | null;
  id?: string | null;
  isDefault?: boolean;
  languageCode?: string | null;
  /**
   * Lowest number wins
   * @format int32
   */
  priority?: number;
}

export interface VirtoCommerceCatalogModuleCoreModelCatalogProduct {
  assets?: VirtoCommerceCatalogModuleCoreModelAsset[] | null;
  associations?: VirtoCommerceCatalogModuleCoreModelProductAssociation[] | null;
  /** The ID of the catalog to which this product belongs. */
  catalogId?: string | null;
  /** The ID of the category to which this product belongs. */
  categoryId?: string | null;
  /** The Stock Keeping Unit (SKU) code for the product. */
  code?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  /**
   * The date and time when the download link or access to the product will expire.
   * @format date-time
   */
  downloadExpiration?: string | null;
  /** The type of product download. Valid values include: "Standard Product", "Software", and "Music". */
  downloadType?: string | null;
  enableReview?: boolean | null;
  /**
   * Listing expires on the specific date and time. If you do not specify an end date, the product will be active until you deactivate it.
   * @format date-time
   */
  endDate?: string | null;
  excludedProperties?:
    | VirtoCommerceCatalogModuleCoreModelExcludedProperty[]
    | null;
  /** The Global Trade Item Number (GTIN) for the product. This can include UPC (in North America), EAN (in Europe), JAN (in Japan), and ISBN (for books). */
  gtin?: string | null;
  /** Indicates whether the product requires the user to agree to any terms or conditions before downloading. */
  hasUserAgreement?: boolean | null;
  /**
   * The height of the product, in the unit specified by the MeasureUnit property.
   * @format double
   */
  height?: number | null;
  id?: string | null;
  images?: VirtoCommerceCatalogModuleCoreModelImage[] | null;
  /** Gets the default image for the product. */
  readonly imgSrc?: string | null;
  /**
   * The date and time when the product was last indexed for search.
   * @format date-time
   */
  indexingDate?: string | null;
  /**
   * Specifies whether the product is currently visible on the store for customers to view and purchase.
   * If set to false, the product is currently sold out.
   */
  isActive?: boolean | null;
  /**
   * Specifies whether the product is currently visible on the store for customers to view and purchase.
   * If set to false, the product is currently ouf of stock.
   */
  isBuyable?: boolean | null;
  /** System flag used to mark that object was inherited from other */
  readonly isInherited?: boolean;
  /**
   * The length of the product, in the unit specified by the MeasureUnit property.
   * @format double
   */
  length?: number | null;
  links?: VirtoCommerceCatalogModuleCoreModelCategoryLink[] | null;
  localizedName?: VirtoCommercePlatformCoreCommonLocalizedString | null;
  /** The ID of the main product associated with this product variation. */
  mainProductId?: string | null;
  /** A manufacturer part number (MPN) is a unique alphanumeric code assigned by a manufacturer to identify a specific product or component. It is used primarily for part tracking in inventory management, supply chain operations, and ordering purposes. */
  manufacturerPartNumber?: string | null;
  /**
   * The maximum number of times the product can be downloaded. A value of 0 indicates no limit.
   * @format int32
   */
  maxNumberOfDownload?: number | null;
  /**
   * The maximum quantity of the product that can be purchased in a single order. A value of 0 indicates that there are no limitations on the maximum quantity.
   * @format int32
   */
  maxQuantity?: number | null;
  /** The unit of measurement for the product's height, length, and width. */
  measureUnit?: string | null;
  /**
   * The minimum quantity of the product that must be purchased in a single order. A value of 0 indicates that there are no limitations on the minimum quantity.
   * @format int32
   */
  minQuantity?: number | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  /** The name of the product. */
  name?: string | null;
  /** An external identifier for the product that can be used for integration with external systems. */
  outerId?: string | null;
  /** Product outline in physical catalog (all parent categories ids concatenated. E.g. (1/21/344)) */
  readonly outline?: string | null;
  outlines?: VirtoCommerceCatalogModuleCoreOutlinesOutline[] | null;
  /**
   * Defines the number of items in a package. Quantity step for your product's. Default value is 1.
   * @format int32
   */
  packSize?: number;
  /** The type of package for this product, which determines the product's specific dimensions. */
  packageType?: string | null;
  readonly parentCategoryIsActive?: boolean;
  /** Product path in physical catalog (all parent categories names concatenated. E.g. (parent1/parent2)) */
  readonly path?: string | null;
  /**
   * Indicates the position of the product in the catalog for ordering purposes.
   * @format int32
   */
  priority?: number;
  /** The type of product. Can be "Physical", "Digital", etc. */
  productType?: string | null;
  properties?: VirtoCommerceCatalogModuleCoreModelProperty[] | null;
  referencedAssociations?:
    | VirtoCommerceCatalogModuleCoreModelProductAssociation[]
    | null;
  /** @format double */
  relevanceScore?: number | null;
  reviews?: VirtoCommerceCatalogModuleCoreModelEditorialReview[] | null;
  seoInfos?: VirtoCommerceSeoCoreModelsSeoInfo[] | null;
  /** Each descendant type should override this property to use other object type for seo records */
  readonly seoObjectType?: string | null;
  /** Specifies the type of shipping option available for the product. */
  shippingType?: string | null;
  /**
   * First listed date and time. If you do not specify an end date, the product will be active until you deactivate it.If you do not specify an end date, the product will be active until you deactivate it.If you do not specify a start date, the product will become active immediately once you save it.
   * @format date-time
   */
  startDate?: string;
  /** Specifies the type of tax applied to the product. */
  taxType?: string | null;
  readonly titularItemId?: string | null;
  /**
   * Indicates whether the inventory service is tracking the availability of this product.
   * If set to false, the product is considered in stock without any inventory limitations.
   */
  trackInventory?: boolean | null;
  variations?: VirtoCommerceCatalogModuleCoreModelVariation[] | null;
  /** ID of the vendor associated with the product. */
  vendor?: string | null;
  /**
   * The weight of the product, in the unit specified by the WeightUnit property.
   * @format double
   */
  weight?: number | null;
  /** The unit of measurement for the product's weight. */
  weightUnit?: string | null;
  /**
   * The width of the product, in the unit specified by the MeasureUnit property.
   * @format double
   */
  width?: number | null;
}

export interface VirtoCommerceCatalogModuleCoreModelCategory {
  assets?: VirtoCommerceCatalogModuleCoreModelAsset[] | null;
  catalogId?: string | null;
  code?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  descriptions?:
    | VirtoCommerceCatalogModuleCoreModelCategoryDescription[]
    | null;
  enableDescription?: boolean | null;
  excludedProperties?:
    | VirtoCommerceCatalogModuleCoreModelExcludedProperty[]
    | null;
  id?: string | null;
  images?: VirtoCommerceCatalogModuleCoreModelImage[] | null;
  /** Gets the default image */
  readonly imgSrc?: string | null;
  isActive?: boolean | null;
  /** System flag used to mark that object was inherited from other */
  readonly isInherited?: boolean;
  isVirtual?: boolean;
  /** @format int32 */
  level?: number;
  links?: VirtoCommerceCatalogModuleCoreModelCategoryLink[] | null;
  localizedName?: VirtoCommercePlatformCoreCommonLocalizedString | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  outerId?: string | null;
  /** Category outline in physical catalog (all parent categories ids concatenated. E.g. (1/21/344)) */
  readonly outline?: string | null;
  outlines?: VirtoCommerceCatalogModuleCoreOutlinesOutline[] | null;
  packageType?: string | null;
  parentId?: string | null;
  readonly parentIsActive?: boolean;
  /** Category path in physical catalog (all parent categories names concatenated. E.g. (parent1/parent2)) */
  readonly path?: string | null;
  /** @format int32 */
  priority?: number;
  properties?: VirtoCommerceCatalogModuleCoreModelProperty[] | null;
  /** @format double */
  relevanceScore?: number | null;
  seoInfos?: VirtoCommerceSeoCoreModelsSeoInfo[] | null;
  readonly seoObjectType?: string | null;
  taxType?: string | null;
}

export interface VirtoCommerceCatalogModuleCoreModelCategoryDescription {
  content?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  descriptionType?: string | null;
  id?: string | null;
  isInherited?: boolean;
  languageCode?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
}

export interface VirtoCommerceCatalogModuleCoreModelCategoryLink {
  catalogId?: string | null;
  categoryId?: string | null;
  /** Entry identifier which this link belongs to */
  readonly entryId?: string | null;
  isAutomatic?: boolean;
  listEntryId?: string | null;
  /** Gets or sets the type of the list entry. E.g. "product", "category" */
  listEntryType?: string | null;
  /** Gets the name of either target Catetory or Catalog */
  readonly name?: string | null;
  /**
   * Product order position in virtual catalog
   * @format int32
   */
  priority?: number;
  /** Gets the Id of either target Catetory or Catalog */
  readonly targetId?: string | null;
}

export interface VirtoCommerceCatalogModuleCoreModelCategoryPropertyValidationRequest {
  catalogId?: string | null;
  categoryId?: string | null;
  propertyName?: string | null;
  propertyType?: string | null;
  propertyValueType?: VirtoCommerceCatalogModuleCoreModelPropertyValueType;
}

export interface VirtoCommerceCatalogModuleCoreModelConfigurationProductConfiguration {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  isActive?: boolean;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  productId?: string | null;
  sections?:
    | VirtoCommerceCatalogModuleCoreModelConfigurationProductConfigurationSection[]
    | null;
}

export interface VirtoCommerceCatalogModuleCoreModelConfigurationProductConfigurationOption {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  isDefault?: boolean;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  productId?: string | null;
  readonly productImageUrl?: string | null;
  readonly productName?: string | null;
  readonly productType?: string | null;
  /** @format int32 */
  quantity?: number;
  sectionId?: string | null;
  text?: string | null;
}

export interface VirtoCommerceCatalogModuleCoreModelConfigurationProductConfigurationSection {
  allowCustomText?: boolean;
  allowPredefinedOptions?: boolean;
  configurationId?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  dependsOnSectionId?: string | null;
  description?: string | null;
  /** @format int32 */
  displayOrder?: number;
  id?: string | null;
  isRequired?: boolean;
  /** @format int32 */
  maxLength?: number | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  options?:
    | VirtoCommerceCatalogModuleCoreModelConfigurationProductConfigurationOption[]
    | null;
  type?: string | null;
}

export interface VirtoCommerceCatalogModuleCoreModelEditorialReview {
  content?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  isInherited?: boolean;
  languageCode?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  reviewType?: string | null;
}

export interface VirtoCommerceCatalogModuleCoreModelExcludedProperty {
  isInherited?: boolean;
  name?: string | null;
}

export interface VirtoCommerceCatalogModuleCoreModelImage {
  altText?: string | null;
  /** @format byte */
  binaryData?: Blob | null;
  /**
   * Gets or sets the transient relative reference to binary data in a catalog backup package.
   * The property is populated only while a backup is exported or restored and is not persisted.
   */
  binaryDataReference?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  description?: string | null;
  /** Gets or sets the asset group name. */
  group?: string | null;
  id?: string | null;
  /** System flag used to mark that object was inherited from other */
  readonly isInherited?: boolean;
  /** Gets or sets the asset language. */
  languageCode?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  /** Gets or sets the asset name. */
  name?: string | null;
  outerId?: string | null;
  relativeUrl?: string | null;
  seoInfos?: VirtoCommerceSeoCoreModelsSeoInfo[] | null;
  readonly seoObjectType?: string | null;
  /** @format int32 */
  sortOrder?: number;
  /** Gets or sets the asset type identifier. */
  typeId?: string | null;
  url?: string | null;
}

/** Represents  move list entries command */
export interface VirtoCommerceCatalogModuleCoreModelListEntriesMoveRequest {
  catalog?: string | null;
  readonly catalogId?: string | null;
  category?: string | null;
  listEntries?:
    | VirtoCommerceCatalogModuleCoreModelListEntryListEntryBase[]
    | null;
}

/** Base class for all entries used in catalog categories browsing. */
export interface VirtoCommerceCatalogModuleCoreModelListEntryListEntryBase {
  /** Gets or sets the catalog id. */
  catalogId?: string | null;
  /** Gets or sets the entry code. */
  code?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  /** Gets or sets the image URL. */
  imageUrl?: string | null;
  /** Gets or sets a value indicating whether this entry is active. */
  isActive?: boolean | null;
  /** Gets or sets the links. */
  links?: VirtoCommerceCatalogModuleCoreModelCategoryLink[] | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  /** Gets or sets the name. */
  name?: string | null;
  /** All entry parents ids */
  outline?: string[] | null;
  outlines?: VirtoCommerceCatalogModuleCoreOutlinesOutline[] | null;
  /** All entry parents names */
  path?: string[] | null;
  /** @format double */
  relevanceScore?: number | null;
  seoInfos?: VirtoCommerceSeoCoreModelsSeoInfo[] | null;
  seoObjectType?: string | null;
  /** Gets or sets the type. E.g. "product", "category" */
  type?: string | null;
}

export interface VirtoCommerceCatalogModuleCoreModelMeasure {
  code?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  description?: string | null;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  units?: VirtoCommerceCatalogModuleCoreModelMeasureUnit[] | null;
}

export interface VirtoCommerceCatalogModuleCoreModelMeasureUnit {
  code?: string | null;
  /** @format double */
  conversionFactor?: number;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  isDefault?: boolean;
  localizedName?: VirtoCommercePlatformCoreCommonLocalizedString | null;
  localizedSymbol?: VirtoCommercePlatformCoreCommonLocalizedString | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  symbol?: string | null;
}

export interface VirtoCommerceCatalogModuleCoreModelProductAssociation {
  /**
   * Each link element can have an associated object like Product, Category, etc.
   * Is a primary key of associated object
   */
  associatedObjectId?: string | null;
  /** Associated object image URL */
  readonly associatedObjectImg?: string | null;
  /** Display name for associated object */
  readonly associatedObjectName?: string | null;
  /** Associated object type : 'product', 'category' etc */
  associatedObjectType?: string | null;
  id?: string | null;
  images?: VirtoCommerceCatalogModuleCoreModelImage[] | null;
  readonly imgSrc?: string | null;
  /** Is a primary key of associating object */
  itemId?: string | null;
  outerId?: string | null;
  /** @format int32 */
  priority?: number;
  /** @format int32 */
  quantity?: number | null;
  tags?: string[] | null;
  /** Association type (Accessories, Up-Sales, Cross-Sales, Related etc) */
  type?: string | null;
}

export interface VirtoCommerceCatalogModuleCoreModelProperty {
  attributes?: VirtoCommerceCatalogModuleCoreModelPropertyAttribute[] | null;
  /** Gets or sets the catalog id that this product belongs to. */
  catalogId?: string | null;
  /** Gets or sets the category id that this product belongs to. */
  categoryId?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  dictionary?: boolean;
  displayNames?:
    | VirtoCommerceCatalogModuleCoreModelPropertyDisplayName[]
    | null;
  /** @format int32 */
  displayOrder?: number | null;
  /** Gets or sets a value indicating whether this VirtoCommerce.CatalogModule.Core.Model.Property is hidden. */
  hidden?: boolean;
  id?: string | null;
  isInherited?: boolean;
  /** Gets or sets a value indicating whether user can change property metadata or remove this property. */
  readonly isManageable?: boolean;
  /** Gets or sets a value indicating whether this instance is new. A new property should be created on server site instead of trying to update it. */
  isNew?: boolean;
  /** Gets or sets a value indicating whether user can change property value. */
  isReadOnly?: boolean;
  measureId?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  multilanguage?: boolean;
  multivalue?: boolean;
  name?: string | null;
  outerId?: string | null;
  ownerName?: string | null;
  propertyGroupId?: string | null;
  required?: boolean;
  type?: VirtoCommerceCatalogModuleCoreModelPropertyType;
  /** Represents property validation rules definition */
  readonly validationRule?: VirtoCommerceCatalogModuleCoreModelPropertyValidationRule | null;
  validationRules?:
    | VirtoCommerceCatalogModuleCoreModelPropertyValidationRule[]
    | null;
  valueType?: VirtoCommerceCatalogModuleCoreModelPropertyValueType;
  values?: VirtoCommerceCatalogModuleCoreModelPropertyValue[] | null;
}

export interface VirtoCommerceCatalogModuleCoreModelPropertyAttribute {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  propertyId?: string | null;
  value?: string | null;
}

export interface VirtoCommerceCatalogModuleCoreModelPropertyDictionaryItem {
  alias?: string | null;
  colorCode?: string | null;
  id?: string | null;
  localizedValues?:
    | VirtoCommerceCatalogModuleCoreModelPropertyDictionaryItemLocalizedValue[]
    | null;
  propertyId?: string | null;
  /** @format int32 */
  sortOrder?: number;
}

export interface VirtoCommerceCatalogModuleCoreModelPropertyDictionaryItemLocalizedValue {
  languageCode?: string | null;
  value?: string | null;
}

export interface VirtoCommerceCatalogModuleCoreModelPropertyDisplayName {
  languageCode?: string | null;
  name?: string | null;
}

export interface VirtoCommerceCatalogModuleCoreModelPropertyGroup {
  catalogId?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  /** @format int32 */
  displayOrder?: number;
  id?: string | null;
  localizedDescription?: VirtoCommercePlatformCoreCommonLocalizedString | null;
  localizedName?: VirtoCommercePlatformCoreCommonLocalizedString | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
}

export interface VirtoCommerceCatalogModuleCoreModelPropertyGroupSearchCriteria {
  catalogId?: string | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceCatalogModuleCoreModelPropertyGroupSearchResult {
  results?: VirtoCommerceCatalogModuleCoreModelPropertyGroup[] | null;
  /** @format int32 */
  totalCount?: number;
}

export type VirtoCommerceCatalogModuleCoreModelPropertyType =
  | "Product"
  | "Variation"
  | "Category"
  | "Catalog";

/** Property name validation data */
export interface VirtoCommerceCatalogModuleCoreModelPropertyValidationRequest {
  name?: string | null;
  originalName?: string | null;
  productId?: string | null;
}

/** Represents property validation rules definition */
export interface VirtoCommerceCatalogModuleCoreModelPropertyValidationRule {
  /**
   * Upper chars count border or null if no defined
   * @format int32
   */
  charCountMax?: number | null;
  /**
   * Down chars count border or null if no defined
   * @format int32
   */
  charCountMin?: number | null;
  id?: string | null;
  /** Uniquie value flag constrain */
  isUnique?: boolean;
  propertyId?: string | null;
  /** Custom regular expression */
  regExp?: string | null;
}

export interface VirtoCommerceCatalogModuleCoreModelPropertyValue {
  alias?: string | null;
  colorCode?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  /** @format int32 */
  displayOrder?: number | null;
  id?: string | null;
  isInherited?: boolean;
  languageCode?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  outerId?: string | null;
  propertyId?: string | null;
  readonly propertyMultivalue?: boolean;
  propertyName?: string | null;
  unitOfMeasureId?: string | null;
  value?: object | null;
  valueId?: string | null;
  valueType?: VirtoCommerceCatalogModuleCoreModelPropertyValueType;
}

export type VirtoCommerceCatalogModuleCoreModelPropertyValueType =
  | "ShortText"
  | "LongText"
  | "Number"
  | "DateTime"
  | "Boolean"
  | "Integer"
  | "GeoPoint"
  | "Html"
  | "Measure"
  | "Color";

export interface VirtoCommerceCatalogModuleCoreModelSearchAggregation {
  /** Gets or sets the value of the aggregation type */
  aggregationType?: string | null;
  /** Gets or sets the value of the aggregation field */
  field?: string | null;
  /** Gets or sets the collection of the aggregation items */
  items?: VirtoCommerceCatalogModuleCoreModelSearchAggregationItem[] | null;
  /** Gets or sets the collection of the aggregation labels */
  labels?: VirtoCommerceCatalogModuleCoreModelSearchAggregationLabel[] | null;
  /** Statistics for range aggregations, such as "PriceRange" or "Range". */
  statistics?: VirtoCommerceCatalogModuleCoreModelSearchAggregationStatistics | null;
  /** Gets or sets the type of "Attribute" aggregation type value sorting (if the aggregation was resolved via browse filters) */
  termValuesSortingType?: string | null;
}

export interface VirtoCommerceCatalogModuleCoreModelSearchAggregationItem {
  /**
   * Gets or sets the aggregation item count
   * @format int32
   */
  count?: number;
  /** Is lower bound for range included */
  includeLower?: boolean;
  /** Is upper bound for range included */
  includeUpper?: boolean;
  /** Gets or sets the flag for aggregation item is applied */
  isApplied?: boolean;
  /** Gets or sets the collection of the aggregation item labels */
  labels?: VirtoCommerceCatalogModuleCoreModelSearchAggregationLabel[] | null;
  /** Gets or sets the request lower bound for range aggregation value */
  requestedLowerBound?: string | null;
  /** Gets or sets the request lower bound for range aggregation value */
  requestedUpperBound?: string | null;
  /** Gets or sets the aggregation item value */
  value?: object | null;
}

export interface VirtoCommerceCatalogModuleCoreModelSearchAggregationLabel {
  label?: string | null;
  language?: string | null;
}

export interface VirtoCommerceCatalogModuleCoreModelSearchAggregationStatistics {
  /** @format double */
  max?: number | null;
  /** @format double */
  min?: number | null;
}

export interface VirtoCommerceCatalogModuleCoreModelSearchAutomaticLinkQuerySearchCriteria {
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
  targetCategoryId?: string | null;
}

export interface VirtoCommerceCatalogModuleCoreModelSearchAutomaticLinkQuerySearchResult {
  results?: VirtoCommerceCatalogModuleCoreModelAutomaticLinkQuery[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceCatalogModuleCoreModelSearchCatalogListEntrySearchCriteria {
  catalogId?: string | null;
  catalogIds?: string[] | null;
  categoryId?: string | null;
  categoryIds?: string[] | null;
  code?: string | null;
  /** Exclude a specified product type from the search */
  excludeProductType?: string | null;
  excludeProductTypes?: string[] | null;
  hideDirectLinkedCategories?: boolean;
  keyword?: string | null;
  languageCode?: string | null;
  /** Search within variations of specified main product */
  mainProductId?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  onlyBuyable?: boolean | null;
  onlyWithTrackingInventory?: boolean | null;
  /** Search product with specified type */
  productType?: string | null;
  productTypes?: string[] | null;
  responseGroup?: string | null;
  /** Search  in all children categories for specified catalog or categories */
  searchInChildren?: boolean;
  /** Also search in variations */
  searchInVariations?: boolean;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
  /** Search by vendor */
  vendorId?: string | null;
  vendorIds?: string[] | null;
  withHidden?: boolean;
}

export interface VirtoCommerceCatalogModuleCoreModelSearchCatalogSearchCriteria {
  catalogIds?: string[] | null;
  isVirtual?: boolean | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  outerIds?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceCatalogModuleCoreModelSearchCatalogSearchResult {
  results?: VirtoCommerceCatalogModuleCoreModelCatalog[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceCatalogModuleCoreModelSearchCategoryIndexedSearchCriteria {
  catalogId?: string | null;
  catalogIds?: string[] | null;
  /** Allows to retrieve only a specific set of fields in the result hits */
  includeFields?: string[] | null;
  /** Enable fuzzy search, i.e. allow to search color:white even if color:wihte actually passed to criteria */
  isFuzzySearch?: boolean;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  /** CategoryId1/CategoryId2, no catalog should be included in the outline */
  outline?: string | null;
  /** CategoryId1/CategoryId2, no catalog should be included in the outline */
  outlines?: string[] | null;
  /** Gets or sets the search provider specific raw search query; all other search criteria will be ignored */
  rawQuery?: string | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  storeId?: string | null;
  /** @format int32 */
  take?: number;
  /** Term format: name:value1,value2 */
  terms?: string[] | null;
  /** Assigned groups for current user. Data format: user_groups:value1,value2 */
  userGroups?: string[] | null;
}

export interface VirtoCommerceCatalogModuleCoreModelSearchCategoryIndexedSearchResult {
  aggregations?: VirtoCommerceCatalogModuleCoreModelSearchAggregation[] | null;
  items?: VirtoCommerceCatalogModuleCoreModelCategory[] | null;
  /** @format int64 */
  totalCount?: number;
}

export interface VirtoCommerceCatalogModuleCoreModelSearchLinkSearchCriteria {
  catalogIds?: string[] | null;
  categoryIds?: string[] | null;
  isAutomatic?: boolean | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceCatalogModuleCoreModelSearchListEntrySearchResult {
  /** Gets or sets the list entries. */
  readonly listEntries?:
    | VirtoCommerceCatalogModuleCoreModelListEntryListEntryBase[]
    | null;
  results?: VirtoCommerceCatalogModuleCoreModelListEntryListEntryBase[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceCatalogModuleCoreModelSearchMeasureSearchCriteria {
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceCatalogModuleCoreModelSearchMeasureSearchResult {
  results?: VirtoCommerceCatalogModuleCoreModelMeasure[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceCatalogModuleCoreModelSearchProductAssociationSearchCriteria {
  associatedObjectIds?: string[] | null;
  group?: string | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  tags?: string[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceCatalogModuleCoreModelSearchProductAssociationSearchResult {
  results?: VirtoCommerceCatalogModuleCoreModelProductAssociation[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceCatalogModuleCoreModelSearchProductConfigurationSearchCriteria {
  isActive?: boolean | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  productId?: string | null;
  productIds?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceCatalogModuleCoreModelSearchProductConfigurationSearchResult {
  results?:
    | VirtoCommerceCatalogModuleCoreModelConfigurationProductConfiguration[]
    | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceCatalogModuleCoreModelSearchProductIndexedSearchCriteria {
  catalogId?: string | null;
  catalogIds?: string[] | null;
  /**
   * Defines the date to be used for filtering products. The date must be in UTC format as that is format indexes are stored in.
   * @format date-time
   */
  certainDate?: string | null;
  /** Gets or sets the class types. */
  classTypes?: string[] | null;
  currency?: string | null;
  /**
   * Gets or sets the end date. The date must be in UTC format as that is format indexes are stored in.
   * @format date-time
   */
  endDate?: string | null;
  /** Gets or sets a "black" list of aggregation keys that identify preconfigured aggregations, which SHOULD NOT be calculated and returned with the search result. */
  excludeAggregations?: string[] | null;
  /** Geo distance filter */
  geoDistanceFilter?: VirtoCommerceSearchModuleCoreModelGeoDistanceFilter | null;
  /** Gets or sets a "white" list of aggregation keys that identify preconfigured aggregations, which SHOULD be calculated and returned with the search result. */
  includeAggregations?: string[] | null;
  /** Allows to retrieve only a specific set of fields in the result hits */
  includeFields?: string[] | null;
  /** Enable fuzzy search, i.e. allow to search color:white even if color:wihte actually passed to criteria */
  isFuzzySearch?: boolean;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  /** CategoryId1/CategoryId2, no catalog should be included in the outline */
  outline?: string | null;
  /** CategoryId1/CategoryId2, no catalog should be included in the outline */
  outlines?: string[] | null;
  priceRange?: VirtoCommerceSearchModuleCoreModelNumericRange | null;
  pricelists?: string[] | null;
  /** Physical, Digital, etc. */
  productType?: string | null;
  /** Gets or sets the search provider specific raw search query; all other search criteria will be ignored */
  rawQuery?: string | null;
  responseGroup?: string | null;
  /** Include product variations in result */
  searchInVariations?: boolean;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  /** Override base SortInfo property to support GeoSortInfo sorting types */
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /**
   * Gets or sets the start date. The date must be in UTC format as that is format indexes are stored in.
   * @format date-time
   */
  startDate?: string;
  /**
   * Gets or sets the start date from filter. Used for filtering new products. The date must be in UTC format as that is format indexes are stored in.
   * @format date-time
   */
  startDateFrom?: string | null;
  storeId?: string | null;
  /** @format int32 */
  take?: number;
  /** Term format: name:value1,value2 */
  terms?: string[] | null;
  /** Assigned groups for current user. Data format: user_groups:value1,value2 */
  userGroups?: string[] | null;
  /** Specifies if we search for hidden products. */
  withHidden?: boolean;
}

export interface VirtoCommerceCatalogModuleCoreModelSearchProductIndexedSearchResult {
  aggregations?: VirtoCommerceCatalogModuleCoreModelSearchAggregation[] | null;
  items?: VirtoCommerceCatalogModuleCoreModelCatalogProduct[] | null;
  /** @format int64 */
  totalCount?: number;
}

/** Search criteria used for search property dictionary items */
export interface VirtoCommerceCatalogModuleCoreModelSearchPropertyDictionaryItemSearchCriteria {
  catalogIds?: string[] | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  propertyIds?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceCatalogModuleCoreModelSearchPropertyDictionaryItemSearchResult {
  results?: VirtoCommerceCatalogModuleCoreModelPropertyDictionaryItem[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceCatalogModuleCoreModelSearchVideoSearchCriteria {
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  ownerIds?: string[] | null;
  ownerType?: string | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceCatalogModuleCoreModelSearchVideoSearchResult {
  results?: VirtoCommerceCatalogModuleCoreModelVideo[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceCatalogModuleCoreModelVariation {
  assets?: VirtoCommerceCatalogModuleCoreModelAsset[] | null;
  associations?: VirtoCommerceCatalogModuleCoreModelProductAssociation[] | null;
  /** The ID of the catalog to which this product belongs. */
  catalogId?: string | null;
  /** The ID of the category to which this product belongs. */
  categoryId?: string | null;
  /** The Stock Keeping Unit (SKU) code for the product. */
  code?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  /**
   * The date and time when the download link or access to the product will expire.
   * @format date-time
   */
  downloadExpiration?: string | null;
  /** The type of product download. Valid values include: "Standard Product", "Software", and "Music". */
  downloadType?: string | null;
  enableReview?: boolean | null;
  /**
   * Listing expires on the specific date and time. If you do not specify an end date, the product will be active until you deactivate it.
   * @format date-time
   */
  endDate?: string | null;
  excludedProperties?:
    | VirtoCommerceCatalogModuleCoreModelExcludedProperty[]
    | null;
  /** The Global Trade Item Number (GTIN) for the product. This can include UPC (in North America), EAN (in Europe), JAN (in Japan), and ISBN (for books). */
  gtin?: string | null;
  /** Indicates whether the product requires the user to agree to any terms or conditions before downloading. */
  hasUserAgreement?: boolean | null;
  /**
   * The height of the product, in the unit specified by the MeasureUnit property.
   * @format double
   */
  height?: number | null;
  id?: string | null;
  images?: VirtoCommerceCatalogModuleCoreModelImage[] | null;
  /** Gets the default image for the product. */
  readonly imgSrc?: string | null;
  /**
   * The date and time when the product was last indexed for search.
   * @format date-time
   */
  indexingDate?: string | null;
  /**
   * Specifies whether the product is currently visible on the store for customers to view and purchase.
   * If set to false, the product is currently sold out.
   */
  isActive?: boolean | null;
  /**
   * Specifies whether the product is currently visible on the store for customers to view and purchase.
   * If set to false, the product is currently ouf of stock.
   */
  isBuyable?: boolean | null;
  /** System flag used to mark that object was inherited from other */
  readonly isInherited?: boolean;
  /**
   * The length of the product, in the unit specified by the MeasureUnit property.
   * @format double
   */
  length?: number | null;
  links?: VirtoCommerceCatalogModuleCoreModelCategoryLink[] | null;
  localizedName?: VirtoCommercePlatformCoreCommonLocalizedString | null;
  /** The ID of the main product associated with this product variation. */
  mainProductId?: string | null;
  /** A manufacturer part number (MPN) is a unique alphanumeric code assigned by a manufacturer to identify a specific product or component. It is used primarily for part tracking in inventory management, supply chain operations, and ordering purposes. */
  manufacturerPartNumber?: string | null;
  /**
   * The maximum number of times the product can be downloaded. A value of 0 indicates no limit.
   * @format int32
   */
  maxNumberOfDownload?: number | null;
  /**
   * The maximum quantity of the product that can be purchased in a single order. A value of 0 indicates that there are no limitations on the maximum quantity.
   * @format int32
   */
  maxQuantity?: number | null;
  /** The unit of measurement for the product's height, length, and width. */
  measureUnit?: string | null;
  /**
   * The minimum quantity of the product that must be purchased in a single order. A value of 0 indicates that there are no limitations on the minimum quantity.
   * @format int32
   */
  minQuantity?: number | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  /** The name of the product. */
  name?: string | null;
  /** An external identifier for the product that can be used for integration with external systems. */
  outerId?: string | null;
  /** Product outline in physical catalog (all parent categories ids concatenated. E.g. (1/21/344)) */
  readonly outline?: string | null;
  outlines?: VirtoCommerceCatalogModuleCoreOutlinesOutline[] | null;
  /**
   * Defines the number of items in a package. Quantity step for your product's. Default value is 1.
   * @format int32
   */
  packSize?: number;
  /** The type of package for this product, which determines the product's specific dimensions. */
  packageType?: string | null;
  readonly parentCategoryIsActive?: boolean;
  /** Product path in physical catalog (all parent categories names concatenated. E.g. (parent1/parent2)) */
  readonly path?: string | null;
  /**
   * Indicates the position of the product in the catalog for ordering purposes.
   * @format int32
   */
  priority?: number;
  /** The type of product. Can be "Physical", "Digital", etc. */
  productType?: string | null;
  properties?: VirtoCommerceCatalogModuleCoreModelProperty[] | null;
  referencedAssociations?:
    | VirtoCommerceCatalogModuleCoreModelProductAssociation[]
    | null;
  /** @format double */
  relevanceScore?: number | null;
  reviews?: VirtoCommerceCatalogModuleCoreModelEditorialReview[] | null;
  seoInfos?: VirtoCommerceSeoCoreModelsSeoInfo[] | null;
  /** Each descendant type should override this property to use other object type for seo records */
  readonly seoObjectType?: string | null;
  /** Specifies the type of shipping option available for the product. */
  shippingType?: string | null;
  /**
   * First listed date and time. If you do not specify an end date, the product will be active until you deactivate it.If you do not specify an end date, the product will be active until you deactivate it.If you do not specify a start date, the product will become active immediately once you save it.
   * @format date-time
   */
  startDate?: string;
  /** Specifies the type of tax applied to the product. */
  taxType?: string | null;
  readonly titularItemId?: string | null;
  /**
   * Indicates whether the inventory service is tracking the availability of this product.
   * If set to false, the product is considered in stock without any inventory limitations.
   */
  trackInventory?: boolean | null;
  variations?: VirtoCommerceCatalogModuleCoreModelVariation[] | null;
  /** ID of the vendor associated with the product. */
  vendor?: string | null;
  /**
   * The weight of the product, in the unit specified by the WeightUnit property.
   * @format double
   */
  weight?: number | null;
  /** The unit of measurement for the product's weight. */
  weightUnit?: string | null;
  /**
   * The width of the product, in the unit specified by the MeasureUnit property.
   * @format double
   */
  width?: number | null;
}

/** Video content information */
export interface VirtoCommerceCatalogModuleCoreModelVideo {
  contentUrl?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  description?: string | null;
  duration?: string | null;
  embedUrl?: string | null;
  id?: string | null;
  languageCode?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  ownerId?: string | null;
  ownerType?: string | null;
  /** @format int32 */
  sortOrder?: number;
  thumbnailUrl?: string | null;
  /** @format date-time */
  uploadDate?: string | null;
}

export interface VirtoCommerceCatalogModuleCoreModelVideoCreateRequest {
  contentUrl?: string | null;
  languageCode?: string | null;
  ownerId?: string | null;
  ownerType?: string | null;
  /** @format int32 */
  sortOrder?: number | null;
}

export interface VirtoCommerceCatalogModuleCoreModelVideoProvidersStatus {
  isVimeoAccessTokenConfigured?: boolean;
  isYouTubeApiKeyConfigured?: boolean;
}

/**
 * Represents the path from the catalog to one of the child objects (product or category):
 * catalog/parent-category1/.../parent-categoryN/object
 */
export interface VirtoCommerceCatalogModuleCoreOutlinesOutline {
  /** Outline parts */
  items?: VirtoCommerceCatalogModuleCoreOutlinesOutlineItem[] | null;
}

/** Represents one outline element: catalog, category or product. */
export interface VirtoCommerceCatalogModuleCoreOutlinesOutlineItem {
  /** True when this object is linked to the virtual parent. */
  hasVirtualParent?: boolean;
  /** Object id */
  id?: string | null;
  localizedName?: VirtoCommercePlatformCoreCommonLocalizedString | null;
  /** The name of current item */
  name?: string | null;
  /** All SEO records for the object */
  seoInfos?: VirtoCommerceSeoCoreModelsSeoInfo[] | null;
  /** Object type */
  seoObjectType?: string | null;
}

/**
 * A field that can be used in a sort clause, offered to the admin clause editor. Derived from the product index
 * schema (single-valued filterable fields) plus a few logical tokens, never a hand-maintained list.
 */
export interface VirtoCommerceCatalogModuleCoreSearchSortingProductSortableField {
  /** Field data type hint (the index field value type, or `Virtual` for logical tokens with no single physical field). */
  dataType?: string | null;
  /** Logical field name to use in a clause (e.g. `name`, `priority`, `createddate`, `price`, `__score`). */
  name?: string | null;
}

/**
 * An effective, composed sorting: the code default merged with the store-level admin override.
 * This is the projection returned to the admin UI and (filtered to visible) to the storefront via GraphQL.
 */
export interface VirtoCommerceCatalogModuleCoreSearchSortingProductSorting {
  /** Whether the admin may override name/order/visibility (mirrors the resolver flag; always true for custom sortings). */
  allowOverride?: boolean;
  /** Effective clauses (for the clause editor and the resolved-expression preview). */
  clauses?: VirtoCommerceCatalogModuleCoreSearchSortingSortClause[] | null;
  /** Stable key used in the API and storefront URL (`?sort=<code>`). */
  code?: string | null;
  /** True when this sorting was authored entirely in the admin UI (no backing code resolver). Only custom sortings can be deleted. */
  isCustom?: boolean;
  /** True for the sorting applied when the incoming sort is empty (the first visible sorting by VirtoCommerce.CatalogModule.Core.Search.Sorting.ProductSorting.Order). Computed. */
  isDefault?: boolean;
  /** Whether the clause editor is editable for this sorting (mirrors the resolver flag; always true for custom sortings). */
  isExpressionEditable?: boolean;
  isVisible?: boolean;
  /** Culture -> name. Admin-owned; the storefront resolves `LocalizedNames[culture] ?? Name`. */
  localizedNames?: Record<string, string | null>;
  /** Effective invariant/base display name. */
  name?: string | null;
  /**
   * Effective position in the dropdown.
   * @format int32
   */
  order?: number;
  /**
   * Effective logical sort expression (e.g. `price:desc`). For clause-based sortings this equals the serialized
   * VirtoCommerce.CatalogModule.Core.Search.Sorting.ProductSorting.Clauses; for computed resolvers it is the resolver output.
   */
  sortExpression?: string | null;
}

/**
 * A single sort instruction: a logical field name and a direction.
 * "Logical" means the field is written as it would be in a sort expression (e.g. `price`, `name`,
 * `priority`) and is bound to the physical index field by the search-request builder
 * (e.g. `price` -> `price_usd`, `name` -> `name_en-us`).
 */
export interface VirtoCommerceCatalogModuleCoreSearchSortingSortClause {
  field?: string | null;
  isDescending?: boolean;
}

/** Information to search and create links to categories and items */
export interface VirtoCommerceCatalogModuleWebModelBulkLinkCreationRequest {
  /** The target catalog identifier for the link */
  catalogId?: string | null;
  /** The target category identifier for the link */
  categoryId?: string | null;
  searchCriteria?: VirtoCommerceCatalogModuleCoreModelSearchCatalogListEntrySearchCriteria | null;
}

export interface VirtoCommerceCatalogPersonalizationModuleCoreModelSearchTaggedItemSearchCriteria {
  /** @format date-time */
  changedFrom?: string | null;
  entityId?: string | null;
  entityIds?: string[] | null;
  entityType?: string | null;
  ids?: string[] | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceCatalogPersonalizationModuleCoreModelSearchTaggedItemSearchResult {
  results?:
    | VirtoCommerceCatalogPersonalizationModuleCoreModelTaggedItem[]
    | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceCatalogPersonalizationModuleCoreModelTaggedItem {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  entityId?: string | null;
  entityType?: string | null;
  id?: string | null;
  inheritedTags?: string[] | null;
  label?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  outlines?:
    | VirtoCommerceCatalogPersonalizationModuleCoreModelTaggedItemOutline[]
    | null;
  tags?: string[] | null;
}

export interface VirtoCommerceCatalogPersonalizationModuleCoreModelTaggedItemOutline {
  id?: string | null;
  outline?: string | null;
  taggedItem?: VirtoCommerceCatalogPersonalizationModuleCoreModelTaggedItem | null;
  taggedItemId?: string | null;
}

export interface VirtoCommerceCatalogPersonalizationModuleCoreModelTaggedItemOutlineSyncPushNotification {
  /** @format date-time */
  created?: string;
  creator?: string | null;
  description?: string | null;
  /** @format int64 */
  readonly errorCount?: number;
  errors?: string[] | null;
  /** @format date-time */
  finished?: string | null;
  id?: string | null;
  isNew?: boolean;
  jobId?: string | null;
  notifyType?: string | null;
  /** @format int64 */
  processedCount?: number;
  /** @format int32 */
  repeatCount?: number;
  serverId?: string | null;
  title?: string | null;
  /** @format int64 */
  totalCount?: number;
}

export interface VirtoCommerceCatalogPersonalizationModuleWebModelTaggedItemOutlinesSynchronizationRequest {
  jobId?: string | null;
}

/** Completeness channel is a provider of completeness of specified catalog */
export interface VirtoCommerceCatalogPublishingModuleCoreModelCompletenessChannel {
  catalogId?: string | null;
  catalogName?: string | null;
  /** @format double */
  completenessPercent?: number | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  currencies?: string[] | null;
  evaluatorType?: string | null;
  id?: string | null;
  languages?: string[] | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
}

/** Completeness detail is a value of completeness per feature, i.e. completeness of product properties, completeness of product prices, etc. */
export interface VirtoCommerceCatalogPublishingModuleCoreModelCompletenessDetail {
  /** @format double */
  completenessPercent?: number;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  productId?: string | null;
}

/** Completeness entriy is a value of completeness per product */
export interface VirtoCommerceCatalogPublishingModuleCoreModelCompletenessEntry {
  channelId?: string | null;
  /** @format double */
  completenessPercent?: number;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  details?:
    | VirtoCommerceCatalogPublishingModuleCoreModelCompletenessDetail[]
    | null;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  productId?: string | null;
}

export interface VirtoCommerceCatalogPublishingModuleCoreModelSearchCompletenessChannelSearchCriteria {
  catalogIds?: string[] | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceCatalogPublishingModuleCoreModelSearchCompletenessChannelSearchResult {
  catalogIds?: string[] | null;
  results?:
    | VirtoCommerceCatalogPublishingModuleCoreModelCompletenessChannel[]
    | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceCatalogPublishingModuleWebModelEvaluateCompletenessNotification {
  completeness?:
    | VirtoCommerceCatalogPublishingModuleCoreModelCompletenessEntry[]
    | null;
  /** @format date-time */
  created?: string;
  creator?: string | null;
  description?: string | null;
  /** @format int64 */
  readonly errorCount?: number;
  errors?: string[] | null;
  /** @format date-time */
  finished?: string | null;
  id?: string | null;
  isNew?: boolean;
  notifyType?: string | null;
  /** @format int64 */
  processedCount?: number;
  /** @format int32 */
  repeatCount?: number;
  serverId?: string | null;
  title?: string | null;
  /** @format int64 */
  totalCount?: number;
}

export interface VirtoCommerceContentModuleCoreModelContentFolder {
  /** @format date-time */
  createdDate?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  parentUrl?: string | null;
  relativeUrl?: string | null;
  type?: string | null;
  url?: string | null;
}

export interface VirtoCommerceContentModuleCoreModelContentItem {
  /** @format date-time */
  createdDate?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  parentUrl?: string | null;
  relativeUrl?: string | null;
  type?: string | null;
  url?: string | null;
}

export interface VirtoCommerceContentModuleCoreModelContentSearchCriteria {
  /** @format date-time */
  activeOn?: string | null;
  contentType?: string | null;
  cultureName?: string | null;
  folderUrl?: string | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  organizationId?: string | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  storeId?: string | null;
  /** @format int32 */
  take?: number;
  userGroups?: string[] | null;
}

export interface VirtoCommerceContentModuleCoreModelContentStatistic {
  activeThemeName?: string | null;
  /** @format int32 */
  blogsCount?: number;
  /** @format int32 */
  pagesCount?: number;
  /** @format int32 */
  themesCount?: number;
}

export interface VirtoCommerceContentModuleCoreModelFilePublishStatus {
  hasChanges?: boolean;
  published?: boolean;
}

export interface VirtoCommerceContentModuleCoreModelMenuLink {
  associatedObjectId?: string | null;
  associatedObjectName?: string | null;
  associatedObjectType?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  menuLinkListId?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  outerId?: string | null;
  /** @format int32 */
  priority?: number;
  securityScopes?: string[] | null;
  title?: string | null;
  url?: string | null;
}

export interface VirtoCommerceContentModuleCoreModelMenuLinkList {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  language?: string | null;
  menuLinks?: VirtoCommerceContentModuleCoreModelMenuLink[] | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  outerId?: string | null;
  securityScopes?: string[] | null;
  storeId?: string | null;
}

export interface VirtoCommerceCoreModuleCoreCommonAddress {
  line1?: string | null;
  line2?: string | null;
  addressType?: VirtoCommerceCoreModuleCoreCommonAddressType;
  city?: string | null;
  countryCode?: string | null;
  countryName?: string | null;
  description?: string | null;
  email?: string | null;
  firstName?: string | null;
  isDefault?: boolean;
  key?: string | null;
  lastName?: string | null;
  middleName?: string | null;
  name?: string | null;
  organization?: string | null;
  outerId?: string | null;
  phone?: string | null;
  postalCode?: string | null;
  regionId?: string | null;
  regionName?: string | null;
  zip?: string | null;
}

export type VirtoCommerceCoreModuleCoreCommonAddressType =
  | "Undefined"
  | "Billing"
  | "Shipping"
  | "BillingAndShipping"
  | "Pickup";

export interface VirtoCommerceCoreModuleCoreCommonDiscount {
  coupon?: string | null;
  currency?: string | null;
  description?: string | null;
  /** @format double */
  discountAmount?: number;
  /** @format double */
  discountAmountWithTax?: number;
  id?: string | null;
  name?: string | null;
  promotionId?: string | null;
}

export interface VirtoCommerceCoreModuleCoreCommonIOperation {
  childrenOperations?: VirtoCommerceCoreModuleCoreCommonIOperation[] | null;
  comment?: string | null;
  currency?: string | null;
  id?: string | null;
  isApproved?: boolean;
  number?: string | null;
  operationType?: string | null;
  parentOperationId?: string | null;
  status?: string | null;
}

export interface VirtoCommerceCoreModuleCoreConditionsIConditionTree {
  /** List of all available children for current tree node (is used in expression designer) */
  readonly availableChildren?:
    | VirtoCommerceCoreModuleCoreConditionsIConditionTree[]
    | null;
  readonly children?:
    | VirtoCommerceCoreModuleCoreConditionsIConditionTree[]
    | null;
  readonly id?: string | null;
}

/** Currency */
export interface VirtoCommerceCoreModuleCoreCurrencyCurrency {
  /** Currency code may be used ISO 4217. */
  code?: string | null;
  cultureName?: string | null;
  /** Custom formatting pattern */
  customFormatting?: string | null;
  /** @format int32 */
  decimalDigits?: number;
  englishName?: string | null;
  /**
   * The exchange rate against the primary exchange rate of the currency.
   * @format double
   */
  exchangeRate?: number;
  /** Flag specifies that this is the primary currency */
  isPrimary?: boolean;
  midpointRounding?: string | null;
  /** name of the currency */
  name?: string | null;
  roundingType?: string | null;
  /** Currency symbol */
  symbol?: string | null;
}

/** Represent predefined dimensions package type */
export interface VirtoCommerceCoreModuleCorePackagePackageType {
  /** @format double */
  height?: number;
  id?: string | null;
  /** @format double */
  length?: number;
  measureUnit?: string | null;
  /** Package type name */
  name?: string | null;
  /** @format double */
  width?: number;
}

export interface VirtoCommerceCoreModuleCoreTaxTaxDetail {
  /** @format double */
  amount?: number;
  name?: string | null;
  /** @format double */
  rate?: number;
}

export interface VirtoCommerceCustomerModuleCoreModelContact {
  about?: string | null;
  addresses?: CustomerAddress[] | null;
  associatedOrganizations?: string[] | null;
  /** @format date-time */
  birthDate?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  currencyCode?: string | null;
  currentOrganizationId?: string | null;
  defaultBillingAddressId?: string | null;
  defaultLanguage?: string | null;
  defaultOrganizationId?: string | null;
  defaultShippingAddressId?: string | null;
  dynamicProperties?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicObjectProperty[]
    | null;
  dynamicPropertyAccessor?: any | null;
  emails?: string[] | null;
  firstName?: string | null;
  fullName?: string | null;
  groups?: string[] | null;
  iconUrl?: string | null;
  id?: string | null;
  isAnonymized?: boolean;
  lastName?: string | null;
  memberType?: string | null;
  middleName?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  notes?: VirtoCommerceCustomerModuleCoreModelNote[] | null;
  readonly objectType?: string | null;
  organizations?: string[] | null;
  outerId?: string | null;
  phones?: string[] | null;
  photoUrl?: string | null;
  preferredCommunication?: string | null;
  preferredDelivery?: string | null;
  /** @format double */
  relevanceScore?: number | null;
  salutation?: string | null;
  securityAccounts?: VirtoCommercePlatformCoreSecurityApplicationUser[] | null;
  seoInfos?: VirtoCommerceSeoCoreModelsSeoInfo[] | null;
  readonly seoObjectType?: string | null;
  status?: string | null;
  taxPayerId?: string | null;
  timeZone?: string | null;
  useDynamicPropertyAccessor?: boolean;
}

export interface VirtoCommerceCustomerModuleCoreModelCustomerPreference {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  userId?: string | null;
  value?: string | null;
}

export interface VirtoCommerceCustomerModuleCoreModelCustomerPreferenceSearchCriteria {
  keyword?: string | null;
  languageCode?: string | null;
  name?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
  userId?: string | null;
}

export interface VirtoCommerceCustomerModuleCoreModelCustomerPreferenceSearchResult {
  results?: VirtoCommerceCustomerModuleCoreModelCustomerPreference[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceCustomerModuleCoreModelCustomerRole {
  description?: string | null;
  id?: string | null;
  name?: string | null;
}

export interface VirtoCommerceCustomerModuleCoreModelCustomerRoleSearchResult {
  results?: VirtoCommerceCustomerModuleCoreModelCustomerRole[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceCustomerModuleCoreModelEmployee {
  addresses?: CustomerAddress[] | null;
  /** @format date-time */
  birthDate?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  currentOrganizationId?: string | null;
  defaultLanguage?: string | null;
  defaultOrganizationId?: string | null;
  dynamicProperties?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicObjectProperty[]
    | null;
  dynamicPropertyAccessor?: any | null;
  emails?: string[] | null;
  employeeType?: string | null;
  firstName?: string | null;
  fullName?: string | null;
  groups?: string[] | null;
  iconUrl?: string | null;
  id?: string | null;
  isActive?: boolean;
  lastName?: string | null;
  memberType?: string | null;
  middleName?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  notes?: VirtoCommerceCustomerModuleCoreModelNote[] | null;
  readonly objectType?: string | null;
  organizations?: string[] | null;
  outerId?: string | null;
  phones?: string[] | null;
  photoUrl?: string | null;
  /** @format double */
  relevanceScore?: number | null;
  salutation?: string | null;
  securityAccounts?: VirtoCommercePlatformCoreSecurityApplicationUser[] | null;
  seoInfos?: VirtoCommerceSeoCoreModelsSeoInfo[] | null;
  readonly seoObjectType?: string | null;
  status?: string | null;
  timeZone?: string | null;
  useDynamicPropertyAccessor?: boolean;
}

export interface VirtoCommerceCustomerModuleCoreModelInviteCustomerError {
  code?: string | null;
  description?: string | null;
  email?: string | null;
  parameter?: string | null;
}

export interface VirtoCommerceCustomerModuleCoreModelInviteCustomerRequest {
  additionalParameters?: Record<string, string | null>;
  cultureName?: string | null;
  emails?: string[] | null;
  message?: string | null;
  organizationId?: string | null;
  roleIds?: string[] | null;
  storeId?: string | null;
  urlSuffix?: string | null;
}

export interface VirtoCommerceCustomerModuleCoreModelInviteCustomerResult {
  errors?: VirtoCommerceCustomerModuleCoreModelInviteCustomerError[] | null;
  succeeded?: boolean;
}

export interface VirtoCommerceCustomerModuleCoreModelLockMembershipRequest {
  /** @format date-time */
  lockoutEnd?: string | null;
}

export interface VirtoCommerceCustomerModuleCoreModelMember {
  addresses?: CustomerAddress[] | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  dynamicProperties?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicObjectProperty[]
    | null;
  dynamicPropertyAccessor?: any | null;
  emails?: string[] | null;
  groups?: string[] | null;
  iconUrl?: string | null;
  id?: string | null;
  memberType?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  notes?: VirtoCommerceCustomerModuleCoreModelNote[] | null;
  readonly objectType?: string | null;
  outerId?: string | null;
  phones?: string[] | null;
  /** @format double */
  relevanceScore?: number | null;
  seoInfos?: VirtoCommerceSeoCoreModelsSeoInfo[] | null;
  readonly seoObjectType?: string | null;
  status?: string | null;
  useDynamicPropertyAccessor?: boolean;
}

export interface VirtoCommerceCustomerModuleCoreModelNote {
  body?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  outerId?: string | null;
  title?: string | null;
}

export interface VirtoCommerceCustomerModuleCoreModelOrganization {
  addresses?: CustomerAddress[] | null;
  businessCategory?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  description?: string | null;
  dynamicProperties?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicObjectProperty[]
    | null;
  dynamicPropertyAccessor?: any | null;
  emails?: string[] | null;
  groups?: string[] | null;
  iconUrl?: string | null;
  id?: string | null;
  memberType?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  notes?: VirtoCommerceCustomerModuleCoreModelNote[] | null;
  readonly objectType?: string | null;
  outerId?: string | null;
  ownerId?: string | null;
  parentId?: string | null;
  phones?: string[] | null;
  /** @format double */
  relevanceScore?: number | null;
  roles?: VirtoCommerceCustomerModuleCoreModelOrganizationRole[] | null;
  seoInfos?: VirtoCommerceSeoCoreModelsSeoInfo[] | null;
  readonly seoObjectType?: string | null;
  status?: string | null;
  useDynamicPropertyAccessor?: boolean;
}

export interface VirtoCommerceCustomerModuleCoreModelOrganizationMembership {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  readonly isCurrentlyLocked?: boolean;
  isLocked?: boolean;
  /** @format date-time */
  lockoutEnd?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  organizationId?: string | null;
  organizationName?: string | null;
  roles?:
    | VirtoCommerceCustomerModuleCoreModelOrganizationMembershipRole[]
    | null;
  status?: string | null;
  userId?: string | null;
}

export interface VirtoCommerceCustomerModuleCoreModelOrganizationMembershipRole {
  id?: string | null;
  membershipId?: string | null;
  roleId?: string | null;
  roleName?: string | null;
}

export interface VirtoCommerceCustomerModuleCoreModelOrganizationMembershipSearchCriteria {
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  onlyLocked?: boolean;
  onlyUnlocked?: boolean;
  organizationId?: string | null;
  organizationIds?: string[] | null;
  responseGroup?: string | null;
  roleIds?: string[] | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  statuses?: string[] | null;
  /** @format int32 */
  take?: number;
  userId?: string | null;
  userIds?: string[] | null;
}

export interface VirtoCommerceCustomerModuleCoreModelOrganizationMembershipSearchResult {
  results?: VirtoCommerceCustomerModuleCoreModelOrganizationMembership[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceCustomerModuleCoreModelOrganizationRole {
  id?: string | null;
  organizationId?: string | null;
  roleId?: string | null;
  roleName?: string | null;
}

export interface VirtoCommerceCustomerModuleCoreModelSearchContactSearchResult {
  results?: VirtoCommerceCustomerModuleCoreModelContact[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceCustomerModuleCoreModelSearchMemberSearchResult {
  results?: VirtoCommerceCustomerModuleCoreModelMember[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceCustomerModuleCoreModelSearchMembersSearchCriteria {
  deepSearch?: boolean;
  excludedObjectIds?: string[] | null;
  group?: string | null;
  groups?: string[] | null;
  keyword?: string | null;
  languageCode?: string | null;
  memberId?: string | null;
  memberIds?: string[] | null;
  memberType?: string | null;
  memberTypes?: string[] | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  outerIds?: string[] | null;
  responseGroup?: string | null;
  rootMembersOnly?: boolean | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceCustomerModuleCoreModelSearchOrganizationSearchResult {
  results?: VirtoCommerceCustomerModuleCoreModelOrganization[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceCustomerModuleCoreModelSearchVendorSearchResult {
  results?: VirtoCommerceCustomerModuleCoreModelVendor[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceCustomerModuleCoreModelVendor {
  addresses?: CustomerAddress[] | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  description?: string | null;
  dynamicProperties?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicObjectProperty[]
    | null;
  dynamicPropertyAccessor?: any | null;
  emails?: string[] | null;
  groupName?: string | null;
  groups?: string[] | null;
  iconUrl?: string | null;
  id?: string | null;
  logoUrl?: string | null;
  memberType?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  notes?: VirtoCommerceCustomerModuleCoreModelNote[] | null;
  readonly objectType?: string | null;
  outerId?: string | null;
  phones?: string[] | null;
  /** @format double */
  relevanceScore?: number | null;
  securityAccounts?: VirtoCommercePlatformCoreSecurityApplicationUser[] | null;
  seoInfos?: VirtoCommerceSeoCoreModelsSeoInfo[] | null;
  readonly seoObjectType?: string | null;
  siteUrl?: string | null;
  status?: string | null;
  useDynamicPropertyAccessor?: boolean;
}

export interface VirtoCommerceEventBusModuleCoreModelsProviderConnection {
  connectionOptionsSerialized?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  providerName?: string | null;
}

export interface VirtoCommerceEventBusModuleCoreModelsProviderConnectionLog {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  errorMessage?: string | null;
  errorPayload?: string | null;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  providerName?: string | null;
  /** @format int32 */
  status?: number;
}

export interface VirtoCommerceEventBusModuleCoreModelsProviderConnectionLogSearchCriteria {
  /** @format date-time */
  endCreatedDate?: string | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  providerConnectionName?: string | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format date-time */
  startCreatedDate?: string | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceEventBusModuleCoreModelsProviderConnectionLogSearchResult {
  results?: VirtoCommerceEventBusModuleCoreModelsProviderConnectionLog[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceEventBusModuleCoreModelsProviderConnectionRequest {
  connectionOptionsSerialized?: string | null;
  name?: string | null;
  providerName?: string | null;
}

export interface VirtoCommerceEventBusModuleCoreModelsProviderConnectionSearchCriteria {
  keyword?: string | null;
  languageCode?: string | null;
  name?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  providerName?: string | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceEventBusModuleCoreModelsProviderConnectionSearchResult {
  results?: VirtoCommerceEventBusModuleCoreModelsProviderConnection[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceEventBusModuleCoreModelsSubscription {
  connectionName?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  eventSettingsSerialized?: string | null;
  events?: VirtoCommerceEventBusModuleCoreModelsSubscriptionEvent[] | null;
  id?: string | null;
  jsonPathFilter?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  payloadTransformationTemplate?: string | null;
}

export interface VirtoCommerceEventBusModuleCoreModelsSubscriptionEvent {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  eventId?: string | null;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  subscriptionId?: string | null;
}

export interface VirtoCommerceEventBusModuleCoreModelsSubscriptionEventRequest {
  eventId?: string | null;
}

export interface VirtoCommerceEventBusModuleCoreModelsSubscriptionRequest {
  connectionName?: string | null;
  eventSettingsSerialized?: string | null;
  events?:
    | VirtoCommerceEventBusModuleCoreModelsSubscriptionEventRequest[]
    | null;
  jsonPathFilter?: string | null;
  name?: string | null;
  payloadTransformationTemplate?: string | null;
}

export interface VirtoCommerceEventBusModuleCoreModelsSubscriptionSearchCriteria {
  connectionName?: string | null;
  eventIds?: string[] | null;
  keyword?: string | null;
  languageCode?: string | null;
  name?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceEventBusModuleCoreModelsSubscriptionSearchResult {
  results?: VirtoCommerceEventBusModuleCoreModelsSubscription[] | null;
  /** @format int32 */
  totalCount?: number;
}

/**
 * Basic query information for data sources to retrieve exported data: included properties, paging, sorting, etc...
 * Applied data sources expand it by adding certain criteria (for example, additional information for searching)
 */
export interface VirtoCommerceExportModuleCoreModelExportDataQuery {
  /** This used to instantiate a data query of this type at export start. */
  readonly exportTypeName?: string | null;
  /** User selected properties to export */
  includedProperties?:
    | VirtoCommerceExportModuleCoreModelExportedTypePropertyInfo[]
    | null;
  /** True means preview (lightweight) data is queried, false - full version requested */
  isPreview?: boolean;
  /** Keyword to search data */
  keyword?: string | null;
  /** Object keys to search data */
  objectIds?: string[] | null;
  /**
   * Paging: skip records
   * @format int32
   */
  skip?: number | null;
  /** How to sort the dataset matching a query */
  sort?: string | null;
  /**
   * Paging: records in one page
   * @format int32
   */
  take?: number | null;
}

/** Incapsulates data required to start export: export type, query for data to export, provider to record */
export interface VirtoCommerceExportModuleCoreModelExportDataRequest {
  /** Query information to retrive exported data */
  dataQuery?: VirtoCommerceExportModuleCoreModelExportDataQuery | null;
  /** Full type name of exportable entity */
  exportTypeName?: string | null;
  /** Export provider configuration */
  providerConfig?: VirtoCommerceExportModuleCoreModelIExportProviderConfiguration | null;
  /** Selected export provider name */
  providerName?: string | null;
}

/** Exportable entities search result. */
export interface VirtoCommerceExportModuleCoreModelExportableSearchResult {
  results?: VirtoCommerceExportModuleCoreModelIExportable[] | null;
  /** @format int32 */
  totalCount?: number;
}

/** Definition of exported entity type */
export interface VirtoCommerceExportModuleCoreModelExportedTypeDefinition {
  /** Specific type name with which we could query exported type data. */
  exportDataQueryType?: string | null;
  /** Logical group name. Entity types can be divided into different groups to simplify selection. */
  group?: string | null;
  /** Returns true if tabular export supported, VirtoCommerce.ExportModule.Core.Model.ExportedTypeDefinition.TabularMetaData is set . */
  readonly isTabularExportSupported?: boolean;
  /** Metadata for this definition (set of properties, version) */
  metaData?: VirtoCommerceExportModuleCoreModelExportedTypeMetadata | null;
  /** Restrict access to select data for export */
  restrictDataSelectivity?: boolean;
  /** Metadata for this definition in case of supported tabular export (flat files, like *.csv). */
  tabularMetaData?: VirtoCommerceExportModuleCoreModelExportedTypeMetadata | null;
  /** Logical type name, given during registration. It could be non-equal to exportable type name. */
  typeName?: string | null;
}

/** Metadata for exported type: properties information and version */
export interface VirtoCommerceExportModuleCoreModelExportedTypeMetadata {
  /** Exportable property infos array */
  propertyInfos?:
    | VirtoCommerceExportModuleCoreModelExportedTypePropertyInfo[]
    | null;
  version?: string | null;
}

/** Export property information */
export interface VirtoCommerceExportModuleCoreModelExportedTypePropertyInfo {
  /** User-friendly name for this property */
  displayName?: string | null;
  /** Property name with the path from the exportable entity (e.g. for entity containing PropertyA with nested properties it could be "PropertyA.PropertyB.PropertyC"). */
  fullName?: string | null;
  /**
   * Property group. Properties can be divided into different groups to simplify selection.
   * Group could be used for grouping property infos.
   */
  group?: string | null;
  /** * Reserved for future use */
  isRequired?: boolean;
}

export interface VirtoCommerceExportModuleCoreModelIExportProviderConfiguration {
  /** Type discriminator to instantiate proper descendant (e.g. thru the universal PolymorphJsonConverter) */
  type?: string | null;
}

/** Interface to implement exportаble entities. */
export interface VirtoCommerceExportModuleCoreModelIExportable {
  id?: string | null;
}

/**
 * Interface for export provider implementation.
 * The export provider allows to write object using the given TextWriter.
 */
export interface VirtoCommerceExportModuleCoreServicesIExportProvider {
  /** Returns provider configuration. */
  readonly configuration?: VirtoCommerceExportModuleCoreModelIExportProviderConfiguration | null;
  /** Extension for resulting export file. */
  readonly exportedFileExtension?: string | null;
  /** Returns true if provider supports only plain tabular objects (without nested entities). */
  readonly isTabular?: boolean;
  /** Provider name. */
  readonly typeName?: string | null;
}

export interface VirtoCommerceExportModuleWebModelExportCancellationRequest {
  jobId?: string | null;
}

export interface VirtoCommerceFileExperienceApiCoreModelsFileUploadResult {
  contentType?: string | null;
  errorCode?: string | null;
  errorMessage?: string | null;
  errorParameter?: object | null;
  id?: string | null;
  name?: string | null;
  ownerEntityId?: string | null;
  ownerEntityType?: string | null;
  publicUrl?: string | null;
  scope?: string | null;
  /** @format int64 */
  size?: number;
  readonly succeeded?: boolean;
  url?: string | null;
}

export interface VirtoCommerceFileExperienceApiCoreModelsFileUploadScopeOptions {
  allowAnonymousUpload?: boolean;
  allowedExtensions: string[];
  /** @format int64 */
  maxFileSize: number;
  /** @minLength 1 */
  scope: string;
}

export type VirtoCommerceImageToolsModuleCoreModelsAnchorPosition =
  | "TopLeft"
  | "TopCenter"
  | "TopRight"
  | "CenterLeft"
  | "Center"
  | "CenterRight"
  | "BottomLeft"
  | "BottomCenter"
  | "BottomRight";

export type VirtoCommerceImageToolsModuleCoreModelsJpegQuality =
  | "Low"
  | "Medium"
  | "High"
  | "VeryHigh";

export type VirtoCommerceImageToolsModuleCoreModelsResizeMethod =
  | "FixedSize"
  | "FixedWidth"
  | "FixedHeight"
  | "Crop";

export interface VirtoCommerceImageToolsModuleCoreModelsThumbnailOption {
  anchorPosition?: VirtoCommerceImageToolsModuleCoreModelsAnchorPosition;
  backgroundColor?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  fileSuffix?: string | null;
  /** @format int32 */
  height?: number | null;
  id?: string | null;
  jpegQuality?: VirtoCommerceImageToolsModuleCoreModelsJpegQuality;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  resizeMethod?: VirtoCommerceImageToolsModuleCoreModelsResizeMethod;
  /** @format int32 */
  width?: number | null;
}

export interface VirtoCommerceImageToolsModuleCoreModelsThumbnailOptionSearchCriteria {
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceImageToolsModuleCoreModelsThumbnailOptionSearchResult {
  results?: VirtoCommerceImageToolsModuleCoreModelsThumbnailOption[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceImageToolsModuleCoreModelsThumbnailTask {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  /** @format date-time */
  lastRun?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  thumbnailOptions?:
    | VirtoCommerceImageToolsModuleCoreModelsThumbnailOption[]
    | null;
  workPath?: string | null;
}

export interface VirtoCommerceImageToolsModuleCoreModelsThumbnailTaskSearchCriteria {
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceImageToolsModuleCoreModelsThumbnailTaskSearchResult {
  results?: VirtoCommerceImageToolsModuleCoreModelsThumbnailTask[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceImageToolsModuleCoreModelsThumbnailsTaskRunRequest {
  regenerate?: boolean;
  taskIds?: string[] | null;
}

export interface VirtoCommerceImageToolsModuleCorePushNotificationsThumbnailProcessNotification {
  /** @format date-time */
  created?: string;
  creator?: string | null;
  description?: string | null;
  /** @format int64 */
  errorCount?: number;
  errors?: string[] | null;
  /** @format date-time */
  finished?: string | null;
  id?: string | null;
  isNew?: boolean;
  jobId?: string | null;
  notifyType?: string | null;
  /** @format int64 */
  processedCount?: number;
  /** @format int32 */
  repeatCount?: number;
  serverId?: string | null;
  title?: string | null;
  /** @format int64 */
  totalCount?: number;
}

export interface VirtoCommerceInventoryModuleCoreModelFulfillmentCenter {
  address?: InventoryAddress | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  description?: string | null;
  dynamicProperties?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicObjectProperty[]
    | null;
  geoLocation?: string | null;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  readonly objectType?: string | null;
  organizationId?: string | null;
  outerId?: string | null;
  shortDescription?: string | null;
}

export interface VirtoCommerceInventoryModuleCoreModelInventoryInfo {
  allowBackorder?: boolean;
  allowPreorder?: boolean;
  /** @format date-time */
  backorderAvailabilityDate?: string | null;
  /** @format int64 */
  backorderQuantity?: number;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  fulfillmentCenter?: VirtoCommerceInventoryModuleCoreModelFulfillmentCenter | null;
  fulfillmentCenterId?: string | null;
  fulfillmentCenterName?: string | null;
  id?: string | null;
  /** @format int64 */
  inStockQuantity?: number;
  /** @format int64 */
  inTransit?: number;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  outerId?: string | null;
  /** @format date-time */
  preorderAvailabilityDate?: string | null;
  /** @format int64 */
  preorderQuantity?: number;
  productId?: string | null;
  /** @format int64 */
  reorderMinQuantity?: number;
  /** @format int64 */
  reservedQuantity?: number;
  status?: VirtoCommerceInventoryModuleCoreModelInventoryStatus;
}

export type VirtoCommerceInventoryModuleCoreModelInventoryStatus =
  | "Disabled"
  | "Enabled"
  | "Ignored";

/** Inventory of a product along with the product information resolved from the catalog. */
export interface VirtoCommerceInventoryModuleCoreModelProductInventoryInfo {
  inventory?: VirtoCommerceInventoryModuleCoreModelInventoryInfo | null;
  /** Null when the product no longer exists in the catalog. */
  product?: VirtoCommerceCatalogModuleCoreModelCatalogProduct | null;
  productId?: string | null;
}

export interface VirtoCommerceInventoryModuleCoreModelSearchFulfillmentCenterSearchCriteria {
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  organizationId?: string | null;
  outerId?: string | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceInventoryModuleCoreModelSearchFulfillmentCenterSearchResult {
  results?: VirtoCommerceInventoryModuleCoreModelFulfillmentCenter[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceInventoryModuleCoreModelSearchInventoryInfoSearchResult {
  results?: VirtoCommerceInventoryModuleCoreModelInventoryInfo[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceInventoryModuleCoreModelSearchInventorySearchCriteria {
  fulfillmentCenterIds?: string[] | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  productIds?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
  /** Return only inventories with positive in stock quantity. */
  withPositiveQuantityOnly?: boolean;
}

export interface VirtoCommerceInventoryModuleCoreModelSearchProductInventoryInfoSearchResult {
  results?: VirtoCommerceInventoryModuleCoreModelProductInventoryInfo[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceInventoryModuleCoreModelSearchProductInventorySearchCriteria {
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  productId?: string | null;
  productIds?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
  withInventoryOnly?: boolean;
}

export interface VirtoCommerceMarketingModuleCoreModelDynamicContentDynamicContentConditionTree {
  all?: boolean;
  availableChildren?:
    | VirtoCommerceCoreModuleCoreConditionsIConditionTree[]
    | null;
  children?: VirtoCommerceCoreModuleCoreConditionsIConditionTree[] | null;
  readonly id?: string | null;
  not?: boolean;
}

export interface VirtoCommerceMarketingModuleCoreModelDynamicContentEvaluationContext {
  categoryId?: string | null;
  contextObject?: object | null;
  currentUrl?: string | null;
  geoCity?: string | null;
  geoConnectionType?: string | null;
  geoContinent?: string | null;
  geoCountry?: string | null;
  geoIpRoutingType?: string | null;
  geoIspSecondLevel?: string | null;
  geoIspTopLevel?: string | null;
  geoState?: string | null;
  geoTimeZone?: string | null;
  geoZipCode?: string | null;
  language?: string | null;
  placeName?: string | null;
  productId?: string | null;
  referredUrl?: string | null;
  /** @format int32 */
  shopperAge?: number;
  shopperGender?: string | null;
  shopperSearchedPhraseInStore?: string | null;
  shopperSearchedPhraseOnInternet?: string | null;
  storeId?: string | null;
  tags?: string[] | null;
  /** @format date-time */
  toDate?: string;
  /** Any tags or groups belongs to user such as VIP, Wholesaler etc */
  userGroups?: string[] | null;
}

export interface VirtoCommerceMarketingModuleCoreModelDynamicContentFolder {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  description?: string | null;
  id?: string | null;
  /** Gets or sets the image URL. */
  imageUrl?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  /** Gets or sets the name. */
  name?: string | null;
  readonly objectType?: string | null;
  /** all parent folders ids concatenated (1;21;344) */
  readonly outline?: string | null;
  parentFolder?: VirtoCommerceMarketingModuleCoreModelDynamicContentFolder | null;
  parentFolderId?: string | null;
  /** all parent folders names concatenated (Root\Child\Child2) */
  readonly path?: string | null;
}

export interface VirtoCommerceMarketingModuleCoreModelDynamicContentItem {
  contentType?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  description?: string | null;
  dynamicProperties?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicObjectProperty[]
    | null;
  folder?: VirtoCommerceMarketingModuleCoreModelDynamicContentFolder | null;
  folderId?: string | null;
  id?: string | null;
  /** Gets or sets the image URL. */
  imageUrl?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  /** Gets or sets the name. */
  name?: string | null;
  readonly objectType?: string | null;
  /** all parent folders ids concatenated (1;21;344) */
  readonly outline?: string | null;
  /** all parent folders names concatenated (Root\Child\Child2) */
  readonly path?: string | null;
  /** @format int32 */
  priority?: number;
}

export interface VirtoCommerceMarketingModuleCoreModelDynamicContentItemSearchCriteria {
  folderId?: string | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceMarketingModuleCoreModelDynamicContentListEntry {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  description?: string | null;
  id?: string | null;
  /** Gets or sets the image URL. */
  imageUrl?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  /** Gets or sets the name. */
  name?: string | null;
  /** Gets or sets the type. E.g. "folder", "content-item", "content-place" */
  objectType?: string | null;
}

export interface VirtoCommerceMarketingModuleCoreModelDynamicContentPlace {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  description?: string | null;
  folder?: VirtoCommerceMarketingModuleCoreModelDynamicContentFolder | null;
  folderId?: string | null;
  id?: string | null;
  /** Gets or sets the image URL. */
  imageUrl?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  /** Gets or sets the name. */
  name?: string | null;
  /** Gets or sets the type. E.g. "folder", "content-item", "content-place" */
  objectType?: string | null;
  /** all parent folders ids concatenated (1;21;344) */
  readonly outline?: string | null;
  /** all parent folders names concatenated (Root\Child\Child2) */
  readonly path?: string | null;
}

export interface VirtoCommerceMarketingModuleCoreModelDynamicContentPlaceSearchCriteria {
  folderId?: string | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceMarketingModuleCoreModelDynamicContentPublication {
  contentItems?:
    | VirtoCommerceMarketingModuleCoreModelDynamicContentItem[]
    | null;
  contentPlaces?:
    | VirtoCommerceMarketingModuleCoreModelDynamicContentPlace[]
    | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  description?: string | null;
  dynamicExpression?: VirtoCommerceMarketingModuleCoreModelDynamicContentDynamicContentConditionTree | null;
  /** @format date-time */
  endDate?: string | null;
  id?: string | null;
  isActive?: boolean;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  outerId?: string | null;
  /** @format int32 */
  priority?: number;
  /** @format date-time */
  startDate?: string | null;
  storeId?: string | null;
}

export interface VirtoCommerceMarketingModuleCoreModelDynamicContentPublicationSearchCriteria {
  folderId?: string | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  onlyActive?: boolean;
  placeName?: string | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  store?: string | null;
  /** @format int32 */
  take?: number;
  /** @format date-time */
  toDate?: string | null;
}

export interface VirtoCommerceMarketingModuleCoreModelDynamicContentSearchDynamicContentItemSearchResult {
  results?: VirtoCommerceMarketingModuleCoreModelDynamicContentItem[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceMarketingModuleCoreModelDynamicContentSearchDynamicContentListEntrySearchResult {
  results?:
    | VirtoCommerceMarketingModuleCoreModelDynamicContentListEntry[]
    | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceMarketingModuleCoreModelDynamicContentSearchDynamicContentPlaceSearchResult {
  results?: VirtoCommerceMarketingModuleCoreModelDynamicContentPlace[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceMarketingModuleCoreModelDynamicContentSearchDynamicContentPublicationSearchResult {
  results?:
    | VirtoCommerceMarketingModuleCoreModelDynamicContentPublication[]
    | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceMarketingModuleCoreModelImportRequest {
  delimiter?: string | null;
  /** @format date-time */
  expirationDate?: string | null;
  fileUrl?: string | null;
  promotionId?: string | null;
}

export interface VirtoCommerceMarketingModuleCoreModelPromotionsCoupon {
  /** coupon code */
  code?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  /** @format date-time */
  expirationDate?: string | null;
  id?: string | null;
  /**
   * Restriction of total coupon usages
   * 0 infinitive
   * @format int32
   */
  maxUsesNumber?: number;
  /**
   * Maximum number of uses per registered user
   * 0 infinitive
   * @format int32
   */
  maxUsesPerUser?: number;
  /** Register coupon for a specific customer or organization */
  memberId?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  outerId?: string | null;
  promotionId?: string | null;
  /**
   * Total number of uses
   * @format int64
   */
  totalUsesCount?: number;
}

export interface VirtoCommerceMarketingModuleCoreModelPromotionsProductPromoEntry {
  attributes?: Record<string, string | null>;
  catalogId?: string | null;
  categoryId?: string | null;
  code?: string | null;
  /** @format double */
  discount?: number;
  /** @format int32 */
  inStockQuantity?: number;
  /** @format double */
  listPrice?: number;
  outline?: string | null;
  owner?: object | null;
  parentId?: string | null;
  /** @format double */
  price?: number;
  productId?: string | null;
  /** @format int32 */
  quantity?: number;
  variations?:
    | VirtoCommerceMarketingModuleCoreModelPromotionsProductPromoEntry[]
    | null;
}

export interface VirtoCommerceMarketingModuleCoreModelPromotionsPromotion {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  description?: string | null;
  dynamicExpression?: VirtoCommerceMarketingModuleCoreModelPromotionsPromotionConditionAndRewardTree | null;
  /** @format date-time */
  endDate?: string | null;
  hasCoupons?: boolean;
  id?: string | null;
  isActive?: boolean;
  /**
   * If this flag is set to true, it allows this promotion to combine with itself.
   * Special for case when need to return same promotion rewards for multiple coupons
   */
  isAllowCombiningWithSelf?: boolean;
  /** If a promotion with this setting is applied, no other promotions can be applied to the order. */
  isExclusive?: boolean;
  isPublic?: boolean;
  localizedDescription?: VirtoCommercePlatformCoreCommonLocalizedString | null;
  localizedDisplayName?: VirtoCommercePlatformCoreCommonLocalizedString | null;
  localizedLabel?: VirtoCommercePlatformCoreCommonLocalizedString | null;
  /**
   * Maximum redemptions by a single customer
   * @format int32
   */
  maxPersonalUsageCount?: number;
  /**
   * Maximum redemptions for this promotion
   * @format int32
   */
  maxUsageCount?: number;
  /**
   * Maximum redemptions on a single order
   * @format int32
   */
  maxUsageOnOrder?: number;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  /** Promotion name */
  name?: string | null;
  outerId?: string | null;
  /**
   * Represents a promotion priority, for combination policies when it is necessary to select a promotion with a higher priority
   * @format int32
   */
  priority?: number;
  /** @format date-time */
  startDate?: string | null;
  storeIds?: string[] | null;
  /** Required for UI. TODO: remove later */
  type?: string | null;
}

export interface VirtoCommerceMarketingModuleCoreModelPromotionsPromotionConditionAndRewardTree {
  all?: boolean;
  availableChildren?:
    | VirtoCommerceCoreModuleCoreConditionsIConditionTree[]
    | null;
  children?: VirtoCommerceCoreModuleCoreConditionsIConditionTree[] | null;
  readonly id?: string | null;
  not?: boolean;
}

export interface VirtoCommerceMarketingModuleCoreModelPromotionsPromotionEvaluationContext {
  availablePaymentMethodCodes?: string[] | null;
  availableShipmentMethodCodes?: string[] | null;
  /** List of product promo in cart */
  cartPromoEntries?:
    | VirtoCommerceMarketingModuleCoreModelPromotionsProductPromoEntry[]
    | null;
  /** @format double */
  cartTotal?: number;
  contactId?: string | null;
  contextObject?: object | null;
  /** Entered coupon */
  coupon?: string | null;
  coupons?: string[] | null;
  currency?: string | null;
  /** Currency */
  currencyObject?: VirtoCommerceCoreModuleCoreCurrencyCurrency | null;
  currentUrl?: string | null;
  /**
   * Contains User Id.
   * This property will be deleted after update to .NET8. Use UserId property instead.
   */
  customerId?: string | null;
  geoCity?: string | null;
  geoConnectionType?: string | null;
  geoContinent?: string | null;
  geoCountry?: string | null;
  geoIpRoutingType?: string | null;
  geoIspSecondLevel?: string | null;
  geoIspTopLevel?: string | null;
  geoState?: string | null;
  geoTimeZone?: string | null;
  geoZipCode?: string | null;
  isEveryone?: boolean;
  /** Has user made any orders */
  isFirstTimeBuyer?: boolean;
  isRegisteredUser?: boolean;
  language?: string | null;
  organizationId?: string | null;
  /** Current payment method */
  paymentMethodCode?: string | null;
  /** @format double */
  paymentMethodPrice?: number;
  /** List of products for promo evaluation */
  promoEntries?:
    | VirtoCommerceMarketingModuleCoreModelPromotionsProductPromoEntry[]
    | null;
  /** Single catalog product promo entry */
  promoEntry?: VirtoCommerceMarketingModuleCoreModelPromotionsProductPromoEntry | null;
  referredUrl?: string | null;
  refusedGiftIds?: string[] | null;
  /** Current shipment method */
  shipmentMethodCode?: string | null;
  shipmentMethodOption?: string | null;
  /** @format double */
  shipmentMethodPrice?: number;
  /** @format int32 */
  shopperAge?: number;
  shopperGender?: string | null;
  shopperSearchedPhraseInStore?: string | null;
  shopperSearchedPhraseOnInternet?: string | null;
  storeId?: string | null;
  /** Any tags or groups belongs to user such as VIP, Wholesaler etc */
  userGroups?: string[] | null;
  userId?: string | null;
}

export type VirtoCommerceMarketingModuleCoreModelPromotionsRewardAmountType =
  | "Absolute"
  | "Relative";

export interface VirtoCommerceMarketingModuleCoreModelPromotionsSearchCouponSearchCriteria {
  code?: string | null;
  codes?: string[] | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  promotionId?: string | null;
  promotionIds?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceMarketingModuleCoreModelPromotionsSearchCouponSearchResult {
  results?: VirtoCommerceMarketingModuleCoreModelPromotionsCoupon[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceMarketingModuleCoreModelPromotionsSearchPromotionSearchCriteria {
  /** @format int32 */
  couponCount?: number | null;
  isPublic?: boolean | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  onlyActive?: boolean;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  status?: VirtoCommerceMarketingModuleCoreModelPromotionsSearchPromotionStatus | null;
  store?: string | null;
  storeIds?: string[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceMarketingModuleCoreModelPromotionsSearchPromotionSearchResult {
  results?: VirtoCommerceMarketingModuleCoreModelPromotionsPromotion[] | null;
  /** @format int32 */
  totalCount?: number;
}

export type VirtoCommerceMarketingModuleCoreModelPromotionsSearchPromotionStatus =
  | "All"
  | "Active"
  | "Upcoming"
  | "Archived"
  | "Deactivated";

export interface VirtoCommerceMarketingModuleCoreModelPushNotificationsImportNotification {
  /** @format date-time */
  created?: string;
  creator?: string | null;
  description?: string | null;
  /** @format int64 */
  errorCount?: number;
  errors?: string[] | null;
  /** @format date-time */
  finished?: string | null;
  id?: string | null;
  isNew?: boolean;
  notifyType?: string | null;
  /** @format int64 */
  processedCount?: number;
  /** @format int32 */
  repeatCount?: number;
  serverId?: string | null;
  title?: string | null;
  /** @format int64 */
  totalCount?: number;
}

/** need to backward compatibility with v.2 */
export interface VirtoCommerceMarketingModuleWebModelPromotionReward {
  /**
   * Gets or sets the value of promotion reward amount
   * @format double
   */
  amount?: number;
  /** Gets or sets the value of promotion reward amount type */
  amountType?: VirtoCommerceMarketingModuleCoreModelPromotionsRewardAmountType;
  /** Gets or sets the value of category id */
  categoryId?: string | null;
  /**
   * Conditional product
   * For N items of entry ProductId  in every Y items of entry ConditionalProductId get %X off
   */
  conditionalProductId?: string | null;
  /** Gets or sets the value of coupon code */
  coupon?: string | null;
  /**
   * Gets or sets the value of coupon amount
   * @format double
   */
  couponAmount?: number;
  /**
   * Gets or sets the value of minimum order total cost for applying coupon
   * @format double
   */
  couponMinOrderAmount?: number | null;
  /** Gets or sets the value of promotion reward description */
  description?: string | null;
  /** @format int32 */
  forNthQuantity?: number;
  /** Gets or sets the value of promotion reward logo absolute URL */
  imageUrl?: string | null;
  /** @format int32 */
  inEveryNthQuantity?: number;
  /** Gets or sets the flag of promotion reward is valid. Also used as a flag for applicability (applied or potential) */
  isValid?: boolean;
  /** Gets or sets the value of line item id */
  lineItemId?: string | null;
  /**
   * Gets or sets the max limit for relative rewards
   * @format double
   */
  maxLimit?: number;
  /** Gets or sets the value of measurement unit */
  measureUnit?: string | null;
  /** Gets or sets the value of reward payment method code */
  paymentMethod?: string | null;
  /** Gets or sets the value of product id */
  productId?: string | null;
  /** Gets or sets the promotion */
  promotion?: VirtoCommerceMarketingModuleCoreModelPromotionsPromotion | null;
  /** Gets or sets the value of promotion id */
  promotionId?: string | null;
  /**
   * Gets or sets the value of line item quantity for applying promotion reward
   * @format int32
   */
  quantity?: number;
  /** Gets or sets the value of promotion reward type */
  rewardType?: string | null;
  /** Gets or sets the value of reward shipping method code */
  shippingMethod?: string | null;
}

/** Base class for Notification */
export interface VirtoCommerceNotificationsModuleCoreModelNotification {
  /**
   * This field represents an alias for the notification type
   * and is used only for backward compatibility with old notification names
   * that are stored and used by API clients.
   */
  alias?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  /**
   * need for saving validation errors
   * if the property is not empty then the notification is not sent
   * for seting use SetCustomValidationError
   */
  readonly customValidationError?: string | null;
  id?: string | null;
  isActive?: boolean | null;
  /** For detecting kind of notifications (email, sms and etc.) */
  readonly kind?: string | null;
  languageCode?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  outerId?: string | null;
  templates?:
    | VirtoCommerceNotificationsModuleCoreModelNotificationTemplate[]
    | null;
  /** For detecting owner */
  tenantIdentity?: VirtoCommercePlatformCoreCommonTenantIdentity | null;
  /** Type of notifications, like Identifier */
  type?: string | null;
}

export interface VirtoCommerceNotificationsModuleCoreModelNotificationLayout {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  isDefault?: boolean;
  isPredefined?: boolean;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  template?: string | null;
}

/** Base class for message of a notification with information about sending */
export interface VirtoCommerceNotificationsModuleCoreModelNotificationMessage {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  readonly kind?: string | null;
  /** Code of language */
  languageCode?: string | null;
  /**
   * The last date of sending attempt
   * @format date-time
   */
  lastSendAttemptDate?: string | null;
  /** The last error of sending */
  lastSendError?: string | null;
  /**
   * Max count of sending attempt
   * @format int32
   */
  maxSendAttemptCount?: number;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  /** Id of Notification */
  notificationId?: string | null;
  /** Type of Notification */
  notificationType?: string | null;
  /**
   * Count of sending attempt
   * @format int32
   */
  sendAttemptCount?: number;
  /**
   * Date of sending
   * @format date-time
   */
  sendDate?: string | null;
  /** Status of message */
  status?: VirtoCommerceNotificationsModuleCoreModelNotificationMessageStatus;
  /** For detecting owner */
  tenantIdentity?: VirtoCommercePlatformCoreCommonTenantIdentity | null;
  /** Discriminator of NotificationMessage, name of real message descendant */
  readonly type?: string | null;
}

export type VirtoCommerceNotificationsModuleCoreModelNotificationMessageStatus =
  | "Pending"
  | "Sent"
  | "Error";

/** Criteria for searching */
export interface VirtoCommerceNotificationsModuleCoreModelNotificationSearchCriteria {
  /** Only active notification */
  isActive?: boolean;
  keyword?: string | null;
  /** Filter notifications by kind (e.g., EmailNotification, SmsNotification) */
  kinds?: string[] | null;
  languageCode?: string | null;
  /** Filter notifications by type */
  notificationType?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
  /** Owner Id of Notification */
  tenantId?: string | null;
  /** Owner Type of Notification */
  tenantType?: string | null;
}

export interface VirtoCommerceNotificationsModuleCoreModelNotificationSearchResult {
  results?: VirtoCommerceNotificationsModuleCoreModelNotification[] | null;
  /** @format int32 */
  totalCount?: number;
}

/** Result of notification sending */
export interface VirtoCommerceNotificationsModuleCoreModelNotificationSendResult {
  errorMessage?: string | null;
  isSuccess?: boolean;
}

/** Template of Notification with a different language */
export interface VirtoCommerceNotificationsModuleCoreModelNotificationTemplate {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  isPredefined?: boolean;
  isReadonly?: boolean;
  /** For detecting kind of notifications (email, sms and etc.) */
  readonly kind?: string | null;
  /** Code of Language */
  languageCode?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  outerId?: string | null;
  /** Discriminator of NotificationTemplate, name of real template descendant */
  readonly type?: string | null;
}

export interface VirtoCommerceNotificationsModuleCoreModelSearchNotificationLayoutSearchCriteria {
  isDefault?: boolean | null;
  keyword?: string | null;
  languageCode?: string | null;
  names?: string[] | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceNotificationsModuleCoreModelSearchNotificationLayoutSearchResult {
  results?:
    | VirtoCommerceNotificationsModuleCoreModelNotificationLayout[]
    | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceNotificationsModuleCoreModelSearchNotificationMessageSearchCriteria {
  /** @format date-time */
  endDate?: string | null;
  keyword?: string | null;
  languageCode?: string | null;
  notificationType?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchInBody?: boolean;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format date-time */
  startDate?: string | null;
  status?: string | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceNotificationsModuleCoreModelSearchNotificationMessageSearchResult {
  results?:
    | VirtoCommerceNotificationsModuleCoreModelNotificationMessage[]
    | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceNotificationsModuleWebModelNotificationParameter {
  isArray?: boolean;
  isDictionary?: boolean;
  parameterCodeInView?: string | null;
  parameterDescription?: string | null;
  parameterName?: string | null;
  type?: VirtoCommerceNotificationsModuleWebModelNotificationParameterValueType;
  value?: object | null;
}

export type VirtoCommerceNotificationsModuleWebModelNotificationParameterValueType =
  | "String"
  | "Integer"
  | "Decimal"
  | "DateTime"
  | "Boolean";

export interface VirtoCommerceNotificationsModuleWebModelNotificationRequest {
  language?: string | null;
  notificationParameters?:
    | VirtoCommerceNotificationsModuleWebModelNotificationParameter[]
    | null;
  objectId?: string | null;
  objectTypeId?: string | null;
  type?: string | null;
}

export interface VirtoCommerceNotificationsModuleWebModelNotificationTemplateRequest {
  /** Base class for Notification */
  data?: VirtoCommerceNotificationsModuleCoreModelNotification | null;
  notificationLayoutId?: string | null;
  text?: string | null;
}

export type VirtoCommerceOrdersModuleCoreModelCancelledState =
  | "Undefined"
  | "Requested"
  | "Completed";

export interface VirtoCommerceOrdersModuleCoreModelCapture {
  /** @format double */
  amount?: number;
  cancelReason?: string | null;
  /** @format date-time */
  cancelledDate?: string | null;
  /** For system use to handle canellation flow */
  cancelledState?: VirtoCommerceOrdersModuleCoreModelCancelledState;
  closeTransaction?: boolean;
  comment?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  currency?: string | null;
  customerOrderId?: string | null;
  dynamicProperties?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicObjectProperty[]
    | null;
  id?: string | null;
  isApproved?: boolean;
  /** Used by payment provides to indicate that cancellation operation has completed */
  isCancelled?: boolean;
  items?: VirtoCommerceOrdersModuleCoreModelCaptureItem[] | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  number?: string | null;
  objectType?: string | null;
  operationType?: string | null;
  operationsLog?: VirtoCommercePlatformCoreChangeLogOperationLog[] | null;
  outerId?: string | null;
  parentOperationId?: string | null;
  paymentId?: string | null;
  status?: string | null;
  /** @format double */
  sum?: number;
  transactionId?: string | null;
  vendorId?: string | null;
  withPrices?: boolean;
}

export interface VirtoCommerceOrdersModuleCoreModelCaptureItem {
  captureId?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  lineItem?: OrderLineItem | null;
  lineItemId?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  outerId?: string | null;
  /** @format int32 */
  quantity?: number;
}

export interface VirtoCommerceOrdersModuleCoreModelCaptureOrderPaymentRequest {
  /** @format double */
  amount?: number | null;
  /** Provides information about the charge that customers see on their statements. If Seller provides this information, a payment provider can implement it. */
  captureDetails?: string | null;
  /** Set to True to close a transaction, restricting future capture operations against this order; otherwise, set to False. By default, False. */
  closeTransaction?: boolean;
  orderId?: string | null;
  outerId?: string | null;
  paymentId?: string | null;
  transactionId?: string | null;
}

export interface VirtoCommerceOrdersModuleCoreModelCustomerOrder {
  addresses?: OrderAddress[] | null;
  cancelReason?: string | null;
  /** @format date-time */
  cancelledDate?: string | null;
  /** For system use to handle canellation flow */
  cancelledState?: VirtoCommerceOrdersModuleCoreModelCancelledState;
  channelId?: string | null;
  comment?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  currency?: string | null;
  customerId?: string | null;
  customerName?: string | null;
  /**
   * When a discount is applied to the order, the tax calculation has already been applied and is shown in the tax field.
   * Therefore, the discount will not be taking tax into account.
   * For instance, if the cart subtotal is $100, and the tax subtotal is $15, a 10% discount will yield a total of $105 ($100 subtotal – $10 discount + $15 tax).
   * @format double
   */
  discountAmount?: number;
  /**
   * Amount of the discount amounts of items, shipments and payments, and the order discount amount
   * @format double
   */
  discountTotal?: number;
  /**
   * Amount of the discount amounts with tax of items, shipments and payments, and the order discount amount with tax
   * @format double
   */
  discountTotalWithTax?: number;
  discounts?: VirtoCommerceCoreModuleCoreCommonDiscount[] | null;
  dynamicProperties?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicObjectProperty[]
    | null;
  employeeId?: string | null;
  employeeName?: string | null;
  /**
   * Any extra fees applied to the order. This value comes from the cart
   * @format double
   */
  fee?: number;
  feeDetails?: VirtoCommerceOrdersModuleCoreModelFeeDetail[] | null;
  /**
   * Amount of the order fee, as well as any item, shipment, and payment fees
   * @format double
   */
  feeTotal?: number;
  /**
   * Total fee with applied tax factor
   * @format double
   */
  feeTotalWithTax?: number;
  /**
   * Order fee with applied tax factor
   * @format double
   */
  feeWithTax?: number;
  /**
   * Reserved for future needs
   * @format double
   */
  handlingTotal?: number;
  /**
   * Reserved for future needs
   * @format double
   */
  handlingTotalWithTax?: number;
  id?: string | null;
  inPayments?: VirtoCommerceOrdersModuleCoreModelPaymentIn[] | null;
  isAnonymous?: boolean;
  isApproved?: boolean;
  /** Used by payment provides to indicate that cancellation operation has completed */
  isCancelled?: boolean;
  /** This checkbox determines whether the order is a prototype */
  isPrototype?: boolean;
  items?: OrderLineItem[] | null;
  languageCode?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  number?: string | null;
  objectType?: string | null;
  operationType?: string | null;
  operationsLog?: VirtoCommercePlatformCoreChangeLogOperationLog[] | null;
  orderTotals?: VirtoCommerceOrdersModuleCoreModelOrderTotal[] | null;
  organizationId?: string | null;
  organizationName?: string | null;
  outerId?: string | null;
  parentOperationId?: string | null;
  /**
   * Amount of the payments discount amounts
   * @format double
   */
  paymentDiscountTotal?: number;
  /**
   * Amount of the payment discount amounts with tax
   * @format double
   */
  paymentDiscountTotalWithTax?: number;
  /**
   * Amount of the payment prices
   * @format double
   */
  paymentSubTotal?: number;
  /**
   * Amount of the payment prices with tax
   * @format double
   */
  paymentSubTotalWithTax?: number;
  /**
   * Reserved for future needs
   * @format double
   */
  paymentTaxTotal?: number;
  /**
   * Amount of the payments totals
   * @format double
   */
  paymentTotal?: number;
  /**
   * Amount of the payment totals with tax
   * @format double
   */
  paymentTotalWithTax?: number;
  /** The order internal number provided by customer */
  purchaseOrderNumber?: string | null;
  /** @format double */
  relevanceScore?: number | null;
  /** @format byte */
  rowVersion?: Blob | null;
  scopes?: string[] | null;
  shipments?: OrderShipment[] | null;
  /**
   * Amount of the shipment discount amounts
   * @format double
   */
  shippingDiscountTotal?: number;
  /**
   * Amount of the shipment discount amounts with tax
   * @format double
   */
  shippingDiscountTotalWithTax?: number;
  /**
   * Amount of the shipment prices
   * @format double
   */
  shippingSubTotal?: number;
  /**
   * Amount of the shipment prices with tax
   * @format double
   */
  shippingSubTotalWithTax?: number;
  /**
   * Reserved for future needs
   * @format double
   */
  shippingTaxTotal?: number;
  /**
   * Amount of the shipment total
   * @format double
   */
  shippingTotal?: number;
  /**
   * Amount of the shipment total with tax
   * @format double
   */
  shippingTotalWithTax?: number;
  /** The base shopping cart ID the order was created with */
  shoppingCartId?: string | null;
  status?: string | null;
  storeId?: string | null;
  storeName?: string | null;
  /**
   * Amount of the item prices
   * @format double
   */
  subTotal?: number;
  /**
   * Amount of the item discount total
   * @format double
   */
  subTotalDiscount?: number;
  /**
   * Amount of the item discount total with tax
   * @format double
   */
  subTotalDiscountWithTax?: number;
  /**
   * Amount of the item tax total
   * @format double
   */
  subTotalTaxTotal?: number;
  /**
   * Amount of the item prices with tax
   * @format double
   */
  subTotalWithTax?: number;
  /** The ID of subscription associated with this order */
  subscriptionId?: string | null;
  /** Number of subscription associated with this order */
  subscriptionNumber?: string | null;
  /** @format double */
  sum?: number;
  taxDetails?: VirtoCommerceCoreModuleCoreTaxTaxDetail[] | null;
  /** @format double */
  taxPercentRate?: number;
  /**
   * Amount of tax totals for items, shipments, and payments without the order discount amount with tax factor applied
   * @format double
   */
  taxTotal?: number;
  /** Tax category or type */
  taxType?: string | null;
  /**
   * Order grand total
   * @format double
   */
  total?: number;
  withPrices?: boolean;
}

export interface VirtoCommerceOrdersModuleCoreModelDashboardMoney {
  /** @format double */
  amount?: number;
  currency?: string | null;
}

export interface VirtoCommerceOrdersModuleCoreModelDashboardStatisticsResult {
  avgOrderValue?: VirtoCommerceOrdersModuleCoreModelDashboardMoney[] | null;
  avgOrderValuePeriodDetails?:
    | VirtoCommerceOrdersModuleCoreModelQuarterPeriodMoney[]
    | null;
  /** @format int32 */
  customersCount?: number;
  /** @format date-time */
  endDate?: string;
  /** @format int32 */
  itemsPurchased?: number;
  /** @format double */
  lineItemsPerOrder?: number;
  /** @format int32 */
  orderCount?: number;
  revenue?: VirtoCommerceOrdersModuleCoreModelDashboardMoney[] | null;
  revenuePerCustomer?:
    | VirtoCommerceOrdersModuleCoreModelDashboardMoney[]
    | null;
  revenuePeriodDetails?:
    | VirtoCommerceOrdersModuleCoreModelQuarterPeriodMoney[]
    | null;
  /** @format date-time */
  startDate?: string;
}

export interface VirtoCommerceOrdersModuleCoreModelFeeDetail {
  /** @format double */
  amount?: number;
  currency?: string | null;
  description?: string | null;
  feeId?: string | null;
}

export interface VirtoCommerceOrdersModuleCoreModelKeyValuePair {
  key?: string | null;
  value?: string | null;
}

export interface VirtoCommerceOrdersModuleCoreModelOrderTotal {
  currencyCode?: string | null;
  /** @format double */
  discountTotal?: number;
  id?: string | null;
  /** @format double */
  subTotal?: number;
  /** @format double */
  taxTotal?: number;
  /** @format double */
  total?: number;
}

export interface VirtoCommerceOrdersModuleCoreModelPaymentCallbackParameters {
  parameters?: VirtoCommerceOrdersModuleCoreModelKeyValuePair[] | null;
}

export interface VirtoCommerceOrdersModuleCoreModelPaymentGatewayTransaction {
  /** @format double */
  amount?: number;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  currencyCode?: string | null;
  /** Gateway IP address */
  gatewayIpAddress?: string | null;
  id?: string | null;
  /** Flag represent that current transaction is processed */
  isProcessed?: boolean;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  note?: string | null;
  /** @format int32 */
  processAttemptCount?: number;
  processError?: string | null;
  /**
   * Date when this transaction was handled
   * @format date-time
   */
  processedDate?: string | null;
  /** Raw request data */
  requestData?: string | null;
  /** Gateway or VC response status code */
  responseCode?: string | null;
  /** Raw response data */
  responseData?: string | null;
  /** "Active", "Expired", and "Inactive" or other */
  status?: string | null;
  /**
   * The type of payment interaction.The payment can be Capture or CheckReceived.
   * The value also includes customer payment interactions such as Website, Call, Store, or Unknown.
   */
  type?: string | null;
}

export interface VirtoCommerceOrdersModuleCoreModelPaymentIn {
  /** @format date-time */
  authorizedDate?: string | null;
  billingAddress?: OrderAddress | null;
  cancelReason?: string | null;
  /** @format date-time */
  cancelledDate?: string | null;
  /** For system use to handle canellation flow */
  cancelledState?: VirtoCommerceOrdersModuleCoreModelCancelledState;
  /** @format date-time */
  capturedDate?: string | null;
  captures?: VirtoCommerceOrdersModuleCoreModelCapture[] | null;
  comment?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  currency?: string | null;
  customerId?: string | null;
  customerName?: string | null;
  /** @format double */
  discountAmount?: number;
  /** @format double */
  discountAmountWithTax?: number;
  discounts?: VirtoCommerceCoreModuleCoreCommonDiscount[] | null;
  dynamicProperties?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicObjectProperty[]
    | null;
  feeDetails?: VirtoCommerceOrdersModuleCoreModelFeeDetail[] | null;
  /** Payment method (gateway) code */
  gatewayCode?: string | null;
  id?: string | null;
  /** @format date-time */
  incomingDate?: string | null;
  isApproved?: boolean;
  /** Used by payment provides to indicate that cancellation operation has completed */
  isCancelled?: boolean;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  number?: string | null;
  objectType?: string | null;
  operationType?: string | null;
  operationsLog?: VirtoCommercePlatformCoreChangeLogOperationLog[] | null;
  orderId?: string | null;
  organizationId?: string | null;
  organizationName?: string | null;
  outerId?: string | null;
  parentOperationId?: string | null;
  /** Payment method contains additional payment method information */
  paymentMethod?: VirtoCommercePaymentModuleCoreModelPaymentMethod | null;
  paymentStatus?: VirtoCommercePaymentModuleCoreModelPaymentStatus;
  /** @format double */
  price?: number;
  /** @format double */
  priceWithTax?: number;
  processPaymentResult?: VirtoCommercePaymentModuleModelRequestsProcessPaymentRequestResult | null;
  purpose?: string | null;
  refunds?: VirtoCommerceOrdersModuleCoreModelRefund[] | null;
  status?: string | null;
  /** @format double */
  sum?: number;
  taxDetails?: VirtoCommerceCoreModuleCoreTaxTaxDetail[] | null;
  /** @format double */
  taxPercentRate?: number;
  /** @format double */
  taxTotal?: number;
  /** Tax category or type */
  taxType?: string | null;
  /** @format double */
  total?: number;
  /** @format double */
  totalWithTax?: number;
  transactions?:
    | VirtoCommerceOrdersModuleCoreModelPaymentGatewayTransaction[]
    | null;
  vendorId?: string | null;
  /** @format date-time */
  voidedDate?: string | null;
  withPrices?: boolean;
}

export interface VirtoCommerceOrdersModuleCoreModelQuarterPeriodMoney {
  /** @format double */
  amount?: number;
  currency?: string | null;
  /** @format int32 */
  quarter?: number;
  /** @format int32 */
  year?: number;
}

export interface VirtoCommerceOrdersModuleCoreModelRefund {
  /** @format double */
  amount?: number;
  cancelReason?: string | null;
  /** @format date-time */
  cancelledDate?: string | null;
  /** For system use to handle canellation flow */
  cancelledState?: VirtoCommerceOrdersModuleCoreModelCancelledState;
  comment?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  currency?: string | null;
  customerOrderId?: string | null;
  dynamicProperties?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicObjectProperty[]
    | null;
  id?: string | null;
  isApproved?: boolean;
  /** Used by payment provides to indicate that cancellation operation has completed */
  isCancelled?: boolean;
  items?: VirtoCommerceOrdersModuleCoreModelRefundItem[] | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  number?: string | null;
  objectType?: string | null;
  operationType?: string | null;
  operationsLog?: VirtoCommercePlatformCoreChangeLogOperationLog[] | null;
  outerId?: string | null;
  parentOperationId?: string | null;
  paymentId?: string | null;
  reasonCode?: VirtoCommerceOrdersModuleCoreModelRefundReasonCode;
  reasonMessage?: string | null;
  refundStatus?: VirtoCommercePaymentModuleCoreModelRefundStatus;
  rejectReasonMessage?: string | null;
  status?: string | null;
  /** @format double */
  sum?: number;
  transactionId?: string | null;
  vendorId?: string | null;
  withPrices?: boolean;
}

export interface VirtoCommerceOrdersModuleCoreModelRefundItem {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  lineItem?: OrderLineItem | null;
  lineItemId?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  outerId?: string | null;
  /** @format int32 */
  quantity?: number;
  refundId?: string | null;
}

export interface VirtoCommerceOrdersModuleCoreModelRefundOrderPaymentRequest {
  /** @format double */
  amount?: number | null;
  orderId?: string | null;
  outerId?: string | null;
  paymentId?: string | null;
  reasonCode?: string | null;
  reasonMessage?: string | null;
  transactionId?: string | null;
}

export type VirtoCommerceOrdersModuleCoreModelRefundReasonCode =
  | "Duplicate"
  | "Fraudulent"
  | "RequestedByCustomer"
  | "Other";

export interface VirtoCommerceOrdersModuleCoreModelSearchCustomerOrderHistorySearchCriteria {
  /** @format date-time */
  endDate?: string | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  operationTypes?: string[] | null;
  orderId?: string | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format date-time */
  startDate?: string | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceOrdersModuleCoreModelSearchCustomerOrderIndexedSearchCriteria {
  customerId?: string | null;
  customerIds?: string[] | null;
  employeeId?: string | null;
  /** @format date-time */
  endDate?: string | null;
  facet?: string | null;
  hasParentOperation?: boolean | null;
  ids?: string[] | null;
  keyword?: string | null;
  languageCode?: string | null;
  /** Search by numbers */
  number?: string | null;
  numbers?: string[] | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  /** Search only recurring orders created by subscription */
  onlyRecurring?: boolean;
  /** It used to limit search within an operation (customer order for example) */
  operationId?: string | null;
  organizationId?: string | null;
  organizationIds?: string[] | null;
  outerIds?: string[] | null;
  parentOperationId?: string | null;
  /** Search orders with a certain product */
  productId?: string | null;
  /** Search orders with a certain promotion */
  promotionId?: string | null;
  /** Search orders with given promotions */
  promotionIds?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format date-time */
  startDate?: string | null;
  /** Search by status */
  status?: string | null;
  statuses?: string[] | null;
  storeIds?: string[] | null;
  /** Search orders with given subscription */
  subscriptionId?: string | null;
  subscriptionIds?: string[] | null;
  /** @format int32 */
  take?: number;
  /** Search orders with flag IsPrototype */
  withPrototypes?: boolean;
}

export interface VirtoCommerceOrdersModuleCoreModelSearchCustomerOrderSearchCriteria {
  customerId?: string | null;
  customerIds?: string[] | null;
  employeeId?: string | null;
  /** @format date-time */
  endDate?: string | null;
  hasParentOperation?: boolean | null;
  ids?: string[] | null;
  keyword?: string | null;
  languageCode?: string | null;
  /** Search by numbers */
  number?: string | null;
  numbers?: string[] | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  /** Search only recurring orders created by subscription */
  onlyRecurring?: boolean;
  /** It used to limit search within an operation (customer order for example) */
  operationId?: string | null;
  organizationId?: string | null;
  organizationIds?: string[] | null;
  outerIds?: string[] | null;
  parentOperationId?: string | null;
  /** Search orders with a certain product */
  productId?: string | null;
  /** Search orders with a certain promotion */
  promotionId?: string | null;
  /** Search orders with given promotions */
  promotionIds?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format date-time */
  startDate?: string | null;
  /** Search by status */
  status?: string | null;
  statuses?: string[] | null;
  storeIds?: string[] | null;
  /** Search orders with given subscription */
  subscriptionId?: string | null;
  subscriptionIds?: string[] | null;
  /** @format int32 */
  take?: number;
  /** Search orders with flag IsPrototype */
  withPrototypes?: boolean;
}

export interface VirtoCommerceOrdersModuleCoreModelSearchCustomerOrderSearchResult {
  results?: VirtoCommerceOrdersModuleCoreModelCustomerOrder[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceOrdersModuleCoreModelSearchPaymentSearchCriteria {
  /** @format date-time */
  authorizedEndDate?: string | null;
  /** @format date-time */
  authorizedStartDate?: string | null;
  /** @format date-time */
  capturedEndDate?: string | null;
  /** @format date-time */
  capturedStartDate?: string | null;
  /** Filter payments by customer */
  customerId?: string | null;
  employeeId?: string | null;
  /** @format date-time */
  endDate?: string | null;
  hasParentOperation?: boolean | null;
  ids?: string[] | null;
  keyword?: string | null;
  languageCode?: string | null;
  /** Search by numbers */
  number?: string | null;
  numbers?: string[] | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  /** It used to limit search within a customer order id */
  orderId?: string | null;
  /** It used to limit search within a customer order number */
  orderNumber?: string | null;
  outerIds?: string[] | null;
  parentOperationId?: string | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format date-time */
  startDate?: string | null;
  /** Search by status */
  status?: string | null;
  statuses?: string[] | null;
  storeIds?: string[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceOrdersModuleCoreModelSearchPaymentSearchResult {
  results?: VirtoCommerceOrdersModuleCoreModelPaymentIn[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceOrdersModuleCoreModelSearchShipmentSearchCriteria {
  employeeId?: string | null;
  /** @format date-time */
  endDate?: string | null;
  fulfillmentCenterId?: string | null;
  hasParentOperation?: boolean | null;
  ids?: string[] | null;
  keyword?: string | null;
  languageCode?: string | null;
  /** Search by numbers */
  number?: string | null;
  numbers?: string[] | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  /** It used to limit search within a customer order id */
  orderId?: string | null;
  /** It used to limit search within a customer order number */
  orderNumber?: string | null;
  outerIds?: string[] | null;
  parentOperationId?: string | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  shipmentMethodCode?: string | null;
  shipmentMethodOption?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format date-time */
  startDate?: string | null;
  /** Search by status */
  status?: string | null;
  statuses?: string[] | null;
  storeIds?: string[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceOrdersModuleCoreModelSearchShipmentSearchResult {
  results?: OrderShipment[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceOrdersModuleCoreModelShipmentPackage {
  barCode?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  /** @format double */
  height?: number | null;
  id?: string | null;
  items?: OrderShipmentItem[] | null;
  /** @format double */
  length?: number | null;
  measureUnit?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  packageType?: string | null;
  /** @format double */
  weight?: number | null;
  weightUnit?: string | null;
  /** @format double */
  width?: number | null;
}

export interface VirtoCommercePageBuilderModuleCoreModelsCreateGroupedPageRequest {
  content?: string | null;
  cultureName?: string | null;
  /** @format date-time */
  endDate?: string | null;
  name?: string | null;
  organizationId?: string | null;
  permalink?: string | null;
  /** @format date-time */
  startDate?: string | null;
  storeId?: string | null;
  userGroups?: string | null;
  visibility?: boolean;
}

export interface VirtoCommercePageBuilderModuleCoreModelsGroupedPageBuilderPage {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  cultureName?: string | null;
  /** @format date-time */
  endDate?: string | null;
  readonly hasChanges?: boolean;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  organizationId?: string | null;
  pages?: VirtoCommercePageBuilderModuleCoreModelsPageBuilderPage[] | null;
  permalink?: string | null;
  /** @format date-time */
  startDate?: string | null;
  readonly status?: string | null;
  storeId?: string | null;
  userGroups?: string | null;
  visibility?: boolean;
}

export interface VirtoCommercePageBuilderModuleCoreModelsGroupedPageBuilderPageSearchResult {
  results?:
    | VirtoCommercePageBuilderModuleCoreModelsGroupedPageBuilderPage[]
    | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommercePageBuilderModuleCoreModelsPageBuilderAssetReference {
  assetUrl?: string | null;
  normalizedAssetUrl?: string | null;
  /** @format int32 */
  pageReferencesCount?: number;
  pages?:
    | VirtoCommercePageBuilderModuleCoreModelsPageBuilderAssetReferencePage[]
    | null;
  /** @format int32 */
  referencesCount?: number;
  /** @format int32 */
  sharedComponentReferencesCount?: number;
  sharedComponents?:
    | VirtoCommercePageBuilderModuleCoreModelsPageBuilderAssetReferenceSharedComponent[]
    | null;
}

export interface VirtoCommercePageBuilderModuleCoreModelsPageBuilderAssetReferencePage {
  cultureName?: string | null;
  id?: string | null;
  name?: string | null;
  permalink?: string | null;
  status?: string | null;
}

export interface VirtoCommercePageBuilderModuleCoreModelsPageBuilderAssetReferenceSharedComponent {
  id?: string | null;
  name?: string | null;
}

export interface VirtoCommercePageBuilderModuleCoreModelsPageBuilderAssetReferencesSearchCriteria {
  assetUrls?: string[] | null;
  folderUrl?: string | null;
  includePages?: boolean;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  statuses?: string | null;
  storeId?: string | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommercePageBuilderModuleCoreModelsPageBuilderAssetReferencesSearchResult {
  results?:
    | VirtoCommercePageBuilderModuleCoreModelsPageBuilderAssetReference[]
    | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommercePageBuilderModuleCoreModelsPageBuilderPage {
  content?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  groupId?: string | null;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  status?: string | null;
  storeId?: string | null;
}

export interface VirtoCommercePageBuilderModuleCoreModelsPageBuilderPageSearchCriteria {
  /** @format date-time */
  activeOn?: string | null;
  keyword?: string | null;
  languageCode?: string | null;
  lifecycle?: string | null;
  /** @format date-time */
  modifiedBefore?: string | null;
  /** @format date-time */
  modifiedSince?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  statuses?: string | null;
  storeId?: string | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommercePageBuilderModuleCoreModelsPageBuilderSharedComponent {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  storeId?: string | null;
  /** @format int32 */
  usageCount?: number;
  usagePages?:
    | VirtoCommercePageBuilderModuleCoreModelsPageBuilderSharedComponentUsagePage[]
    | null;
}

export interface VirtoCommercePageBuilderModuleCoreModelsPageBuilderSharedComponentSearchCriteria {
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  storeId?: string | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommercePageBuilderModuleCoreModelsPageBuilderSharedComponentSearchResult {
  results?:
    | VirtoCommercePageBuilderModuleCoreModelsPageBuilderSharedComponent[]
    | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommercePageBuilderModuleCoreModelsPageBuilderSharedComponentUsagePage {
  cultureName?: string | null;
  id?: string | null;
  name?: string | null;
  permalink?: string | null;
  status?: string | null;
}

export interface VirtoCommercePageBuilderModuleCoreModelsUpdatePageContentRequest {
  content?: string | null;
}

export interface VirtoCommercePageBuilderModuleWebControllersApiPageBuilderControllerSaveFilesModel {
  files?: string | null;
}

export interface VirtoCommercePageBuilderModuleWebModelsLegacyDraftsDeleteRequest {
  dryRun?: boolean;
  paths?: string[] | null;
}

export interface VirtoCommercePageBuilderModuleWebModelsPageBuilderSharedComponentCreateModel {
  content?: any | null;
  name?: string | null;
  storeId?: string | null;
}

export interface VirtoCommercePageBuilderModuleWebModelsPageBuilderSharedComponentUpdateModel {
  name?: string | null;
  storeId?: string | null;
}

export interface VirtoCommercePagesCoreModelsPageDocument {
  content?: string | null;
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  cultureName?: string | null;
  description?: string | null;
  /** @format date-time */
  endDate?: string | null;
  id?: string | null;
  mimeType?: string | null;
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  organizationId?: string | null;
  outerId?: string | null;
  permalink?: string | null;
  source?: string | null;
  /** @format date-time */
  startDate?: string | null;
  status?: VirtoCommercePagesCoreModelsPageDocumentStatus;
  storeId?: string | null;
  title?: string | null;
  userGroups?: string[] | null;
  visibility?: VirtoCommercePagesCoreModelsPageDocumentVisibility;
}

export interface VirtoCommercePagesCoreModelsPageDocumentSearchCriteria {
  /** @format date-time */
  certainDate?: string | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  organizationId?: string | null;
  permalink?: string | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  status?: VirtoCommercePagesCoreModelsPageDocumentStatus | null;
  storeId?: string | null;
  /** @format int32 */
  take?: number;
  userGroups?: string[] | null;
  visibility?: VirtoCommercePagesCoreModelsPageDocumentVisibility;
}

export interface VirtoCommercePagesCoreModelsPageDocumentSearchResult {
  results?: VirtoCommercePagesCoreModelsPageDocument[] | null;
  /** @format int32 */
  totalCount?: number;
}

export type VirtoCommercePagesCoreModelsPageDocumentStatus =
  | "Draft"
  | "NewVersion"
  | "Published"
  | "Archived"
  | "Unpublished"
  | "Deleted";

export type VirtoCommercePagesCoreModelsPageDocumentVisibility =
  | "Private"
  | "Public";

export interface VirtoCommercePaymentModuleCoreModelBankCardInfo {
  bankCardCVV2?: string | null;
  /** @format int32 */
  bankCardMonth?: number;
  bankCardNumber?: string | null;
  bankCardType?: string | null;
  /** @format int32 */
  bankCardYear?: number;
  cardholderName?: string | null;
}

export interface VirtoCommercePaymentModuleCoreModelPaymentMethod {
  readonly allowCartPayment?: boolean;
  allowDeferredPayment?: boolean;
  code?: string | null;
  currency?: string | null;
  description?: string | null;
  /** @format double */
  discountAmount?: number;
  /** @format double */
  readonly discountAmountWithTax?: number;
  id?: string | null;
  isActive?: boolean;
  isAvailableForPartial?: boolean;
  localizedName?: VirtoCommercePlatformCoreCommonLocalizedString | null;
  logoUrl?: string | null;
  name?: string | null;
  readonly paymentMethodGroupType?: VirtoCommercePaymentModuleCoreModelPaymentMethodGroupType;
  readonly paymentMethodType?: VirtoCommercePaymentModuleCoreModelPaymentMethodType;
  /** @format double */
  price?: number;
  /** @format double */
  readonly priceWithTax?: number;
  /** @format int32 */
  priority?: number;
  settings?: VirtoCommercePlatformCoreSettingsObjectSettingEntry[] | null;
  storeId?: string | null;
  taxDetails?: VirtoCommerceCoreModuleCoreTaxTaxDetail[] | null;
  /** @format double */
  taxPercentRate?: number;
  /** @format double */
  readonly taxTotal?: number;
  taxType?: string | null;
  /** @format double */
  readonly total?: number;
  /** @format double */
  readonly totalWithTax?: number;
  readonly typeName?: string | null;
}

export type VirtoCommercePaymentModuleCoreModelPaymentMethodGroupType =
  | "Paypal"
  | "BankCard"
  | "Alternative"
  | "Manual";

export type VirtoCommercePaymentModuleCoreModelPaymentMethodType =
  | "Unknown"
  | "Standard"
  | "Redirection"
  | "PreparedForm";

export type VirtoCommercePaymentModuleCoreModelPaymentStatus =
  | "New"
  | "Pending"
  | "Authorized"
  | "Paid"
  | "PartiallyRefunded"
  | "Refunded"
  | "Voided"
  | "Custom"
  | "Cancelled"
  | "Declined"
  | "Error";

export type VirtoCommercePaymentModuleCoreModelRefundStatus =
  | "Pending"
  | "Rejected"
  | "Processed";

export interface VirtoCommercePaymentModuleCoreModelSearchPaymentMethodsSearchCriteria {
  codes?: string[] | null;
  isActive?: boolean | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  storeId?: string | null;
  /** @format int32 */
  take?: number;
  withoutTransient?: boolean;
}

export interface VirtoCommercePaymentModuleCoreModelSearchPaymentMethodsSearchResult {
  results?: VirtoCommercePaymentModuleCoreModelPaymentMethod[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommercePaymentModuleModelRequestsPostProcessPaymentRequestResult {
  errorMessage?: string | null;
  isSuccess?: boolean;
  newPaymentStatus?: VirtoCommercePaymentModuleCoreModelPaymentStatus;
  orderId?: string | null;
  outerId?: string | null;
  paymentMethod?: VirtoCommercePaymentModuleCoreModelPaymentMethod | null;
  publicParameters?: Record<string, string | null>;
  returnUrl?: string | null;
}

export interface VirtoCommercePaymentModuleModelRequestsProcessPaymentRequestResult {
  errorMessage?: string | null;
  htmlForm?: string | null;
  isSuccess?: boolean;
  newPaymentStatus?: VirtoCommercePaymentModuleCoreModelPaymentStatus;
  outerId?: string | null;
  paymentMethod?: VirtoCommercePaymentModuleCoreModelPaymentMethod | null;
  publicParameters?: Record<string, string | null>;
  redirectUrl?: string | null;
}

export interface VirtoCommercePlatformCoreChangeLogChangeLogSearchCriteria {
  /** @format date-time */
  endDate?: string | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  operationTypes?: VirtoCommercePlatformCoreCommonEntryState[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format date-time */
  startDate?: string | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommercePlatformCoreChangeLogChangeLogSearchResult {
  results?: VirtoCommercePlatformCoreChangeLogOperationLog[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommercePlatformCoreChangeLogOperationLog {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  detail?: string | null;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  objectId?: string | null;
  objectType?: string | null;
  operationType?: VirtoCommercePlatformCoreCommonEntryState;
}

export type VirtoCommercePlatformCoreCommonEntryState =
  | "Detached"
  | "Unchanged"
  | "Added"
  | "Deleted"
  | "Modified";

export interface VirtoCommercePlatformCoreCommonKeyValue {
  key?: string | null;
  value?: string | null;
}

export interface VirtoCommercePlatformCoreCommonLocalizedString {
  readonly values?: Record<string, string | null>;
}

export interface VirtoCommercePlatformCoreCommonSemanticVersion {
  /** @format int32 */
  readonly major?: number;
  /** @format int32 */
  readonly minor?: number;
  /** @format int32 */
  readonly patch?: number;
  readonly prerelease?: string | null;
}

export type VirtoCommercePlatformCoreCommonSortDirection =
  | "Ascending"
  | "Descending";

export interface VirtoCommercePlatformCoreCommonSortInfo {
  sortColumn?: string | null;
  sortDirection?: VirtoCommercePlatformCoreCommonSortDirection;
}

export interface VirtoCommercePlatformCoreCommonTenantIdentity {
  id?: string | null;
  readonly isEmpty?: boolean;
  readonly isValid?: boolean;
  type?: string | null;
}

export interface VirtoCommercePlatformCoreDeveloperToolsDeveloperToolDescriptor {
  isExternal?: boolean;
  name?: string | null;
  permission?: string | null;
  /** @format int32 */
  sortOrder?: number;
  url?: string | null;
}

export interface VirtoCommercePlatformCoreDynamicPropertiesDynamicObjectProperty {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  description?: string | null;
  displayNames?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicPropertyName[]
    | null;
  /** @format int32 */
  displayOrder?: number | null;
  id?: string | null;
  isArray?: boolean;
  isDictionary?: boolean;
  isMultilingual?: boolean;
  isRequired?: boolean;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  objectId?: string | null;
  objectType?: string | null;
  valueType?: VirtoCommercePlatformCoreDynamicPropertiesDynamicPropertyValueType;
  values?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicPropertyObjectValue[]
    | null;
}

export interface VirtoCommercePlatformCoreDynamicPropertiesDynamicProperty {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  description?: string | null;
  displayNames?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicPropertyName[]
    | null;
  /** @format int32 */
  displayOrder?: number | null;
  id?: string | null;
  isArray?: boolean;
  isDictionary?: boolean;
  isMultilingual?: boolean;
  isRequired?: boolean;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  objectType?: string | null;
  valueType?: VirtoCommercePlatformCoreDynamicPropertiesDynamicPropertyValueType;
}

export interface VirtoCommercePlatformCoreDynamicPropertiesDynamicPropertyDictionaryItem {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  displayNames?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicPropertyDictionaryItemName[]
    | null;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  propertyId?: string | null;
}

export interface VirtoCommercePlatformCoreDynamicPropertiesDynamicPropertyDictionaryItemName {
  locale?: string | null;
  name?: string | null;
}

export interface VirtoCommercePlatformCoreDynamicPropertiesDynamicPropertyDictionaryItemSearchCriteria {
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  propertyId?: string | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommercePlatformCoreDynamicPropertiesDynamicPropertyDictionaryItemSearchResult {
  results?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicPropertyDictionaryItem[]
    | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommercePlatformCoreDynamicPropertiesDynamicPropertyName {
  locale?: string | null;
  name?: string | null;
}

export interface VirtoCommercePlatformCoreDynamicPropertiesDynamicPropertyObjectValue {
  locale?: string | null;
  objectId?: string | null;
  objectType?: string | null;
  propertyId?: string | null;
  propertyName?: string | null;
  value?: object | null;
  valueId?: string | null;
  valueType?: VirtoCommercePlatformCoreDynamicPropertiesDynamicPropertyValueType;
}

export interface VirtoCommercePlatformCoreDynamicPropertiesDynamicPropertySearchCriteria {
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
  readonly typeName?: string | null;
}

export interface VirtoCommercePlatformCoreDynamicPropertiesDynamicPropertySearchResult {
  results?: VirtoCommercePlatformCoreDynamicPropertiesDynamicProperty[] | null;
  /** @format int32 */
  totalCount?: number;
}

export type VirtoCommercePlatformCoreDynamicPropertiesDynamicPropertyValueType =
  | "Undefined"
  | "ShortText"
  | "LongText"
  | "Integer"
  | "Decimal"
  | "DateTime"
  | "Boolean"
  | "Html"
  | "Image";

export interface VirtoCommercePlatformCoreExportImportPushNotificationsPlatformExportPushNotification {
  /** @format date-time */
  created?: string;
  creator?: string | null;
  description?: string | null;
  downloadUrl?: string | null;
  /** @format int64 */
  readonly errorCount?: number;
  errors?: string[] | null;
  /** @format date-time */
  finished?: string | null;
  id?: string | null;
  isNew?: boolean;
  jobId?: string | null;
  notifyType?: string | null;
  /** @format int64 */
  processedCount?: number;
  progressLog?: VirtoCommercePlatformCoreModularityProgressMessage[] | null;
  /** @format int32 */
  repeatCount?: number;
  serverId?: string | null;
  title?: string | null;
  /** @format int64 */
  totalCount?: number;
}

export interface VirtoCommercePlatformCoreJobsEnqueueOptions {
  /** @format int32 */
  maxRetryAttempts?: number | null;
  progressNotificationId?: string | null;
  queue?: string | null;
  reportProgress?: boolean;
  title?: string | null;
  uniqueKey?: string | null;
}

export interface VirtoCommercePlatformCoreJobsJob {
  completed?: boolean;
  id?: string | null;
  state?: string | null;
}

export type VirtoCommercePlatformCoreModularityAppPlacement =
  | "AppMenu"
  | "MainMenu"
  | "Hidden";

export interface VirtoCommercePlatformCoreModularityModuleIdentity {
  id?: string | null;
  optional?: boolean;
  version?: VirtoCommercePlatformCoreCommonSemanticVersion | null;
}

export interface VirtoCommercePlatformCoreModularityModuleInstallRequest {
  id?: string | null;
  version?: string | null;
}

export interface VirtoCommercePlatformCoreModularityProgressMessage {
  level?: VirtoCommercePlatformCoreModularityProgressMessageLevel;
  message?: string | null;
}

export type VirtoCommercePlatformCoreModularityProgressMessageLevel =
  | "Info"
  | "Warning"
  | "Debug"
  | "Error";

export interface VirtoCommercePlatformCoreModularityPushNotificationsModuleAutoInstallPushNotification {
  /** @format date-time */
  created?: string;
  creator?: string | null;
  description?: string | null;
  /** @format int32 */
  readonly errorCount?: number;
  /** @format date-time */
  finished?: string | null;
  id?: string | null;
  isNew?: boolean;
  notifyType?: string | null;
  progressLog?: VirtoCommercePlatformCoreModularityProgressMessage[] | null;
  /** @format int32 */
  repeatCount?: number;
  serverId?: string | null;
  /** @format date-time */
  started?: string | null;
  title?: string | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommercePlatformCoreModularityPushNotificationsModulePushNotification {
  /** @format date-time */
  created?: string;
  creator?: string | null;
  description?: string | null;
  /** @format int32 */
  readonly errorCount?: number;
  /** @format date-time */
  finished?: string | null;
  id?: string | null;
  isNew?: boolean;
  notifyType?: string | null;
  progressLog?: VirtoCommercePlatformCoreModularityProgressMessage[] | null;
  /** @format int32 */
  repeatCount?: number;
  serverId?: string | null;
  /** @format date-time */
  started?: string | null;
  title?: string | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommercePlatformCorePushNotificationsPushNotification {
  /** @format date-time */
  created?: string;
  creator?: string | null;
  description?: string | null;
  id?: string | null;
  isNew?: boolean;
  notifyType?: string | null;
  /** @format int32 */
  repeatCount?: number;
  serverId?: string | null;
  title?: string | null;
}

export interface VirtoCommercePlatformCorePushNotificationsPushNotificationSearchCriteria {
  /** @format date-time */
  endDate?: string | null;
  ids?: string[] | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  onlyNew?: boolean;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format date-time */
  startDate?: string | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommercePlatformCorePushNotificationsPushNotificationSearchResult {
  /** @format int32 */
  newCount?: number;
  notifyEvents?:
    | VirtoCommercePlatformCorePushNotificationsPushNotification[]
    | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommercePlatformCoreSecurityApplicationUser {
  /** @format int32 */
  accessFailedCount?: number;
  concurrencyStamp?: string | null;
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  email?: string | null;
  emailConfirmed?: boolean;
  id?: string | null;
  isAdministrator?: boolean;
  /** @format date-time */
  lastLoginDate?: string | null;
  /** @format date-time */
  lastPasswordChangeRequestDate?: string | null;
  /** @format date-time */
  lastPasswordChangedDate?: string | null;
  lockoutEnabled?: boolean;
  /** @format date-time */
  lockoutEnd?: string | null;
  logins?: VirtoCommercePlatformCoreSecurityApplicationUserLogin[] | null;
  memberId?: string | null;
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  normalizedEmail?: string | null;
  normalizedUserName?: string | null;
  password?: string | null;
  passwordExpired?: boolean;
  passwordHash?: string | null;
  phoneNumber?: string | null;
  phoneNumberConfirmed?: boolean;
  photoUrl?: string | null;
  roles?: VirtoCommercePlatformCoreSecurityRole[] | null;
  securityStamp?: string | null;
  status?: string | null;
  storeId?: string | null;
  twoFactorEnabled?: boolean;
  userName?: string | null;
  userType?: string | null;
}

export interface VirtoCommercePlatformCoreSecurityApplicationUserLogin {
  loginProvider?: string | null;
  providerKey?: string | null;
}

export interface VirtoCommercePlatformCoreSecurityPermission {
  assignedScopes?: VirtoCommercePlatformCoreSecurityPermissionScope[] | null;
  readonly availableScopes?:
    | VirtoCommercePlatformCoreSecurityPermissionScope[]
    | null;
  groupName?: string | null;
  moduleId?: string | null;
  name?: string | null;
}

export interface VirtoCommercePlatformCoreSecurityPermissionScope {
  label?: string | null;
  scope?: string | null;
  type?: string | null;
}

export interface VirtoCommercePlatformCoreSecurityRole {
  concurrencyStamp?: string | null;
  description?: string | null;
  id?: string | null;
  name?: string | null;
  normalizedName?: string | null;
  permissions?: VirtoCommercePlatformCoreSecurityPermission[] | null;
}

export interface VirtoCommercePlatformCoreSecurityRoleSearchCriteria {
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommercePlatformCoreSecuritySearchRoleSearchResult {
  results?: VirtoCommercePlatformCoreSecurityRole[] | null;
  readonly roles?: VirtoCommercePlatformCoreSecurityRole[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommercePlatformCoreSecuritySearchUserSearchResult {
  results?: VirtoCommercePlatformCoreSecurityApplicationUser[] | null;
  /** @format int32 */
  totalCount?: number;
  readonly users?: VirtoCommercePlatformCoreSecurityApplicationUser[] | null;
}

export interface VirtoCommercePlatformCoreSecuritySearchUserSessionSearchCriteria {
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
  userId?: string | null;
}

export interface VirtoCommercePlatformCoreSecuritySearchUserSessionSearchResult {
  results?: VirtoCommercePlatformCoreSecurityUserSession[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommercePlatformCoreSecuritySecurityResult {
  errors?: string[] | null;
  succeeded?: boolean;
}

export interface VirtoCommercePlatformCoreSecuritySignInLogUserSignInLog {
  clientId?: string | null;
  /** @format date-time */
  createdDate?: string;
  failureReason?: string | null;
  host?: string | null;
  id?: string | null;
  ipAddress?: string | null;
  memberId?: string | null;
  operatorUserId?: string | null;
  operatorUserName?: string | null;
  organizationId?: string | null;
  organizationName?: string | null;
  provider?: string | null;
  sessionId?: string | null;
  signInType?: string | null;
  storeId?: string | null;
  storeName?: string | null;
  succeeded?: boolean;
  userAgent?: string | null;
  userId?: string | null;
  userName?: string | null;
}

export interface VirtoCommercePlatformCoreSecuritySignInLogUserSignInLogSearchCriteria {
  /** @format date-time */
  endDate?: string | null;
  failureReasons?: string[] | null;
  ipAddress?: string | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  organizationId?: string | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  signInTypes?: string[] | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format date-time */
  startDate?: string | null;
  storeId?: string | null;
  succeeded?: boolean | null;
  /** @format int32 */
  take?: number;
  userId?: string | null;
  userName?: string | null;
  withoutStore?: boolean | null;
}

export interface VirtoCommercePlatformCoreSecuritySignInLogUserSignInLogSearchResult {
  results?: VirtoCommercePlatformCoreSecuritySignInLogUserSignInLog[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommercePlatformCoreSecuritySignInLogUserSignInLogStats {
  /** @format int32 */
  distinctUserCount?: number;
  /** @format int32 */
  failedCount?: number;
  failureReasonBreakdown?:
    | VirtoCommercePlatformCoreSecuritySignInLogUserSignInLogStatsEntry[]
    | null;
  /** @format int32 */
  impersonationCount?: number;
  /** @format int32 */
  previousDistinctUserCount?: number | null;
  /** @format int32 */
  previousFailedCount?: number | null;
  /** @format int32 */
  previousImpersonationCount?: number | null;
  /** @format int32 */
  previousTotalCount?: number | null;
  recordingEnabled?: boolean;
  signInsByOrganization?:
    | VirtoCommercePlatformCoreSecuritySignInLogUserSignInLogStatsEntry[]
    | null;
  signInsByStore?:
    | VirtoCommercePlatformCoreSecuritySignInLogUserSignInLogStatsEntry[]
    | null;
  timeline?:
    | VirtoCommercePlatformCoreSecuritySignInLogUserSignInLogTimelinePoint[]
    | null;
  timelineGranularity?: string | null;
  topFailedIpAddresses?:
    | VirtoCommercePlatformCoreSecuritySignInLogUserSignInLogStatsEntry[]
    | null;
  topFailedUserNames?:
    | VirtoCommercePlatformCoreSecuritySignInLogUserSignInLogStatsEntry[]
    | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommercePlatformCoreSecuritySignInLogUserSignInLogStatsEntry {
  /** @format int32 */
  count?: number;
  key?: string | null;
}

export interface VirtoCommercePlatformCoreSecuritySignInLogUserSignInLogTimelinePoint {
  /** @format int32 */
  failedCount?: number;
  /** @format int32 */
  succeededCount?: number;
  /** @format date-time */
  timestamp?: string;
}

export interface VirtoCommercePlatformCoreSecurityUserApiKey {
  apiKey?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  isActive?: boolean;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  userId?: string | null;
  userName?: string | null;
}

export interface VirtoCommercePlatformCoreSecurityUserSearchCriteria {
  emailConfirmed?: boolean | null;
  keyword?: string | null;
  languageCode?: string | null;
  /**
   * @deprecated
   * @format date-time
   */
  lasLoginDate?: string | null;
  /** @format date-time */
  loginEndDate?: string | null;
  /** @format date-time */
  loginStartDate?: string | null;
  memberId?: string | null;
  memberIds?: string[] | null;
  /** @format date-time */
  modifiedSinceDate?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  onlyLocked?: boolean;
  onlyUnlocked?: boolean;
  responseGroup?: string | null;
  roles?: string[] | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  status?: string | null;
  storeId?: string | null;
  /** @format int32 */
  take?: number;
  userType?: string | null;
}

export interface VirtoCommercePlatformCoreSecurityUserSession {
  /** @format date-time */
  createdDate?: string;
  /** @format date-time */
  expirationDate?: string;
  id?: string | null;
  ipAddress?: string | null;
  isImpersonated?: boolean;
  operatorUserId?: string | null;
  operatorUserName?: string | null;
  sessionGroupId?: string | null;
  userAgent?: string | null;
}

export interface VirtoCommercePlatformCoreSettingsDictionaryItem {
  alias?: string | null;
  localizedValues?: VirtoCommercePlatformCoreSettingsLocalizedValue[] | null;
}

export interface VirtoCommercePlatformCoreSettingsLocalizableSetting {
  isLocalizable?: boolean;
  items?: VirtoCommercePlatformCoreSettingsDictionaryItem[] | null;
  name?: string | null;
}

export interface VirtoCommercePlatformCoreSettingsLocalizableSettingsAndLanguages {
  languages?: string[] | null;
  settings?: VirtoCommercePlatformCoreSettingsLocalizableSetting[] | null;
}

export interface VirtoCommercePlatformCoreSettingsLocalizedValue {
  languageCode?: string | null;
  value?: string | null;
}

export interface VirtoCommercePlatformCoreSettingsObjectSettingEntry {
  allowedValues?: object[] | null;
  defaultValue?: object | null;
  displayName?: string | null;
  groupName?: string | null;
  id?: string | null;
  isDictionary?: boolean;
  isHidden?: boolean;
  isLocalizable?: boolean;
  isPublic?: boolean;
  isReadOnly?: boolean;
  isRequired?: boolean;
  readonly itHasValues?: boolean;
  moduleId?: string | null;
  name?: string | null;
  objectId?: string | null;
  objectType?: string | null;
  restartRequired?: boolean;
  tenant?: string | null;
  value?: object | null;
  valueType?: VirtoCommercePlatformCoreSettingsSettingValueType;
}

export interface VirtoCommercePlatformCoreSettingsSettingPropertySchema {
  allowedValues?: object[] | null;
  assignedToTenants?: string[] | null;
  defaultValue?: object | null;
  displayName?: string | null;
  groupName?: string | null;
  isDictionary?: boolean;
  isLocalizable?: boolean;
  isReadOnly?: boolean;
  isRequired?: boolean;
  moduleId?: string | null;
  name?: string | null;
  restartRequired?: boolean;
  valueType?: VirtoCommercePlatformCoreSettingsSettingValueType;
}

export type VirtoCommercePlatformCoreSettingsSettingValueType =
  | "ShortText"
  | "LongText"
  | "Integer"
  | "Decimal"
  | "DateTime"
  | "Boolean"
  | "SecureString"
  | "Json"
  | "PositiveInteger"
  | "Cron";

export interface VirtoCommercePlatformWebLicensingLicense {
  customerEmail?: string | null;
  customerName?: string | null;
  /** @format date-time */
  expirationDate?: string;
  rawLicense?: string | null;
  type?: string | null;
}

export interface VirtoCommercePlatformWebModelChangedEntitiesRequest {
  entityNames?: string[] | null;
  /** @format date-time */
  modifiedSince?: string;
}

export interface VirtoCommercePlatformWebModelChangedEntitiesResponse {
  entities?: VirtoCommercePlatformWebModelChangedEntity[] | null;
}

export interface VirtoCommercePlatformWebModelChangedEntity {
  /** @format date-time */
  modifiedDate?: string;
  name?: string | null;
}

export interface VirtoCommercePlatformWebModelDiagnosticsSystemInfo {
  is64BitOperatingSystem?: boolean;
  is64BitProcess?: boolean;
  databaseProvider?: string | null;
  environmentName?: string | null;
  installedModules?:
    | VirtoCommercePlatformWebModularityModuleDescriptor[]
    | null;
  license?: VirtoCommercePlatformWebLicensingLicense | null;
  platformVersion?: string | null;
  runtimeIdentifier?: string | null;
  version?: string | null;
}

export interface VirtoCommercePlatformWebModelLastModifiedResponse {
  /** @format date-time */
  lastModifiedDate?: string;
  scope?: string | null;
}

export interface VirtoCommercePlatformWebModelModularityAppDescriptor {
  description?: string | null;
  iconUrl?: string | null;
  id?: string | null;
  permission?: string | null;
  /**
   * Where the app surfaces in the admin navigation
   * (`AppMenu` / `MainMenu` / `Hidden`).
   */
  placement?: VirtoCommercePlatformCoreModularityAppPlacement;
  relativeUrl?: string | null;
  /**
   * Deprecated. Use VirtoCommerce.Platform.Web.Model.Modularity.AppDescriptor.Placement instead. Equivalent to
   * `Placement == AppPlacement.MainMenu`; kept on the JSON
   * contract for backwards compatibility.
   */
  supportEmbeddedMode?: boolean;
  title?: string | null;
}

/**
 * Response shape for `GET /api/apps/{appId}/manifest`.
 * Returns the host app metadata plus a topologically ordered, permission-filtered
 * list of plugins the host should load.
 */
export interface VirtoCommercePlatformWebModelModularityAppManifestResponse {
  /** Echo of the requested app id (e.g. `vc-shell-marketplace`, `system-operations`, `platform`). */
  appId?: string | null;
  /**
   * Plugins to load, in topological dependency order of their owning modules.
   * Already filtered by current user permissions and (for Module Federation
   * hosts) by host-app discovery folder convention.
   */
  plugins?: VirtoCommercePlatformWebModelModularityPluginEntry[] | null;
  /**
   * Display title of the host app, taken from the owning module's
   * `<app>` declaration in `module.manifest`.
   */
  title?: string | null;
  /**
   * Version of the host app — taken from the running platform when
   * VirtoCommerce.Platform.Web.Model.Modularity.AppManifestResponse.AppId is the reserved `platform` id, otherwise
   * from the module that declares the `<app>` in its
   * `module.manifest`. Useful for clients that want to surface the
   * host's version (e.g. footer banner, support diagnostics) without
   * a second round-trip.
   */
  version?: string | null;
}

/**
 * One asset belonging to a plugin (script, stylesheet, etc.). Carries the
 * information a client-side loader needs to build the right HTML element
 * with proper cache busting.
 */
export interface VirtoCommercePlatformWebModelModularityContentFile {
  /**
   * Cache-busting hash (`?v={hash}`). Stable across requests as long
   * as the file's last-write time is unchanged. `null` when the file
   * doesn't exist on disk (e.g. a manifest reference that fell back to
   * convention defaults).
   */
  hash?: string | null;
  /**
   * Absolute URL path served by the platform's static-file middleware,
   * e.g. `/modules/$(VirtoCommerce.Catalog)/dist/app.js`.
   */
  path?: string | null;
  /**
   * Asset kind. See VirtoCommerce.Platform.Core.Modularity.ContentFileTypes
   * for the canonical values. Lower-case string so the JSON contract is
   * stable against future C# enum renames.
   */
  type?: string | null;
}

/**
 * One plugin contribution to a host app, returned by
 * `GET /api/apps/{appId}/manifest`.
 */
export interface VirtoCommercePlatformWebModelModularityPluginEntry {
  /**
   * Additional assets the host should preload alongside VirtoCommerce.Platform.Web.Model.Modularity.PluginEntry.Entry
   * (typically stylesheets). Each carries its own type so a generic loader
   * can dispatch on it.
   */
  contentFiles?: VirtoCommercePlatformWebModelModularityContentFile[] | null;
  /**
   * The plugin's primary file. For Module Federation plugins this is the
   * federation entry (`remoteEntry.js`). For the legacy AngularJS host
   * it is the module bundle (`dist/app.js`). Always a script.
   */
  entry?: VirtoCommercePlatformWebModelModularityContentFile | null;
  /**
   * Unique plugin id within the (host app, request) tuple.
   * Defaults to the owning .NET module id (e.g. `VirtoCommerce.MarketplaceReviews`).
   */
  id?: string | null;
  /** Module Federation coordinates. `null` for the legacy AngularJS host. */
  remote?: VirtoCommercePlatformWebModelModularityPluginRemote | null;
  /** Plugin version. Defaults to the parent module version. */
  version?: string | null;
}

/**
 * Module Federation remote coordinates for a plugin. Mirrors the shape
 * expected by `@module-federation/runtime`.
 */
export interface VirtoCommercePlatformWebModelModularityPluginRemote {
  exposed?: string | null;
  name?: string | null;
}

export interface VirtoCommercePlatformWebModelSecurityChangePasswordRequest {
  newPassword?: string | null;
  oldPassword?: string | null;
  userName?: string | null;
}

export interface VirtoCommercePlatformWebModelSecurityConfirmEmailRequest {
  token?: string | null;
}

export interface VirtoCommercePlatformWebModelSecurityExternalSignInProviderInfo {
  authenticationType?: string | null;
  displayName?: string | null;
  logoUrl?: string | null;
}

export interface VirtoCommercePlatformWebModelSecurityLoginRequest {
  password?: string | null;
  rememberMe?: boolean;
  userName?: string | null;
}

export interface VirtoCommercePlatformWebModelSecurityLoginType {
  authenticationType?: string | null;
  enabled?: boolean;
  hasLoginForm?: boolean;
  /** @format int32 */
  priority?: number;
}

export interface VirtoCommercePlatformWebModelSecurityOAuthAppSearchCriteria {
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommercePlatformWebModelSecurityOAuthAppSearchResult {
  results?: OpenIddictAbstractionsOpenIddictApplicationDescriptor[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommercePlatformWebModelSecurityResetPasswordConfirmRequest {
  newPassword?: string | null;
  token?: string | null;
}

export interface VirtoCommercePlatformWebModelSecurityResetPasswordRequest {
  forcePasswordChangeOnNextSignIn?: boolean;
  newPassword?: string | null;
}

export interface VirtoCommercePlatformWebModelSecurityUserDetail {
  authenticationMethod?: string | null;
  canAccessAdminUI?: boolean;
  /** @format int32 */
  daysTillPasswordExpiry?: number;
  id?: string | null;
  isAdministrator?: boolean;
  isSsoAuthenticationMethod?: boolean;
  memberId?: string | null;
  passwordExpired?: boolean;
  permissions?: string[] | null;
  userName?: string | null;
}

export interface VirtoCommercePlatformWebModelSecurityUserLockedResult {
  locked?: boolean;
}

export interface VirtoCommercePlatformWebModelSecurityValidatePasswordResetTokenRequest {
  token?: string | null;
}

export interface VirtoCommercePlatformWebModelSecurityVerifyTokenRequest {
  purpose?: string | null;
  token?: string | null;
  tokenProvider?: string | null;
}

export interface VirtoCommercePlatformWebModularityModuleDescriptor {
  authors?: string[] | null;
  copyright?: string | null;
  dependencies?: VirtoCommercePlatformCoreModularityModuleIdentity[] | null;
  description?: string | null;
  groups?: string[] | null;
  iconUrl?: string | null;
  id?: string | null;
  installedVersion?: VirtoCommercePlatformCoreModularityModuleIdentity | null;
  isInstalled?: boolean;
  isRemovable?: boolean;
  licenseUrl?: string | null;
  owners?: string[] | null;
  packageUrl?: string | null;
  platformVersion?: string | null;
  projectUrl?: string | null;
  releaseNotes?: string | null;
  requireLicenseAcceptance?: boolean;
  tags?: string | null;
  title?: string | null;
  validationErrors?: string[] | null;
  version?: string | null;
}

export interface VirtoCommercePricingModuleCoreModelConditionsPriceConditionTree {
  all?: boolean;
  availableChildren?:
    | VirtoCommerceCoreModuleCoreConditionsIConditionTree[]
    | null;
  children?: VirtoCommerceCoreModuleCoreConditionsIConditionTree[] | null;
  readonly id?: string | null;
  not?: boolean;
}

export interface VirtoCommercePricingModuleCoreModelMergedPrice {
  currency?: string | null;
  id?: string | null;
  /** @format double */
  list?: number;
  /** @format int32 */
  minQuantity?: number;
  pricelistId?: string | null;
  productId?: string | null;
  /** @format double */
  sale?: number | null;
  state?: VirtoCommercePricingModuleCoreModelMergedPriceState;
}

export interface VirtoCommercePricingModuleCoreModelMergedPriceGroup {
  /** @format int32 */
  groupPricesCount?: number;
  groupState?: VirtoCommercePricingModuleCoreModelMergedPriceState;
  /** @format double */
  maxListPrice?: number;
  /** @format double */
  maxSalePrice?: number | null;
  /** @format double */
  minListPrice?: number;
  /** @format double */
  minSalePrice?: number | null;
  productCode?: string | null;
  productId?: string | null;
  productImgSrc?: string | null;
  productName?: string | null;
}

export type VirtoCommercePricingModuleCoreModelMergedPriceState =
  | "Base"
  | "New"
  | "Updated";

export interface VirtoCommercePricingModuleCoreModelPrice {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  currency?: string | null;
  /** @format double */
  readonly effectiveValue?: number;
  /**
   * Optional end date for this price, so that we can prepare prices ahead of time.
   * If end date equals now, this price will not be active.
   * @format date-time
   */
  endDate?: string | null;
  id?: string | null;
  /** @format double */
  list?: number;
  /** @format int32 */
  minQuantity?: number;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  outerId?: string | null;
  pricelist?: VirtoCommercePricingModuleCoreModelPricelist | null;
  pricelistId?: string | null;
  productId?: string | null;
  /** @format double */
  sale?: number | null;
  /**
   * Optional start date for this price, so that we can prepare prices ahead of time.
   * If start date equals now, this price will be active.
   * @format date-time
   */
  startDate?: string | null;
}

export interface VirtoCommercePricingModuleCoreModelPriceEvaluationContext {
  catalogId?: string | null;
  /** @format date-time */
  certainDate?: string | null;
  contextObject?: object | null;
  currency?: string | null;
  currentUrl?: string | null;
  customerId?: string | null;
  geoCity?: string | null;
  geoConnectionType?: string | null;
  geoContinent?: string | null;
  geoCountry?: string | null;
  geoIpRoutingType?: string | null;
  geoIspSecondLevel?: string | null;
  geoIspTopLevel?: string | null;
  geoState?: string | null;
  geoTimeZone?: string | null;
  geoZipCode?: string | null;
  language?: string | null;
  organizationId?: string | null;
  pricelistIds?: string[] | null;
  pricelists?: VirtoCommercePricingModuleCoreModelPricelist[] | null;
  productIds?: string[] | null;
  /** @format double */
  quantity?: number;
  referredUrl?: string | null;
  returnAllMatchedPrices?: boolean;
  /** @format int32 */
  shopperAge?: number;
  shopperGender?: string | null;
  shopperSearchedPhraseInStore?: string | null;
  shopperSearchedPhraseOnInternet?: string | null;
  skipAssignmentValidation?: boolean;
  storeId?: string | null;
  /** Any tags or groups belongs to user such as VIP, Wholesaler etc */
  userGroups?: string[] | null;
}

export interface VirtoCommercePricingModuleCoreModelPricelist {
  assignments?: VirtoCommercePricingModuleCoreModelPricelistAssignment[] | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  currency?: string | null;
  description?: string | null;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  outerId?: string | null;
  prices?: VirtoCommercePricingModuleCoreModelPrice[] | null;
  /** @format int32 */
  priority?: number;
}

/** Used to assign pricelist to specific catalog by using conditional expression */
export interface VirtoCommercePricingModuleCoreModelPricelistAssignment {
  catalogId?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  description?: string | null;
  /** List of conditions and rules to define Prices Assignment is valid */
  dynamicExpression?: VirtoCommercePricingModuleCoreModelConditionsPriceConditionTree | null;
  /**
   * End of period when Prices Assignment is valid. Null value means no limit
   * @format date-time
   */
  endDate?: string | null;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  outerId?: string | null;
  pricelist?: VirtoCommercePricingModuleCoreModelPricelist | null;
  pricelistId?: string | null;
  /**
   * If two PricelistAssignments satisfies the conditions and rules, will use one with the greater priority
   * @format int32
   */
  priority?: number;
  /**
   * Start of period when Prices Assignment is valid. Null value means no limit
   * @format date-time
   */
  startDate?: string | null;
  storeId?: string | null;
}

export interface VirtoCommercePricingModuleCoreModelProductPrice {
  /** List prices for the products. It includes tiered prices also. (Depending on the quantity, for example) */
  prices?: VirtoCommercePricingModuleCoreModelPrice[] | null;
  product?: VirtoCommerceCatalogModuleCoreModelCatalogProduct | null;
  productId?: string | null;
}

export interface VirtoCommercePricingModuleCoreModelSearchMergedPriceGroupSearchResult {
  results?: VirtoCommercePricingModuleCoreModelMergedPriceGroup[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommercePricingModuleCoreModelSearchMergedPriceSearchCriteria {
  all?: boolean;
  basePriceListId?: string | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  priorityPriceListId?: string | null;
  productIds?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommercePricingModuleCoreModelSearchMergedPriceSearchResult {
  results?: VirtoCommercePricingModuleCoreModelMergedPrice[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommercePricingModuleCoreModelSearchPricelistAssignmentSearchResult {
  results?: VirtoCommercePricingModuleCoreModelPricelistAssignment[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommercePricingModuleCoreModelSearchPricelistSearchResult {
  results?: VirtoCommercePricingModuleCoreModelPricelist[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommercePricingModuleCoreModelSearchPricesSearchCriteria {
  groupByProducts?: boolean;
  keyword?: string | null;
  languageCode?: string | null;
  /** @format date-time */
  modifiedSince?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  priceListId?: string | null;
  priceListIds?: string[] | null;
  productId?: string | null;
  productIds?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommercePricingModuleCoreModelSearchProductPriceSearchResult {
  results?: VirtoCommercePricingModuleCoreModelProductPrice[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceQuoteModuleCoreModelsQuoteAttachment {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  mimeType?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  /** @format int64 */
  size?: number;
  url?: string | null;
}

export interface VirtoCommerceQuoteModuleCoreModelsQuoteConfigurationItem {
  catalogId?: string | null;
  categoryId?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  customText?: string | null;
  files?: VirtoCommerceQuoteModuleCoreModelsQuoteConfigurationItemFile[] | null;
  id?: string | null;
  imageUrl?: string | null;
  lineItemId?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  productId?: string | null;
  /** @format int32 */
  quantity?: number;
  sku?: string | null;
  type?: string | null;
}

export interface VirtoCommerceQuoteModuleCoreModelsQuoteConfigurationItemFile {
  configurationItemId?: string | null;
  contentType?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  /** @format int64 */
  size?: number;
  url?: string | null;
}

export interface VirtoCommerceQuoteModuleCoreModelsQuoteItem {
  catalogId?: string | null;
  categoryId?: string | null;
  comment?: string | null;
  configurationItems?:
    | VirtoCommerceQuoteModuleCoreModelsQuoteConfigurationItem[]
    | null;
  currency?: string | null;
  id?: string | null;
  imageUrl?: string | null;
  isConfigured?: boolean;
  /** @format double */
  listPrice?: number;
  name?: string | null;
  product?: VirtoCommerceCatalogModuleCoreModelCatalogProduct | null;
  productId?: string | null;
  proposalPrices?: VirtoCommerceQuoteModuleCoreModelsTierPrice[] | null;
  /** @format int32 */
  quantity?: number;
  /** @format double */
  salePrice?: number;
  selectedTierPrice?: VirtoCommerceQuoteModuleCoreModelsTierPrice | null;
  sku?: string | null;
  taxType?: string | null;
}

export interface VirtoCommerceQuoteModuleCoreModelsQuoteRequest {
  addresses?: QuoteAddress[] | null;
  attachments?: VirtoCommerceQuoteModuleCoreModelsQuoteAttachment[] | null;
  cancelReason?: string | null;
  /** @format date-time */
  cancelledDate?: string | null;
  channelId?: string | null;
  comment?: string | null;
  coupon?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  currency?: string | null;
  customerId?: string | null;
  customerName?: string | null;
  dynamicProperties?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicObjectProperty[]
    | null;
  employeeId?: string | null;
  employeeName?: string | null;
  enableNotification?: boolean;
  /** @format date-time */
  expirationDate?: string | null;
  id?: string | null;
  innerComment?: string | null;
  isAnonymous?: boolean;
  isCancelled?: boolean;
  isLocked?: boolean;
  items?: VirtoCommerceQuoteModuleCoreModelsQuoteItem[] | null;
  languageCode?: string | null;
  /** @format double */
  manualRelDiscountAmount?: number;
  /** @format double */
  manualShippingTotal?: number;
  /** @format double */
  manualSubTotal?: number;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  number?: string | null;
  readonly objectType?: string | null;
  operationsLog?: VirtoCommercePlatformCoreChangeLogOperationLog[] | null;
  organizationId?: string | null;
  organizationName?: string | null;
  /** @format date-time */
  reminderDate?: string | null;
  shipmentMethod?: VirtoCommerceQuoteModuleCoreModelsShipmentMethod | null;
  status?: string | null;
  storeId?: string | null;
  tag?: string | null;
  taxDetails?: VirtoCommerceCoreModuleCoreTaxTaxDetail[] | null;
  totals?: VirtoCommerceQuoteModuleCoreModelsQuoteRequestTotals | null;
}

export interface VirtoCommerceQuoteModuleCoreModelsQuoteRequestSearchCriteria {
  currency?: string | null;
  customerId?: string | null;
  /** @format date-time */
  endDate?: string | null;
  keyword?: string | null;
  languageCode?: string | null;
  number?: string | null;
  numberKeyword?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  organizationId?: string | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format date-time */
  startDate?: string | null;
  status?: string | null;
  statuses?: string[] | null;
  storeId?: string | null;
  tag?: string | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceQuoteModuleCoreModelsQuoteRequestSearchResult {
  results?: VirtoCommerceQuoteModuleCoreModelsQuoteRequest[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceQuoteModuleCoreModelsQuoteRequestTotals {
  /** @format double */
  readonly adjustmentQuoteExlTax?: number;
  /** @format double */
  discountTotal?: number;
  /** @format double */
  readonly grandTotalExlTax?: number;
  /** @format double */
  readonly grandTotalInclTax?: number;
  /** @format double */
  originalSubTotalExlTax?: number;
  /** @format double */
  shippingTotal?: number;
  /** @format double */
  subTotalExlTax?: number;
  /** @format double */
  taxTotal?: number;
}

export interface VirtoCommerceQuoteModuleCoreModelsShipmentMethod {
  currency?: string | null;
  logoUrl?: string | null;
  optionName?: string | null;
  /** @format double */
  price?: number;
  shipmentMethodCode?: string | null;
  typeName?: string | null;
}

export interface VirtoCommerceQuoteModuleCoreModelsTierPrice {
  /** @format double */
  price?: number;
  /** @format int64 */
  quantity?: number;
}

export interface VirtoCommerceSearchModuleCoreModelGeoDistanceFilter {
  /** @format double */
  distance?: number;
  fieldName?: string | null;
  location?: VirtoCommerceSearchModuleCoreModelGeoPoint | null;
}

export interface VirtoCommerceSearchModuleCoreModelGeoPoint {
  /** @format double */
  latitude?: number;
  /** @format double */
  longitude?: number;
}

export interface VirtoCommerceSearchModuleCoreModelIndexDocument {
  fields?: VirtoCommerceSearchModuleCoreModelIndexDocumentField[] | null;
  id?: string | null;
}

export interface VirtoCommerceSearchModuleCoreModelIndexDocumentField {
  isCollection?: boolean;
  isFilterable?: boolean;
  isRetrievable?: boolean;
  isSearchable?: boolean;
  isSuggestable?: boolean;
  name?: string | null;
  value?: object | null;
  valueType?: VirtoCommerceSearchModuleCoreModelIndexDocumentFieldValueType;
  values?: object[] | null;
}

export type VirtoCommerceSearchModuleCoreModelIndexDocumentFieldValueType =
  | "Undefined"
  | "String"
  | "Char"
  | "Guid"
  | "Integer"
  | "Double"
  | "Short"
  | "Byte"
  | "Long"
  | "Float"
  | "Decimal"
  | "DateTime"
  | "Boolean"
  | "GeoPoint"
  | "Complex"
  | "DenseVector";

export interface VirtoCommerceSearchModuleCoreModelIndexFieldSetting {
  documentType?: string | null;
  fieldName?: string | null;
  id?: string | null;
  values?: VirtoCommerceSearchModuleCoreModelIndexFieldValueSetting[] | null;
}

export interface VirtoCommerceSearchModuleCoreModelIndexFieldSettingSearchCriteria {
  documentType?: string | null;
  fieldName?: string | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceSearchModuleCoreModelIndexFieldSettingSearchResult {
  results?: VirtoCommerceSearchModuleCoreModelIndexFieldSetting[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceSearchModuleCoreModelIndexFieldValueSetting {
  id?: string | null;
  synonyms?: string[] | null;
  value?: string | null;
}

export interface VirtoCommerceSearchModuleCoreModelIndexProgressPushNotification {
  /** @format date-time */
  created?: string;
  creator?: string | null;
  description?: string | null;
  documentType?: string | null;
  /** @format int64 */
  errorCount?: number;
  errors?: string[] | null;
  /** @format date-time */
  finished?: string | null;
  id?: string | null;
  isNew?: boolean;
  jobId?: string | null;
  notifyType?: string | null;
  /** @format int64 */
  processedCount?: number;
  /** @format int32 */
  repeatCount?: number;
  serverId?: string | null;
  title?: string | null;
  /** @format int64 */
  totalCount?: number;
}

export interface VirtoCommerceSearchModuleCoreModelIndexState {
  documentType?: string | null;
  /** @format int64 */
  indexedDocumentsCount?: number | null;
  isActive?: boolean;
  /** @format date-time */
  lastIndexationDate?: string | null;
  provider?: string | null;
  scope?: string | null;
}

export interface VirtoCommerceSearchModuleCoreModelIndexingOptions {
  /** @format int32 */
  batchSize?: number | null;
  deleteExistingIndex?: boolean;
  documentIds?: string[] | null;
  documentType?: string | null;
  /** @format date-time */
  endDate?: string | null;
  /** @format date-time */
  startDate?: string | null;
}

export interface VirtoCommerceSearchModuleCoreModelNumericRange {
  includeLower?: boolean;
  includeUpper?: boolean;
  /** @format double */
  lower?: number | null;
  /** @format double */
  upper?: number | null;
}

export interface VirtoCommerceSearchModuleCoreModelSuggestionResponse {
  suggestions?: string[] | null;
}

export interface VirtoCommerceSeoCoreModelsBrokenLink {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  /** @format int32 */
  hitCount?: number;
  id?: string | null;
  language?: string | null;
  /** @format date-time */
  lastHitDate?: string;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  permalink?: string | null;
  redirectUrl?: string | null;
  status?: string | null;
  storeId?: string | null;
}

export interface VirtoCommerceSeoCoreModelsBrokenLinkSearchCriteria {
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  permalink?: string | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  status?: string | null;
  storeId?: string | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceSeoCoreModelsBrokenLinkSearchResult {
  results?: VirtoCommerceSeoCoreModelsBrokenLink[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceSeoCoreModelsExplainSeoExplainItem {
  /** @format int32 */
  objectTypePriority?: number;
  /** @format int32 */
  score?: number;
  seoInfo?: VirtoCommerceSeoCoreModelsSeoInfo | null;
}

export interface VirtoCommerceSeoCoreModelsExplainSeoExplainResult {
  items?: VirtoCommerceSeoCoreModelsExplainSeoExplainItem[] | null;
  stage?: VirtoCommerceSeoCoreModelsExplainSeoExplainStage;
}

export type VirtoCommerceSeoCoreModelsExplainSeoExplainStage =
  | "Undefined"
  | "Original"
  | "Filtered"
  | "Scored"
  | "FilteredScore"
  | "Ordered"
  | "Final";

export interface VirtoCommerceSeoCoreModelsRedirectRule {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  inbound?: string | null;
  isActive?: boolean;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  outbound?: string | null;
  /** @format int32 */
  priority?: number;
  redirectRuleType?: string | null;
  storeId?: string | null;
}

export interface VirtoCommerceSeoCoreModelsRedirectRuleSearchCriteria {
  isActive?: boolean;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  storeId?: string | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceSeoCoreModelsRedirectRuleSearchResult {
  results?: VirtoCommerceSeoCoreModelsRedirectRule[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceSeoCoreModelsSeoInfo {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  imageAltDescription?: string | null;
  isActive?: boolean;
  languageCode?: string | null;
  metaDescription?: string | null;
  metaKeywords?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  objectId?: string | null;
  objectType?: string | null;
  organizationId?: string | null;
  outline?: string | null;
  pageTitle?: string | null;
  semanticUrl?: string | null;
  storeId?: string | null;
}

export interface VirtoCommerceSeoCoreModelsSeoSearchCriteria {
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  organizationId?: string | null;
  permalink?: string | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  slug?: string | null;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  storeId?: string | null;
  /** @format int32 */
  take?: number;
  userId?: string | null;
}

export interface VirtoCommerceShippingModuleCoreModelPickupLocation {
  address?: VirtoCommerceShippingModuleCoreModelPickupLocationAddress | null;
  contactEmail?: string | null;
  contactPhone?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  /** @format int32 */
  deliveryDays?: number | null;
  /**
   * @minLength 0
   * @maxLength 1024
   */
  description?: string | null;
  /**
   * @minLength 0
   * @maxLength 128
   */
  fulfillmentCenterId?: string | null;
  geoLocation?: string | null;
  id?: string | null;
  isActive?: boolean;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  outerId?: string | null;
  /** @format double */
  relevanceScore?: number | null;
  /** @format int32 */
  storageDays?: number | null;
  /**
   * @minLength 0
   * @maxLength 128
   */
  storeId?: string | null;
  transferFulfillmentCenterIds?: string[] | null;
  workingHours?: string | null;
}

export interface VirtoCommerceShippingModuleCoreModelPickupLocationAddress {
  line1?: string | null;
  line2?: string | null;
  addressType?: VirtoCommerceCoreModuleCoreCommonAddressType;
  city?: string | null;
  countryCode?: string | null;
  countryName?: string | null;
  description?: string | null;
  email?: string | null;
  firstName?: string | null;
  id?: string | null;
  isDefault?: boolean;
  key?: string | null;
  lastName?: string | null;
  middleName?: string | null;
  name?: string | null;
  organization?: string | null;
  outerId?: string | null;
  phone?: string | null;
  postalCode?: string | null;
  regionId?: string | null;
  regionName?: string | null;
  zip?: string | null;
}

export interface VirtoCommerceShippingModuleCoreModelSearchPickupLocationSearchCriteria {
  isActive?: boolean | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  storeId?: string | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceShippingModuleCoreModelSearchShippingMethodsSearchCriteria {
  codes?: string[] | null;
  isActive?: boolean | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  storeId?: string | null;
  /** @format int32 */
  take?: number;
  taxType?: string | null;
  withoutTransient?: boolean;
}

export interface VirtoCommerceShippingModuleCoreModelSearchShippingMethodsSearchResult {
  results?: VirtoCommerceShippingModuleCoreModelShippingMethod[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceShippingModuleCoreModelShippingMethod {
  code?: string | null;
  description?: string | null;
  id?: string | null;
  isActive?: boolean;
  logoUrl?: string | null;
  name?: string | null;
  /** @format int32 */
  priority?: number;
  settings?: VirtoCommercePlatformCoreSettingsObjectSettingEntry[] | null;
  storeId?: string | null;
  taxType?: string | null;
  readonly typeName?: string | null;
}

export interface VirtoCommerceShippingModuleCoreModelShippingRate {
  currency?: string | null;
  /** @format double */
  discountAmount?: number;
  /** @format double */
  discountAmountWithTax?: number;
  optionDescription?: string | null;
  optionName?: string | null;
  /** @format double */
  rate?: number;
  /** @format double */
  rateWithTax?: number;
  shippingMethod?: VirtoCommerceShippingModuleCoreModelShippingMethod | null;
}

export interface VirtoCommerceSitemapsModuleCoreModelsSearchSitemapItemSearchCriteria {
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  sitemapId?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceSitemapsModuleCoreModelsSearchSitemapItemsSearchResult {
  results?: VirtoCommerceSitemapsModuleCoreModelsSitemapItem[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceSitemapsModuleCoreModelsSearchSitemapSearchCriteria {
  keyword?: string | null;
  languageCode?: string | null;
  location?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  storeId?: string | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceSitemapsModuleCoreModelsSearchSitemapSearchResult {
  results?: VirtoCommerceSitemapsModuleCoreModelsSitemap[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceSitemapsModuleCoreModelsSitemap {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  items?: VirtoCommerceSitemapsModuleCoreModelsSitemapItem[] | null;
  location?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  sitemapMode?: VirtoCommerceSitemapsModuleCoreModelsSitemapContentMode;
  storeId?: string | null;
  /** @format int32 */
  totalItemsCount?: number;
  urlTemplate?: string | null;
}

export type VirtoCommerceSitemapsModuleCoreModelsSitemapContentMode =
  | "Full"
  | "OnlyProducts"
  | "OnlyCategories";

export interface VirtoCommerceSitemapsModuleCoreModelsSitemapItem {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  imageUrl?: string | null;
  itemsRecords?:
    | VirtoCommerceSitemapsModuleCoreModelsSitemapItemRecord[]
    | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  objectId?: string | null;
  objectType?: string | null;
  sitemapId?: string | null;
  title?: string | null;
  urlTemplate?: string | null;
}

export interface VirtoCommerceSitemapsModuleCoreModelsSitemapItemAlternateLinkRecord {
  language?: string | null;
  type?: string | null;
  url?: string | null;
}

export interface VirtoCommerceSitemapsModuleCoreModelsSitemapItemImageRecord {
  loc?: string | null;
}

export interface VirtoCommerceSitemapsModuleCoreModelsSitemapItemRecord {
  alternates?:
    | VirtoCommerceSitemapsModuleCoreModelsSitemapItemAlternateLinkRecord[]
    | null;
  images?: VirtoCommerceSitemapsModuleCoreModelsSitemapItemImageRecord[] | null;
  /** @format date-time */
  modifiedDate?: string;
  objectType?: string | null;
  /** @format double */
  priority?: number;
  updateFrequency?: string | null;
  url?: string | null;
}

export interface VirtoCommerceSitemapsModuleDataModelPushNotificationsSitemapDownloadNotification {
  /** @format date-time */
  created?: string;
  creator?: string | null;
  description?: string | null;
  downloadUrl?: string | null;
  /** @format int64 */
  readonly errorCount?: number;
  errors?: string[] | null;
  /** @format date-time */
  finished?: string | null;
  id?: string | null;
  isNew?: boolean;
  notifyType?: string | null;
  /** @format int64 */
  processedCount?: number;
  /** @format int32 */
  repeatCount?: number;
  serverId?: string | null;
  title?: string | null;
  /** @format int64 */
  totalCount?: number;
}

export interface VirtoCommerceStoreModuleCoreModelModulePublicStoreSettings {
  moduleId?: string | null;
  settings?: VirtoCommerceStoreModuleCoreModelPublicStoreSetting[] | null;
}

export interface VirtoCommerceStoreModuleCoreModelPublicStoreSetting {
  name?: string | null;
  value?: object | null;
}

export interface VirtoCommerceStoreModuleCoreModelSearchStoreSearchCriteria {
  domain?: string | null;
  fulfillmentCenterIds?: string[] | null;
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  storeStates?: VirtoCommerceStoreModuleCoreModelStoreState[] | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceStoreModuleCoreModelSearchStoreSearchResult {
  results?: VirtoCommerceStoreModuleCoreModelStore[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceStoreModuleCoreModelStore {
  /** Alternate fulfillment centers ids */
  additionalFulfillmentCenterIds?: string[] | null;
  adminEmail?: string | null;
  adminEmailName?: string | null;
  /**
   * Base URL used to build public asset (image) URLs for this store in the Experience API responses.
   * Overrides the global Assets PublicUrl. When empty, the global/admin default is used.
   */
  assetPublicUrl?: string | null;
  /** Catalog id used as primary store catalog */
  catalog?: string | null;
  country?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  creditCardSavePolicy?: boolean;
  /** All store supported currencies */
  currencies?: string[] | null;
  defaultCurrency?: string | null;
  defaultLanguage?: string | null;
  description?: string | null;
  displayOutOfStock?: boolean;
  dynamicProperties?:
    | VirtoCommercePlatformCoreDynamicPropertiesDynamicObjectProperty[]
    | null;
  /** Primary store contact email can be used for store event notifications and for feed back */
  email?: string | null;
  emailName?: string | null;
  id?: string | null;
  /** All store supported languages */
  languages?: string[] | null;
  /** Primary (default) fulfillment center id */
  mainFulfillmentCenterId?: string | null;
  /** Primary (default) fulfillment center for order return */
  mainReturnsFulfillmentCenterId?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  readonly objectType?: string | null;
  outerId?: string | null;
  region?: string | null;
  /** Alternate fulfillment centers for order return */
  returnsFulfillmentCenterIds?: string[] | null;
  scopes?: string[] | null;
  /** Store storefront https url */
  secureUrl?: string | null;
  seoInfos?: VirtoCommerceSeoCoreModelsSeoInfo[] | null;
  readonly seoObjectType?: string | null;
  settings?: VirtoCommercePlatformCoreSettingsObjectSettingEntry[] | null;
  /** Store current state (Open, Closed, RestrictedAccess) */
  storeState?: VirtoCommerceStoreModuleCoreModelStoreState;
  timeZone?: string | null;
  /** All store trusted groups (group of stores that shared the user logins) */
  trustedGroups?: string[] | null;
  readonly typeName?: string | null;
  /** Store storefront url */
  url?: string | null;
}

export interface VirtoCommerceStoreModuleCoreModelStoreAuthenticationScheme {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  displayName?: string | null;
  id?: string | null;
  isActive?: boolean;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  name?: string | null;
  /** @format int32 */
  position?: number;
  storeId?: string | null;
}

export type VirtoCommerceStoreModuleCoreModelStoreState =
  | "Open"
  | "Closed"
  | "RestrictedAccess";

/** Represent result for checking of possibility login on behalf request */
export interface VirtoCommerceStoreModuleWebModelLoginOnBehalfInfo {
  canLoginOnBehalf?: boolean;
  userName?: string | null;
}

export interface VirtoCommerceStoreModuleWebModelSendDynamicNotificationRequest {
  fields?: Record<string, string | null>;
  language?: string | null;
  storeId?: string | null;
  type?: string | null;
}

export type VirtoCommerceSubscriptionModuleCoreModelPaymentInterval =
  | "Days"
  | "Weeks"
  | "Months"
  | "Years";

export interface VirtoCommerceSubscriptionModuleCoreModelPaymentPlan {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  id?: string | null;
  /** (days, months, years) - billing interval */
  interval?: VirtoCommerceSubscriptionModuleCoreModelPaymentInterval;
  /**
   * - to set more customized intervals (every 5 month)
   * @format int32
   */
  intervalCount?: number;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  /**
   * subscription trial period in days
   * @format int32
   */
  trialPeriodDays?: number;
}

export interface VirtoCommerceSubscriptionModuleCoreModelSearchSubscriptionSearchCriteria {
  customerId?: string | null;
  /** Search subscription for related order id */
  customerOrderId?: string | null;
  /** @format date-time */
  endDate?: string | null;
  keyword?: string | null;
  languageCode?: string | null;
  /** @format date-time */
  modifiedSinceDate?: string | null;
  /** Search by subscription number */
  number?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  /** Search by external subscription system id */
  outerId?: string | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  /**
   * Search subscription in StartDate and EndDate range inclusive
   * @format date-time
   */
  startDate?: string | null;
  /** Search with specified statuses */
  statuses?: string[] | null;
  /** Search within specified store */
  storeId?: string | null;
  /** @format int32 */
  take?: number;
}

export interface VirtoCommerceSubscriptionModuleCoreModelSearchSubscriptionSearchResult {
  results?: VirtoCommerceSubscriptionModuleCoreModelSubscription[] | null;
  readonly subscriptions?:
    | VirtoCommerceSubscriptionModuleCoreModelSubscription[]
    | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceSubscriptionModuleCoreModelSubscription {
  /**
   * Subscription actual balance
   * @format double
   */
  balance?: number;
  cancelReason?: string | null;
  /** @format date-time */
  cancelledDate?: string | null;
  /** The subscription comment */
  comment?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  /** @format date-time */
  currentPeriodEnd?: string | null;
  /** @format date-time */
  currentPeriodStart?: string | null;
  customerId?: string | null;
  customerName?: string | null;
  /** Order prototype for future orders. Changing this prototype can affect for future orders of this subscription */
  customerOrderPrototype?: VirtoCommerceOrdersModuleCoreModelCustomerOrder | null;
  customerOrderPrototypeId?: string | null;
  /** List of all orders  created on the basis of the subscription */
  customerOrders?: VirtoCommerceOrdersModuleCoreModelCustomerOrder[] | null;
  /** List of all orders ids created on the basis of the subscription */
  customerOrdersIds?: string[] | null;
  /**
   * The date the subscription ended
   * @format date-time
   */
  endDate?: string | null;
  id?: string | null;
  /** (days, months, years) - billing interval */
  interval?: VirtoCommerceSubscriptionModuleCoreModelPaymentInterval;
  /**
   * - to set more customized intervals (every 5 month)
   * @format int32
   */
  intervalCount?: number;
  isCancelled?: boolean;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  /** Subscription number */
  number?: string | null;
  operationsLog?: VirtoCommercePlatformCoreChangeLogOperationLog[] | null;
  /** External Subscription entity system ID */
  outerId?: string | null;
  /**
   * Date the most recent update to this subscription started.
   * @format date-time
   */
  startDate?: string | null;
  storeId?: string | null;
  subscriptionStatus?: VirtoCommerceSubscriptionModuleCoreModelSubscriptionStatus;
  /** @format date-time */
  trialEnd?: string | null;
  /**
   * subscription trial period in days
   * @format int32
   */
  trialPeriodDays?: number;
  /** @format date-time */
  trialStart?: string | null;
}

export type VirtoCommerceSubscriptionModuleCoreModelSubscriptionStatus =
  | "Active"
  | "Trialing"
  | "PastDue"
  | "Cancelled"
  | "Unpaid";

export interface VirtoCommerceSubscriptionModuleWebModelSubscriptionCancelRequest {
  cancelReason?: string | null;
  subscriptionId?: string | null;
}

export interface VirtoCommerceTaxModuleCoreModelSearchTaxProviderSearchCriteria {
  keyword?: string | null;
  languageCode?: string | null;
  objectIds?: string[] | null;
  objectType?: string | null;
  objectTypes?: string[] | null;
  responseGroup?: string | null;
  searchPhrase?: string | null;
  /** @format int32 */
  skip?: number;
  sort?: string | null;
  readonly sortInfos?: VirtoCommercePlatformCoreCommonSortInfo[] | null;
  storeIds?: string[] | null;
  /** @format int32 */
  take?: number;
  withoutTransient?: boolean;
}

export interface VirtoCommerceTaxModuleCoreModelSearchTaxProviderSearchResult {
  results?: VirtoCommerceTaxModuleCoreModelTaxProvider[] | null;
  /** @format int32 */
  totalCount?: number;
}

export interface VirtoCommerceTaxModuleCoreModelTaxEvaluationContext {
  address?: TaxAddress | null;
  code?: string | null;
  currency?: string | null;
  customer?: TaxCustomer | null;
  customerId?: string | null;
  id?: string | null;
  lines?: VirtoCommerceTaxModuleCoreModelTaxLine[] | null;
  organizationId?: string | null;
  store?: TaxStore | null;
  storeId?: string | null;
  type?: string | null;
}

export interface VirtoCommerceTaxModuleCoreModelTaxLine {
  /** @format double */
  amount?: number;
  code?: string | null;
  id?: string | null;
  name?: string | null;
  /** @format double */
  price?: number;
  /** @format int32 */
  quantity?: number;
  taxType?: string | null;
  typeName?: string | null;
}

export interface VirtoCommerceTaxModuleCoreModelTaxProvider {
  code?: string | null;
  id?: string | null;
  isActive?: boolean;
  logoUrl?: string | null;
  /** @format int32 */
  priority?: number;
  settings?: VirtoCommercePlatformCoreSettingsObjectSettingEntry[] | null;
  storeId?: string | null;
  readonly typeName?: string | null;
}

export interface VirtoCommerceTaxModuleCoreModelTaxRate {
  currency?: string | null;
  line?: VirtoCommerceTaxModuleCoreModelTaxLine | null;
  /** @format double */
  percentRate?: number;
  /** @format double */
  rate?: number;
  taxDetails?: VirtoCommerceCoreModuleCoreTaxTaxDetail[] | null;
  taxProviderCode?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpCapabilityVersion {
  version?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpCart {
  addresses?: VirtoCommerceUCPCoreModelsUcpCartAddress[] | null;
  buyer_id?: string | null;
  cart_name?: string | null;
  cart_type?: string | null;
  continue_url?: string | null;
  coupons?: VirtoCommerceUCPCoreModelsUcpCartCoupon[] | null;
  currency?: string | null;
  id?: string | null;
  line_items?: VirtoCommerceUCPCoreModelsUcpCartLineItem[] | null;
  messages?: VirtoCommerceUCPCoreModelsUcpMessage[] | null;
  organization_id?: string | null;
  payments?: VirtoCommerceUCPCoreModelsUcpCartPayment[] | null;
  shipments?: VirtoCommerceUCPCoreModelsUcpCartShipment[] | null;
  status?: string | null;
  store_id?: string | null;
  totals?: VirtoCommerceUCPCoreModelsUcpCartTotals | null;
}

export interface VirtoCommerceUCPCoreModelsUcpCartAddress {
  line1?: string | null;
  line2?: string | null;
  address_type?: string | null;
  city?: string | null;
  country_code?: string | null;
  country_name?: string | null;
  email?: string | null;
  first_name?: string | null;
  id?: string | null;
  last_name?: string | null;
  name?: string | null;
  organization?: string | null;
  phone?: string | null;
  postal_code?: string | null;
  region?: string | null;
  region_id?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpCartContext {
  address_country?: string | null;
  address_region?: string | null;
  buyer_id?: string | null;
  cart_name?: string | null;
  cart_type?: string | null;
  currency?: string | null;
  intent?: string | null;
  language?: string | null;
  organization_id?: string | null;
  store_id?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpCartCoupon {
  applied?: boolean;
  code?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpCartLineItem {
  discount_total?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  id?: string | null;
  image_url?: string | null;
  line_total?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  list_price?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  messages?: VirtoCommerceUCPCoreModelsUcpMessage[] | null;
  name?: string | null;
  product_id?: string | null;
  /** @format int32 */
  quantity?: number;
  sku?: string | null;
  tax_total?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  unit_price?: VirtoCommerceUCPCoreModelsUcpMoney | null;
}

export interface VirtoCommerceUCPCoreModelsUcpCartLineItemRequest {
  id?: string | null;
  product_id?: string | null;
  /** @format int32 */
  quantity?: number;
}

export interface VirtoCommerceUCPCoreModelsUcpCartListResponse {
  carts?: VirtoCommerceUCPCoreModelsUcpCart[] | null;
  messages?: VirtoCommerceUCPCoreModelsUcpMessage[] | null;
  pagination?: VirtoCommerceUCPCoreModelsUcpPaginationResponse | null;
  ucp?: VirtoCommerceUCPCoreModelsUcpResponseMetadata | null;
}

export interface VirtoCommerceUCPCoreModelsUcpCartPayment {
  amount?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  billing_address?: VirtoCommerceUCPCoreModelsUcpCartAddress | null;
  id?: string | null;
  payment_gateway_code?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpCartRequest {
  buyer_id?: string | null;
  cart_name?: string | null;
  cart_type?: string | null;
  context?: VirtoCommerceUCPCoreModelsUcpCartContext | null;
  coupons?: string[] | null;
  currency?: string | null;
  language?: string | null;
  line_items?: VirtoCommerceUCPCoreModelsUcpCartLineItemRequest[] | null;
  organization_id?: string | null;
  store_id?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpCartResponse {
  cart?: VirtoCommerceUCPCoreModelsUcpCart | null;
  messages?: VirtoCommerceUCPCoreModelsUcpMessage[] | null;
  ucp?: VirtoCommerceUCPCoreModelsUcpResponseMetadata | null;
}

export interface VirtoCommerceUCPCoreModelsUcpCartShipment {
  delivery_address?: VirtoCommerceUCPCoreModelsUcpCartAddress | null;
  id?: string | null;
  price?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  shipment_method_code?: string | null;
  shipment_method_option?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpCartTotals {
  discount_total?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  fee_total?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  payment_total?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  shipping_total?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  subtotal?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  tax_total?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  total?: VirtoCommerceUCPCoreModelsUcpMoney | null;
}

export interface VirtoCommerceUCPCoreModelsUcpCatalogContext {
  address_country?: string | null;
  address_region?: string | null;
  currency?: string | null;
  intent?: string | null;
  language?: string | null;
  store_id?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpCatalogSearchRequest {
  context?: VirtoCommerceUCPCoreModelsUcpCatalogContext | null;
  currency?: string | null;
  filters?: VirtoCommerceUCPCoreModelsUcpSearchFilters | null;
  language?: string | null;
  /** @format int32 */
  limit?: number | null;
  pagination?: VirtoCommerceUCPCoreModelsUcpPaginationRequest | null;
  query?: string | null;
  store_id?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpCatalogSearchResponse {
  messages?: VirtoCommerceUCPCoreModelsUcpMessage[] | null;
  pagination?: VirtoCommerceUCPCoreModelsUcpPaginationResponse | null;
  products?: VirtoCommerceUCPCoreModelsUcpProduct[] | null;
  ucp?: VirtoCommerceUCPCoreModelsUcpResponseMetadata | null;
}

export interface VirtoCommerceUCPCoreModelsUcpCheckout {
  billing_address?: VirtoCommerceUCPCoreModelsUcpCheckoutAddress | null;
  buyer?: VirtoCommerceUCPCoreModelsUcpCheckoutBuyer | null;
  cart?: VirtoCommerceUCPCoreModelsUcpCart | null;
  cart_id?: string | null;
  continue_url?: string | null;
  /** @format date-time */
  expires_at?: string | null;
  id?: string | null;
  messages?: VirtoCommerceUCPCoreModelsUcpMessage[] | null;
  payment_handler?: string | null;
  payment_handlers?:
    | VirtoCommerceUCPCoreModelsUcpPaymentHandlerProfile[]
    | null;
  shipping_address?: VirtoCommerceUCPCoreModelsUcpCheckoutAddress | null;
  shipping_method_id?: string | null;
  status?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpCheckoutAddress {
  line1?: string | null;
  line2?: string | null;
  city?: string | null;
  country_code?: string | null;
  country_name?: string | null;
  email?: string | null;
  first_name?: string | null;
  id?: string | null;
  last_name?: string | null;
  name?: string | null;
  organization?: string | null;
  phone?: string | null;
  postal_code?: string | null;
  region?: string | null;
  region_id?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpCheckoutBuyer {
  email?: string | null;
  id?: string | null;
  name?: string | null;
  phone?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpCheckoutHandoffResponse {
  checkout?: VirtoCommerceUCPCoreModelsUcpCheckout | null;
  messages?: VirtoCommerceUCPCoreModelsUcpMessage[] | null;
  ucp?: VirtoCommerceUCPCoreModelsUcpResponseMetadata | null;
}

export interface VirtoCommerceUCPCoreModelsUcpCheckoutRequest {
  billing_address?: VirtoCommerceUCPCoreModelsUcpCheckoutAddress | null;
  buyer?: VirtoCommerceUCPCoreModelsUcpCheckoutBuyer | null;
  buyer_id?: string | null;
  cart_id?: string | null;
  context?: VirtoCommerceUCPCoreModelsUcpCartContext | null;
  currency?: string | null;
  language?: string | null;
  notes?: string | null;
  organization_id?: string | null;
  payment_handler?: string | null;
  shipping_address?: VirtoCommerceUCPCoreModelsUcpCheckoutAddress | null;
  shipping_method_id?: string | null;
  store_id?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpCheckoutResponse {
  checkout?: VirtoCommerceUCPCoreModelsUcpCheckout | null;
  messages?: VirtoCommerceUCPCoreModelsUcpMessage[] | null;
  ucp?: VirtoCommerceUCPCoreModelsUcpResponseMetadata | null;
}

export interface VirtoCommerceUCPCoreModelsUcpCountriesResponse {
  countries?: VirtoCommerceUCPCoreModelsUcpCountry[] | null;
  ucp?: VirtoCommerceUCPCoreModelsUcpResponseMetadata | null;
}

export interface VirtoCommerceUCPCoreModelsUcpCountry {
  id?: string | null;
  name?: string | null;
  /** @format int32 */
  region_count?: number;
}

export interface VirtoCommerceUCPCoreModelsUcpCountryResponse {
  country?: VirtoCommerceUCPCoreModelsUcpCountry | null;
  ucp?: VirtoCommerceUCPCoreModelsUcpResponseMetadata | null;
}

export interface VirtoCommerceUCPCoreModelsUcpDiscoveryDocument {
  ucp?: VirtoCommerceUCPCoreModelsUcpDiscoveryProfile | null;
}

export interface VirtoCommerceUCPCoreModelsUcpDiscoveryProfile {
  capabilities?: Record<
    string,
    VirtoCommerceUCPCoreModelsUcpCapabilityVersion[] | null
  >;
  payment_handlers?: Record<
    string,
    VirtoCommerceUCPCoreModelsUcpPaymentHandlerProfile[] | null
  >;
  services?: Record<
    string,
    VirtoCommerceUCPCoreModelsUcpDiscoveryServiceProfile[] | null
  >;
  status?: string | null;
  version?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpDiscoveryServiceProfile {
  endpoint?: string | null;
  transport?: string | null;
  version?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpError {
  code?: string | null;
  correlation_id?: string | null;
  details?: Record<string, object | null>;
  message?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpHandoffRestoreRequest {
  ucp_session?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpHandoffRestoreResponse {
  anonymous_buyer_id?: string | null;
  checkout?: VirtoCommerceUCPCoreModelsUcpCheckout | null;
  ucp?: VirtoCommerceUCPCoreModelsUcpResponseMetadata | null;
}

export interface VirtoCommerceUCPCoreModelsUcpMessage {
  code?: string | null;
  content?: string | null;
  severity?: string | null;
  type?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpMoney {
  /** @format int64 */
  amount?: number;
  currency?: string | null;
  formatted_amount?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpOrder {
  buyer_id?: string | null;
  cart_id?: string | null;
  created_at?: string | null;
  currency?: string | null;
  customer_name?: string | null;
  id?: string | null;
  line_items?: VirtoCommerceUCPCoreModelsUcpOrderLineItem[] | null;
  messages?: VirtoCommerceUCPCoreModelsUcpMessage[] | null;
  number?: string | null;
  payments?: VirtoCommerceUCPCoreModelsUcpOrderPayment[] | null;
  shipments?: VirtoCommerceUCPCoreModelsUcpOrderShipment[] | null;
  status?: string | null;
  status_display_value?: string | null;
  store_id?: string | null;
  totals?: VirtoCommerceUCPCoreModelsUcpOrderTotals | null;
}

export interface VirtoCommerceUCPCoreModelsUcpOrderAddress {
  line1?: string | null;
  line2?: string | null;
  city?: string | null;
  country_code?: string | null;
  country_name?: string | null;
  email?: string | null;
  first_name?: string | null;
  id?: string | null;
  last_name?: string | null;
  name?: string | null;
  organization?: string | null;
  phone?: string | null;
  postal_code?: string | null;
  region?: string | null;
  region_id?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpOrderLineItem {
  discount_total?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  id?: string | null;
  image_url?: string | null;
  line_total?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  name?: string | null;
  placed_price?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  product_id?: string | null;
  /** @format int32 */
  quantity?: number;
  sku?: string | null;
  status?: string | null;
  tax_total?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  unit_price?: VirtoCommerceUCPCoreModelsUcpMoney | null;
}

export interface VirtoCommerceUCPCoreModelsUcpOrderPayment {
  approved?: boolean;
  billing_address?: VirtoCommerceUCPCoreModelsUcpOrderAddress | null;
  gateway_code?: string | null;
  id?: string | null;
  method_code?: string | null;
  method_name?: string | null;
  number?: string | null;
  status?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpOrderResponse {
  messages?: VirtoCommerceUCPCoreModelsUcpMessage[] | null;
  order?: VirtoCommerceUCPCoreModelsUcpOrder | null;
  ucp?: VirtoCommerceUCPCoreModelsUcpResponseMetadata | null;
}

export interface VirtoCommerceUCPCoreModelsUcpOrderShipment {
  approved?: boolean;
  delivery_address?: VirtoCommerceUCPCoreModelsUcpOrderAddress | null;
  delivery_at?: string | null;
  discount_amount?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  id?: string | null;
  number?: string | null;
  price?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  shipment_method_code?: string | null;
  shipment_method_option?: string | null;
  status?: string | null;
  tracking_number?: string | null;
  tracking_url?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpOrderTotals {
  discount_total?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  shipping_subtotal?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  shipping_total?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  subtotal?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  tax_total?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  total?: VirtoCommerceUCPCoreModelsUcpMoney | null;
}

export interface VirtoCommerceUCPCoreModelsUcpPaginationRequest {
  cursor?: string | null;
  /** @format int32 */
  limit?: number | null;
}

export interface VirtoCommerceUCPCoreModelsUcpPaginationResponse {
  cursor?: string | null;
  has_next_page?: boolean;
  /** @format int32 */
  total_count?: number;
}

export interface VirtoCommerceUCPCoreModelsUcpPaymentHandlerProfile {
  available?: boolean;
  capability?: string | null;
  code?: string | null;
  reason?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpPaymentHandlersResponse {
  checkout_id?: string | null;
  payment_handlers?:
    | VirtoCommerceUCPCoreModelsUcpPaymentHandlerProfile[]
    | null;
  ucp?: VirtoCommerceUCPCoreModelsUcpResponseMetadata | null;
}

export interface VirtoCommerceUCPCoreModelsUcpPriceFilter {
  /** @format int64 */
  max?: number | null;
  /** @format int64 */
  min?: number | null;
}

export interface VirtoCommerceUCPCoreModelsUcpProduct {
  attributes?: VirtoCommerceUCPCoreModelsUcpProductAttribute[] | null;
  availability?: VirtoCommerceUCPCoreModelsUcpProductAvailability | null;
  brand?: string | null;
  code?: string | null;
  id?: string | null;
  image_url?: string | null;
  list_price?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  name?: string | null;
  price?: VirtoCommerceUCPCoreModelsUcpMoney | null;
  product_type?: string | null;
  slug?: string | null;
  variations?: VirtoCommerceUCPCoreModelsUcpProductVariation[] | null;
}

export interface VirtoCommerceUCPCoreModelsUcpProductAttribute {
  name?: string | null;
  value?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpProductAvailability {
  /** @format double */
  available_quantity?: number;
  is_available?: boolean;
  is_buyable?: boolean;
  is_in_stock?: boolean;
}

export interface VirtoCommerceUCPCoreModelsUcpProductResponse {
  messages?: VirtoCommerceUCPCoreModelsUcpMessage[] | null;
  product?: VirtoCommerceUCPCoreModelsUcpProduct | null;
  ucp?: VirtoCommerceUCPCoreModelsUcpResponseMetadata | null;
}

export interface VirtoCommerceUCPCoreModelsUcpProductVariation {
  attributes?: VirtoCommerceUCPCoreModelsUcpProductAttribute[] | null;
  availability?: VirtoCommerceUCPCoreModelsUcpProductAvailability | null;
  code?: string | null;
  id?: string | null;
  name?: string | null;
  price?: VirtoCommerceUCPCoreModelsUcpMoney | null;
}

export interface VirtoCommerceUCPCoreModelsUcpRegion {
  id?: string | null;
  name?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpRegionsResponse {
  country?: VirtoCommerceUCPCoreModelsUcpCountry | null;
  regions?: VirtoCommerceUCPCoreModelsUcpRegion[] | null;
  ucp?: VirtoCommerceUCPCoreModelsUcpResponseMetadata | null;
}

export interface VirtoCommerceUCPCoreModelsUcpResponseMetadata {
  capabilities?: Record<
    string,
    VirtoCommerceUCPCoreModelsUcpCapabilityVersion[] | null
  >;
  correlation_id?: string | null;
  status?: string | null;
  version?: string | null;
}

export interface VirtoCommerceUCPCoreModelsUcpSearchFilters {
  categories?: string[] | null;
  price?: VirtoCommerceUCPCoreModelsUcpPriceFilter | null;
}

export interface VirtoCommerceUCPWebModelsUcpProtectedResourceMetadata {
  authorization_servers?: string[] | null;
  bearer_methods_supported?: string[] | null;
  resource?: string | null;
  resource_name?: string | null;
  scopes_supported?: string[] | null;
}

export interface VirtoCommerceWhiteLabelingCoreModelsWhiteLabelingSetting {
  /**
   * @minLength 0
   * @maxLength 64
   */
  createdBy?: string | null;
  /** @format date-time */
  createdDate?: string;
  faviconUrl?: string | null;
  footerLinkListName?: string | null;
  id?: string | null;
  isEnabled?: boolean;
  logoUrl?: string | null;
  mainMenuLinkListName?: string | null;
  /**
   * @minLength 0
   * @maxLength 64
   */
  modifiedBy?: string | null;
  /** @format date-time */
  modifiedDate?: string | null;
  organizationId?: string | null;
  secondaryLogoUrl?: string | null;
  storeId?: string | null;
  themePresetName?: string | null;
  userId?: string | null;
}
