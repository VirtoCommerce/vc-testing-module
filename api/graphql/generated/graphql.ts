/* eslint-disable */
/** Internal type. DO NOT USE DIRECTLY. */
type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
/** Internal type. DO NOT USE DIRECTLY. */
export type Incremental<T> = T | { [P in keyof T]?: P extends " $fragmentName" | "__typename" ? T[P] : never };

import type { DocumentTypeDecoration } from "@graphql-typed-document-node/core";
export type AddAddressToFavoritesCommandType = {
  addressId: string;
};

export type CancelQuoteCommandType = {
  comment: string;
  quoteId: string;
};

export type ChangeQuoteCommentCommandType = {
  comment: string;
  quoteId: string;
};

export type ChangeQuoteItemQuantityCommandType = {
  lineItemId: string;
  quantity: number;
  quoteId: string;
};

export type ConfigurableProductOptionInput = {
  /** Product ID */
  productId: string;
  /** Quantity of product */
  quantity: number;
  /** Whether the configuration item is selected for checkout */
  selectedForCheckout?: boolean | null | undefined;
};

export type ConfigurationSectionInput = {
  /** Custom text for 'Text' section */
  customText?: string | null | undefined;
  /** List of file links for 'File' section */
  fileUrls?: Array<string | null | undefined> | null | undefined;
  /** Configuration section option/product */
  option?: ConfigurableProductOptionInput | null | undefined;
  /** Configuration section ID */
  sectionId: string;
  /** Configuration section type. Possible values: 'Product', 'Variation', 'Text', 'File' */
  type: string;
};

export type CreateQuoteCommandType = {
  cultureName: string;
  currencyCode: string;
  storeId: string;
  userId: string;
};

export type CreateQuoteFromCartCommandType = {
  cartId: string;
  comment: string;
};

export type InputAddBulkItemsType = {
  cartId?: string | null | undefined;
  /** Bulk cart items */
  cartItems: Array<InputNewBulkItemType | null | undefined>;
  cartName?: string | null | undefined;
  cartType?: string | null | undefined;
  cultureName?: string | null | undefined;
  currencyCode?: string | null | undefined;
  storeId: string;
  userId: string;
};

export type InputAddCouponType = {
  cartId?: string | null | undefined;
  cartName?: string | null | undefined;
  cartType?: string | null | undefined;
  /** Coupon code */
  couponCode: string;
  cultureName?: string | null | undefined;
  currencyCode?: string | null | undefined;
  storeId: string;
  userId: string;
};

export type InputAddItemType = {
  cartId?: string | null | undefined;
  cartName?: string | null | undefined;
  cartType?: string | null | undefined;
  /** Comment */
  comment?: string | null | undefined;
  /** Configurable product support. List of configurable product sections */
  configurationSections?: Array<ConfigurationSectionInput | null | undefined> | null | undefined;
  /** Create date. Optional, to manually control line item position in the cart if required. ISO-8601 format, for example: 2025-01-23T11:46:11Z */
  createdDate?: string | null | undefined;
  cultureName?: string | null | undefined;
  currencyCode?: string | null | undefined;
  dynamicProperties?: Array<InputDynamicPropertyValueType | null | undefined> | null | undefined;
  /** Add the product in a different currency */
  itemCurrencyCode?: string | null | undefined;
  /** Price */
  price?: number | null | undefined;
  /** Product ID */
  productId: string;
  /** Quantity */
  quantity: number;
  storeId: string;
  userId: string;
};

export type InputAddItemsType = {
  cartId?: string | null | undefined;
  /** Cart items */
  cartItems: Array<InputNewCartItemType | null | undefined>;
  cartName?: string | null | undefined;
  cartType?: string | null | undefined;
  cultureName?: string | null | undefined;
  currencyCode?: string | null | undefined;
  storeId: string;
  userId: string;
};

export type InputAddOrUpdateCartPaymentType = {
  cartId?: string | null | undefined;
  cartName?: string | null | undefined;
  cartType?: string | null | undefined;
  cultureName?: string | null | undefined;
  currencyCode?: string | null | undefined;
  /** Payment */
  payment: InputPaymentType;
  storeId: string;
  userId: string;
};

export type InputAddOrUpdateCartShipmentType = {
  cartId?: string | null | undefined;
  cartName?: string | null | undefined;
  cartType?: string | null | undefined;
  cultureName?: string | null | undefined;
  currencyCode?: string | null | undefined;
  /** Shipment */
  shipment: InputShipmentType;
  storeId: string;
  userId: string;
};

export type InputAddWishlistBulkItemType = {
  /** Configurable product support. List of configurable product sections */
  configurationSections?: Array<ConfigurationSectionInput | null | undefined> | null | undefined;
  /** Wish list ids */
  listIds: Array<string | null | undefined>;
  /** Product id to add */
  productId: string;
  /** Product quantity to add */
  quantity?: number | null | undefined;
};

export type InputAddWishlistItemsType = {
  listId: string;
  /** List items */
  listItems: Array<InputNewWishlistItemType>;
};

export type InputAddressType = {
  addressType?: number | null | undefined;
  /** City */
  city?: string | null | null | undefined;
  /** Country code */
  countryCode?: string | null | null | undefined;
  /** Country */
  countryName?: string | null | null | undefined;
  /** Description */
  description?: string | null | null | undefined;
  /** Email */
  email?: string | null | null | undefined;
  /** First name */
  firstName?: string | null | null | undefined;
  /** ID */
  id?: string | null | null | undefined;
  /** ID */
  key?: string | null | null | undefined;
  /** Last name */
  lastName?: string | null | null | undefined;
  /** Line1 */
  line1?: string | null | null | undefined;
  /** Line2 */
  line2?: string | null | null | undefined;
  /** Middle name */
  middleName?: string | null | null | undefined;
  /** Name */
  name?: string | null | null | undefined;
  /** Company name */
  organization?: string | null | null | undefined;
  /** Outer ID */
  outerId?: string | null | null | undefined;
  /** Phone */
  phone?: string | null | null | undefined;
  /** Postal code */
  postalCode?: string | null | null | undefined;
  /** Region ID */
  regionId?: string | null | null | undefined;
  /** Region */
  regionName?: string | null | null | undefined;
  /** Zip */
  zip?: string | null | null | undefined;
};

export type InputChangeAllCartItemsSelectedType = {
  cartId?: string | null | undefined;
  cartName?: string | null | undefined;
  cartType?: string | null | undefined;
  cultureName?: string | null | undefined;
  currencyCode?: string | null | undefined;
  storeId: string;
  userId: string;
};

export type InputChangeCartConfiguredItemType = {
  cartId?: string | null | undefined;
  cartName?: string | null | undefined;
  cartType?: string | null | undefined;
  /** Configuration sections */
  configurationSections?: Array<ConfigurationSectionInput | null | undefined> | null | undefined;
  cultureName?: string | null | undefined;
  currencyCode?: string | null | undefined;
  /** Line item Id */
  lineItemId: string;
  /** Quantity */
  quantity?: number | null | undefined;
  storeId: string;
  userId: string;
};

export type InputChangeCartItemsSelectedType = {
  cartId?: string | null | undefined;
  cartName?: string | null | undefined;
  cartType?: string | null | undefined;
  cultureName?: string | null | undefined;
  currencyCode?: string | null | undefined;
  /** List of line item Ids */
  lineItemIds?: Array<string | null | undefined> | null | undefined;
  storeId: string;
  userId: string;
};

export type InputChangeOrganizationContactRoleType = {
  /** Contact member ID to be changed */
  memberId: string;
  /** Role IDs or names to be assigned to the user within the organization */
  roleIds?: Array<string> | null | undefined;
  /** ID of store whose company-role whitelist should be used for validation. When omitted, the member's own store is used */
  storeId?: string | null | undefined;
};

export type InputChangeWishlistType = {
  /** Culture name */
  cultureName?: string | null | undefined;
  /** List description */
  description?: string | null | undefined;
  /** List ID */
  listId: string;
  /** New List name */
  listName?: string | null | undefined;
  /** List scope (private or organization) */
  scope?: string | null | undefined;
  /** Id of the principal the list is shared with (id space defined by scope) */
  sharedWithId?: string | null | undefined;
  /** Sharing key (URL argument) */
  sharingKey?: string | null | undefined;
};

export type InputClearCartType = {
  cartId?: string | null | undefined;
  cartName?: string | null | undefined;
  cartType?: string | null | undefined;
  cultureName?: string | null | undefined;
  currencyCode?: string | null | undefined;
  storeId: string;
  userId: string;
};

export type InputCreateConfiguredLineItemCommand = {
  configurableProductId: string;
  configurationSections?: Array<ConfigurationSectionInput | null | undefined> | null | undefined;
  cultureName?: string | null | undefined;
  currencyCode?: string | null | undefined;
  storeId?: string | null | undefined;
};

export type InputCreateOrderFromCartType = {
  /** Cart ID */
  cartId?: string | null | undefined;
};

export type InputCreateWishlistType = {
  /** Culture name */
  cultureName?: string | null | undefined;
  /** Currency code */
  currencyCode?: string | null | undefined;
  /** List description */
  description?: string | null | undefined;
  /** List name */
  listName?: string | null | undefined;
  /** List scope (private or organization) */
  scope?: string | null | undefined;
  /** Id of the principal the list is shared with (id space defined by scope) */
  sharedWithId?: string | null | undefined;
  /** Sharing key (URL argument) */
  sharingKey?: string | null | undefined;
  /** Store ID */
  storeId: string;
  /** Owner ID */
  userId: string;
};

export type InputDeleteContactType = {
  contactId: string;
};

export type InputDeleteMemberAddressType = {
  addresses: Array<InputMemberAddressType | null | undefined>;
  memberId: string;
};

export type InputDeleteUserType = {
  userNames: Array<string | null | undefined>;
};

export type InputDynamicPropertyValueType = {
  /** Culture name ("en-US") for multilingual property */
  cultureName?: string | null | undefined;
  /** Dynamic property name */
  name: string;
  /** Dynamic property value. ID must be passed for dictionary item */
  value?: unknown;
};

export type InputInviteUserType = {
  /** Customer order Id to be associated with this user. */
  customerOrderId?: string | null | undefined;
  /** Emails which will receive invites */
  emails: Array<string>;
  /** Optional message to include into email with instructions which invites persons will see */
  message?: string | null | undefined;
  /** ID of organization where contact will be added for user */
  organizationId?: string | null | undefined;
  /** Role IDs or names to be assigned to the invited user */
  roleIds?: Array<string> | null | undefined;
  /** ID of store which will send invites */
  storeId: string;
  /** Optional URL suffix: you may provide here relative URL to your page which handle registration by invite */
  urlSuffix?: string | null | undefined;
};

export type InputLockUnlockOrganizationContactType = {
  /** Contact member ID */
  memberId: string;
};

export type InputMemberAddressType = {
  addressType?: number | null | undefined;
  /** City */
  city: string;
  /** Country code */
  countryCode: string;
  /** Country name */
  countryName?: string | null | undefined;
  /** Description */
  description?: string | null | undefined;
  /** Email */
  email?: string | null | undefined;
  /** First name */
  firstName?: string | null | undefined;
  /** Id */
  id?: string | null | undefined;
  /** key */
  key?: string | null | undefined;
  /** Last name */
  lastName?: string | null | undefined;
  /** Line1 */
  line1: string;
  /** Line2 */
  line2?: string | null | undefined;
  /** Middle name */
  middleName?: string | null | undefined;
  /** Name */
  name?: string | null | undefined;
  /** Company name */
  organization?: string | null | undefined;
  /** Outer id */
  outerId?: string | null | undefined;
  /** Phone */
  phone?: string | null | undefined;
  /** Postal code */
  postalCode: string;
  /** Region id */
  regionId?: string | null | undefined;
  /** Region name */
  regionName?: string | null | undefined;
  /** Zip */
  zip?: string | null | undefined;
};

export type InputMergeCartType = {
  cartId?: string | null | undefined;
  cartName?: string | null | undefined;
  cartType?: string | null | undefined;
  cultureName?: string | null | undefined;
  currencyCode?: string | null | undefined;
  /** Delete second cart after merge */
  deleteAfterMerge?: boolean | null | undefined;
  /** Second cart Id */
  secondCartId: string;
  storeId: string;
  userId: string;
};

export type InputNewBulkItemType = {
  /** Product SKU */
  productSku: string;
  /** Product quantity */
  quantity?: number | null | undefined;
};

export type InputNewCartItemType = {
  /** Comment */
  comment?: string | null | undefined;
  /** Configurable product sections */
  configurationSections?: Array<ConfigurationSectionInput | null | undefined> | null | undefined;
  /** Line item created date override */
  createdDate?: string | null | undefined;
  dynamicProperties?: Array<InputDynamicPropertyValueType | null | undefined> | null | undefined;
  /** Add the product in a different currency */
  itemCurrencyCode?: string | null | undefined;
  /** Price */
  price?: number | null | undefined;
  /** Product Id */
  productId: string;
  /** Product quantity */
  quantity?: number | null | undefined;
};

export type InputNewWishlistItemType = {
  /** Product Id */
  productId: string;
  /** Product quantity */
  quantity?: number | null | undefined;
};

export type InputPaymentType = {
  amount?: number | null | null | undefined;
  billingAddress?: InputAddressType | null | undefined;
  /** Text comment */
  comment?: string | null | null | undefined;
  currency?: string | null | null | undefined;
  /** Dynamic properties */
  dynamicProperties?: Array<InputDynamicPropertyValueType | null | undefined> | null | undefined;
  /** Payment ID */
  id?: string | null | null | undefined;
  /** Payment outer ID value */
  outerId?: string | null | null | undefined;
  /** Payment gateway code value */
  paymentGatewayCode?: string | null | null | undefined;
  price?: number | null | null | undefined;
  purpose?: string | null | null | undefined;
  vendorId?: string | null | null | undefined;
};

export type InputQuoteAddressType = {
  addressType?: number | null | undefined;
  city: string;
  countryCode?: string | null | undefined;
  countryName: string;
  email?: string | null | undefined;
  firstName?: string | null | undefined;
  id?: string | null | undefined;
  key?: string | null | undefined;
  lastName?: string | null | undefined;
  line1?: string | null | undefined;
  line2?: string | null | undefined;
  name?: string | null | undefined;
  /** Company name */
  organization?: string | null | undefined;
  outerId?: string | null | undefined;
  phone?: string | null | undefined;
  postalCode?: string | null | undefined;
  regionId?: string | null | undefined;
  regionName?: string | null | undefined;
};

export type InputRegisterAccountType = {
  email: string;
  password: string;
  username: string;
};

export type InputRegisterByInvitationType = {
  /** Customer order Id to be associated with this user. */
  customerOrderId?: string | null | undefined;
  /** First name of person */
  firstName: string;
  /** Last name of person */
  lastName: string;
  /** ID of the organization this invite was for. Only this organization's pending invite is approved on registration. */
  organizationId?: string | null | undefined;
  /** Password */
  password: string;
  /** Phone */
  phone?: string | null | undefined;
  /** Invitation token */
  token: string;
  /** ID of use created for invited email */
  userId: string;
  /** Username */
  username: string;
};

export type InputRegisterContactType = {
  about?: string | null | undefined;
  address?: InputMemberAddressType | null | undefined;
  birthdate?: string | null | undefined;
  dynamicProperties?: Array<InputDynamicPropertyValueType | null | undefined> | null | undefined;
  firstName: string;
  lastName: string;
  middleName?: string | null | undefined;
  phoneNumber?: string | null | undefined;
};

export type InputRegisterOrganizationType = {
  address?: InputMemberAddressType | null | undefined;
  addresses?: Array<InputMemberAddressType | null | undefined> | null | undefined;
  description?: string | null | undefined;
  dynamicProperties?: Array<InputDynamicPropertyValueType | null | undefined> | null | undefined;
  name: string;
  phoneNumber?: string | null | undefined;
};

export type InputRemoveCartType = {
  /** Cart Id */
  cartId: string;
  /** User Id */
  userId: string;
};

export type InputRemoveCouponType = {
  cartId?: string | null | undefined;
  cartName?: string | null | undefined;
  cartType?: string | null | undefined;
  /** Coupon code */
  couponCode?: string | null | undefined;
  cultureName?: string | null | undefined;
  currencyCode?: string | null | undefined;
  storeId: string;
  userId: string;
};

export type InputRemoveItemType = {
  cartId?: string | null | undefined;
  cartName?: string | null | undefined;
  cartType?: string | null | undefined;
  cultureName?: string | null | undefined;
  currencyCode?: string | null | undefined;
  /** Line item Id */
  lineItemId: string;
  storeId: string;
  userId: string;
};

export type InputRemoveWishlistItemsType = {
  /** Line item IDs to remove */
  lineItemIds: Array<string>;
  /** List ID */
  listId: string;
};

export type InputRemoveWishlistType = {
  /** List ID */
  listId: string;
};

export type InputRequestRegistrationType = {
  /** Creating contact's account */
  account: InputRegisterAccountType;
  /** Creating contact */
  contact: InputRegisterContactType;
  /** Notification language code */
  languageCode?: string | null | undefined;
  /** company type */
  organization?: InputRegisterOrganizationType | null | undefined;
  /** Store ID */
  storeId: string;
};

export type InputResetPasswordByTokenType = {
  /** New password according with system security policy */
  newPassword: string;
  /** User password reset token */
  token: string;
  /** User identifier */
  userId: string;
};

export type InputSaveForLaterType = {
  /** Source Cart ID */
  cartId: string;
  /** Culture name */
  cultureName?: string | null | undefined;
  /** Currency code */
  currencyCode?: string | null | undefined;
  /** Line item IDs to save for later */
  lineItemIds: Array<string | null | undefined>;
  /** Store ID */
  storeId: string;
  /** Owner ID */
  userId: string;
};

export type InputShipmentType = {
  /** Text comment */
  comment?: string | null | null | undefined;
  /** Currency value */
  currency?: string | null | null | undefined;
  /** Delivery address */
  deliveryAddress?: InputAddressType | null | undefined;
  /** Dynamic properties */
  dynamicProperties?: Array<InputDynamicPropertyValueType | null | undefined> | null | undefined;
  /** Fulfillment center iD */
  fulfillmentCenterId?: string | null | null | undefined;
  /** Height value */
  height?: number | null | null | undefined;
  /** Shipment ID */
  id?: string | null | null | undefined;
  /** Length value */
  length?: number | null | null | undefined;
  /** Measurement unit value */
  measureUnit?: string | null | null | undefined;
  /** Pickup location Id when shipment is Pickup */
  pickupLocationId?: string | null | null | undefined;
  /** Price value */
  price?: number | null | null | undefined;
  /** Shipping method code */
  shipmentMethodCode?: string | null | null | undefined;
  /** Shipping method option */
  shipmentMethodOption?: string | null | null | undefined;
  /** Vendor ID */
  vendorId?: string | null | null | undefined;
  /** Volumetric weight value */
  volumetricWeight?: number | null | null | undefined;
  /** Weight value */
  weight?: number | null | null | undefined;
  /** Weight unit value */
  weightUnit?: string | null | null | undefined;
  /** Width value */
  width?: number | null | null | undefined;
};

export type InputUpdateCartQuantity = {
  cartId?: string | null | undefined;
  cartName?: string | null | undefined;
  cartType?: string | null | undefined;
  cultureName?: string | null | undefined;
  currencyCode?: string | null | undefined;
  items?: Array<InputUpdateCartQuantityItem | null | undefined> | null | undefined;
  storeId: string;
  userId: string;
};

export type InputUpdateCartQuantityItem = {
  /** Add the product in a different currency */
  itemCurrencyCode?: string | null | undefined;
  /** Product ID */
  productId: string;
  /** Quantity */
  quantity: number;
};

export type InputUpdateMemberAddressType = {
  addresses: Array<InputMemberAddressType | null | undefined>;
  memberId: string;
};

export type InputUpdateWishlistItemsType = {
  /** Bulk wishlist items */
  items: Array<InputUpdateWishlistLineItemType | null | undefined>;
  /** Wish list id */
  listId: string;
};

export type InputUpdateWishlistLineItemType = {
  /** Line Item Id to update */
  lineItemId: string;
  /** Product quantity to add */
  quantity: number;
};

export type ProductPickupAvailabilityType =
  /** Available via global transfer (within weeks) */
  | "GlobalTransfer"
  /** Available today (within hours) */
  | "Today"
  /** Available via transfer (within days) */
  | "Transfer";

export type RemoveAddressFromFavoritesCommandType = {
  addressId: string;
};

export type RemoveQuoteItemCommandType = {
  lineItemId: string;
  quoteId: string;
};

export type SendPasswordResetEmailCommandType = {
  cultureName?: string | null | undefined;
  loginOrEmail: string;
  storeId?: string | null | undefined;
  urlSuffix?: string | null | undefined;
};

export type SubmitQuoteCommandType = {
  comment: string;
  quoteId: string;
};

export type UpdateQuoteAddressesCommandType = {
  addresses: Array<InputQuoteAddressType | null | undefined>;
  quoteId: string;
};

export type WishlistScopeType =
  /** Anyone (anonymous) scope */
  | "AnyoneAnonymous"
  /** Anyone (authorized) scope */
  | "AnyoneAuthorized"
  /** Organization scope */
  | "Organization"
  /** Private scope */
  | "Private"
  /** User scope */
  | "User";

export type CartAddressFragment = {
  id: string | null;
  key: string | null;
  city: string | null;
  countryCode: string | null;
  countryName: string | null;
  email: string | null;
  firstName: string | null;
  middleName: string | null;
  lastName: string | null;
  line1: string | null;
  line2: string | null;
  name: string | null;
  organization: string | null;
  phone: string | null;
  postalCode: string;
  regionId: string | null;
  regionName: string | null;
  zip: string | null;
  outerId: string | null;
  description: string | null;
  addressType: number | null;
};

export type CartConfigurationItemFragment = {
  id: string;
  sectionId: string;
  type: string;
  productId: string | null;
  name: string | null;
  sku: string | null;
  imageUrl: string | null;
  quantity: number | null;
  customText: string | null;
  selectedForCheckout: boolean;
};

export type CartWithListFragment = {
  cart: {
    id: string;
    storeId: string;
    isAnonymous: boolean;
    hasPhysicalProducts: boolean | null;
    customerId: string;
    itemsCount: number;
    itemsQuantity: number;
    total: { amount: number; formattedAmount: string };
    subTotal: { amount: number; formattedAmount: string };
    subTotalDiscount: { amount: number; formattedAmount: string };
    shippingTotal: { amount: number; formattedAmount: string };
    items: Array<{
      id: string;
      sku: string;
      productId: string;
      name: string;
      quantity: number;
      selectedForCheckout: boolean;
      isValid: boolean;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      placedPrice: { amount: number; formattedAmount: string };
      extendedPrice: { amount: number; formattedAmount: string };
      discountAmount: { amount: number; formattedAmount: string };
      validationErrors: Array<{
        errorCode: string | null;
        errorMessage: string | null;
        objectType: string | null;
        objectId: string | null;
        errorParameters: Array<{ key: string; value: string } | null> | null;
      }>;
      configurationItems: Array<{
        id: string;
        sectionId: string;
        type: string;
        productId: string | null;
        name: string | null;
        sku: string | null;
        imageUrl: string | null;
        quantity: number | null;
        customText: string | null;
        selectedForCheckout: boolean;
      } | null> | null;
    }>;
    payments: Array<{
      id: string;
      outerId: string | null;
      paymentGatewayCode: string | null;
      currency: { code: string };
      total: { amount: number; formattedAmount: string };
      billingAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    shipments: Array<{
      id: string;
      shipmentMethodCode: string | null;
      shipmentMethodOption: string | null;
      fulfillmentCenterId: string | null;
      price: { amount: number; formattedAmount: string };
      currency: { code: string };
      deliveryAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
    gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
    addresses: Array<{
      id: string | null;
      key: string | null;
      city: string | null;
      countryCode: string | null;
      countryName: string | null;
      email: string | null;
      firstName: string | null;
      middleName: string | null;
      lastName: string | null;
      line1: string | null;
      line2: string | null;
      name: string | null;
      organization: string | null;
      phone: string | null;
      postalCode: string;
      regionId: string | null;
      regionName: string | null;
      zip: string | null;
      outerId: string | null;
      description: string | null;
      addressType: number | null;
    }>;
    validationErrors: Array<{
      errorCode: string | null;
      errorMessage: string | null;
      objectType: string | null;
      objectId: string | null;
      errorParameters: Array<{ key: string; value: string } | null> | null;
    }>;
  } | null;
  list: {
    id: string;
    storeId: string;
    isAnonymous: boolean;
    hasPhysicalProducts: boolean | null;
    customerId: string;
    itemsCount: number;
    itemsQuantity: number;
    total: { amount: number; formattedAmount: string };
    subTotal: { amount: number; formattedAmount: string };
    subTotalDiscount: { amount: number; formattedAmount: string };
    shippingTotal: { amount: number; formattedAmount: string };
    items: Array<{
      id: string;
      sku: string;
      productId: string;
      name: string;
      quantity: number;
      selectedForCheckout: boolean;
      isValid: boolean;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      placedPrice: { amount: number; formattedAmount: string };
      extendedPrice: { amount: number; formattedAmount: string };
      discountAmount: { amount: number; formattedAmount: string };
      validationErrors: Array<{
        errorCode: string | null;
        errorMessage: string | null;
        objectType: string | null;
        objectId: string | null;
        errorParameters: Array<{ key: string; value: string } | null> | null;
      }>;
      configurationItems: Array<{
        id: string;
        sectionId: string;
        type: string;
        productId: string | null;
        name: string | null;
        sku: string | null;
        imageUrl: string | null;
        quantity: number | null;
        customText: string | null;
        selectedForCheckout: boolean;
      } | null> | null;
    }>;
    payments: Array<{
      id: string;
      outerId: string | null;
      paymentGatewayCode: string | null;
      currency: { code: string };
      total: { amount: number; formattedAmount: string };
      billingAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    shipments: Array<{
      id: string;
      shipmentMethodCode: string | null;
      shipmentMethodOption: string | null;
      fulfillmentCenterId: string | null;
      price: { amount: number; formattedAmount: string };
      currency: { code: string };
      deliveryAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
    gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
    addresses: Array<{
      id: string | null;
      key: string | null;
      city: string | null;
      countryCode: string | null;
      countryName: string | null;
      email: string | null;
      firstName: string | null;
      middleName: string | null;
      lastName: string | null;
      line1: string | null;
      line2: string | null;
      name: string | null;
      organization: string | null;
      phone: string | null;
      postalCode: string;
      regionId: string | null;
      regionName: string | null;
      zip: string | null;
      outerId: string | null;
      description: string | null;
      addressType: number | null;
    }>;
    validationErrors: Array<{
      errorCode: string | null;
      errorMessage: string | null;
      objectType: string | null;
      objectId: string | null;
      errorParameters: Array<{ key: string; value: string } | null> | null;
    }>;
  } | null;
};

export type CartFragment = {
  id: string;
  storeId: string;
  isAnonymous: boolean;
  hasPhysicalProducts: boolean | null;
  customerId: string;
  itemsCount: number;
  itemsQuantity: number;
  total: { amount: number; formattedAmount: string };
  subTotal: { amount: number; formattedAmount: string };
  subTotalDiscount: { amount: number; formattedAmount: string };
  shippingTotal: { amount: number; formattedAmount: string };
  items: Array<{
    id: string;
    sku: string;
    productId: string;
    name: string;
    quantity: number;
    selectedForCheckout: boolean;
    isValid: boolean;
    listPrice: { amount: number; formattedAmount: string };
    salePrice: { amount: number; formattedAmount: string };
    placedPrice: { amount: number; formattedAmount: string };
    extendedPrice: { amount: number; formattedAmount: string };
    discountAmount: { amount: number; formattedAmount: string };
    validationErrors: Array<{
      errorCode: string | null;
      errorMessage: string | null;
      objectType: string | null;
      objectId: string | null;
      errorParameters: Array<{ key: string; value: string } | null> | null;
    }>;
    configurationItems: Array<{
      id: string;
      sectionId: string;
      type: string;
      productId: string | null;
      name: string | null;
      sku: string | null;
      imageUrl: string | null;
      quantity: number | null;
      customText: string | null;
      selectedForCheckout: boolean;
    } | null> | null;
  }>;
  payments: Array<{
    id: string;
    outerId: string | null;
    paymentGatewayCode: string | null;
    currency: { code: string };
    total: { amount: number; formattedAmount: string };
    billingAddress: {
      id: string | null;
      key: string | null;
      city: string | null;
      countryCode: string | null;
      countryName: string | null;
      email: string | null;
      firstName: string | null;
      middleName: string | null;
      lastName: string | null;
      line1: string | null;
      line2: string | null;
      name: string | null;
      organization: string | null;
      phone: string | null;
      postalCode: string;
      regionId: string | null;
      regionName: string | null;
      zip: string | null;
      outerId: string | null;
      description: string | null;
      addressType: number | null;
    } | null;
  }>;
  shipments: Array<{
    id: string;
    shipmentMethodCode: string | null;
    shipmentMethodOption: string | null;
    fulfillmentCenterId: string | null;
    price: { amount: number; formattedAmount: string };
    currency: { code: string };
    deliveryAddress: {
      id: string | null;
      key: string | null;
      city: string | null;
      countryCode: string | null;
      countryName: string | null;
      email: string | null;
      firstName: string | null;
      middleName: string | null;
      lastName: string | null;
      line1: string | null;
      line2: string | null;
      name: string | null;
      organization: string | null;
      phone: string | null;
      postalCode: string;
      regionId: string | null;
      regionName: string | null;
      zip: string | null;
      outerId: string | null;
      description: string | null;
      addressType: number | null;
    } | null;
  }>;
  coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
  gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
  addresses: Array<{
    id: string | null;
    key: string | null;
    city: string | null;
    countryCode: string | null;
    countryName: string | null;
    email: string | null;
    firstName: string | null;
    middleName: string | null;
    lastName: string | null;
    line1: string | null;
    line2: string | null;
    name: string | null;
    organization: string | null;
    phone: string | null;
    postalCode: string;
    regionId: string | null;
    regionName: string | null;
    zip: string | null;
    outerId: string | null;
    description: string | null;
    addressType: number | null;
  }>;
  validationErrors: Array<{
    errorCode: string | null;
    errorMessage: string | null;
    objectType: string | null;
    objectId: string | null;
    errorParameters: Array<{ key: string; value: string } | null> | null;
  }>;
};

export type CategoryFragment = { id: string; code: string; name: string; outline: string | null; slug: string | null };

export type ConfigurationLineItemFragment = {
  id: string | null;
  text: string | null;
  quantity: number;
  product: {
    id: string;
    code: string;
    productType: string | null;
    isConfigurable: boolean;
    name: string;
    vendor: { id: string; name: string } | null;
    price: { list: { amount: number; formattedAmount: string }; actual: { amount: number; formattedAmount: string } };
  } | null;
  listPrice: { amount: number; formattedAmount: string } | null;
  salePrice: { amount: number; formattedAmount: string } | null;
  extendedPrice: { amount: number; formattedAmount: string } | null;
  discountAmount: { amount: number; formattedAmount: string } | null;
};

export type ContactFragment = {
  id: string;
  firstName: string;
  lastName: string;
  fullName: string;
  status: string | null;
  organizationId: string | null;
  organizationsIds: Array<string | null> | null;
  securityAccounts: Array<{
    id: string;
    userName: string;
    email: string | null;
    emailConfirmed: boolean;
    isAdministrator: boolean;
    memberId: string | null;
    storeId: string | null;
    roles: Array<{ id: string; name: string; normalizedName: string } | null> | null;
  } | null> | null;
};

export type CouponFragment = { code: string | null; isAppliedSuccessfully: boolean };

export type CurrencyFragment = { code: string };

export type CustomIdentityResultFragment = {
  succeeded: boolean;
  errors: Array<{ code: string; parameter: string | null; description: string | null } | null> | null;
};

export type GiftItemFragment = {
  id: string;
  quantity: number;
  productId: string | null;
  name: string;
  lineItemId: string | null;
};

export type IdentityResultFragment = {
  succeeded: boolean;
  errors: Array<{ code: string | null; description: string | null } | null> | null;
};

export type LanguageFragment = { cultureName: string; nativeName: string };

export type LineItemFragment = {
  id: string;
  sku: string;
  productId: string;
  name: string;
  quantity: number;
  selectedForCheckout: boolean;
  isValid: boolean;
  listPrice: { amount: number; formattedAmount: string };
  salePrice: { amount: number; formattedAmount: string };
  placedPrice: { amount: number; formattedAmount: string };
  extendedPrice: { amount: number; formattedAmount: string };
  discountAmount: { amount: number; formattedAmount: string };
  validationErrors: Array<{
    errorCode: string | null;
    errorMessage: string | null;
    objectType: string | null;
    objectId: string | null;
    errorParameters: Array<{ key: string; value: string } | null> | null;
  }>;
  configurationItems: Array<{
    id: string;
    sectionId: string;
    type: string;
    productId: string | null;
    name: string | null;
    sku: string | null;
    imageUrl: string | null;
    quantity: number | null;
    customText: string | null;
    selectedForCheckout: boolean;
  } | null> | null;
};

export type MemberAddressFragment = {
  id: string | null;
  key: string | null;
  isDefault: boolean;
  isFavorite: boolean;
  city: string | null;
  countryCode: string | null;
  countryName: string | null;
  email: string | null;
  firstName: string | null;
  middleName: string | null;
  lastName: string | null;
  line1: string | null;
  line2: string | null;
  name: string | null;
  organization: string | null;
  phone: string | null;
  postalCode: string;
  regionId: string | null;
  regionName: string | null;
  zip: string | null;
  outerId: string | null;
  description: string | null;
  addressType: number | null;
};

export type MenuLinkFragment = { title: string; url: string; priority: number };

export type MoneyFragment = { amount: number; formattedAmount: string };

export type OrderLineItemFragment = {
  id: string;
  name: string;
  sku: string;
  productId: string;
  quantity: number;
  price: { amount: number; formattedAmount: string };
  extendedPrice: { amount: number; formattedAmount: string };
};

export type OrderPaymentFragment = {
  id: string;
  number: string;
  gatewayCode: string | null;
  status: string | null;
  sum: { amount: number; formattedAmount: string };
};

export type OrderShipmentFragment = {
  id: string;
  number: string;
  shipmentMethodCode: string | null;
  shipmentMethodOption: string | null;
  status: string | null;
  total: { amount: number; formattedAmount: string };
};

export type OrderFragment = {
  id: string;
  number: string;
  status: string | null;
  createdDate: string;
  total: { amount: number; formattedAmount: string };
  items: Array<{
    id: string;
    name: string;
    sku: string;
    productId: string;
    quantity: number;
    price: { amount: number; formattedAmount: string };
    extendedPrice: { amount: number; formattedAmount: string };
  }>;
  inPayments: Array<{
    id: string;
    number: string;
    gatewayCode: string | null;
    status: string | null;
    sum: { amount: number; formattedAmount: string };
  }>;
  shipments: Array<{
    id: string;
    number: string;
    shipmentMethodCode: string | null;
    shipmentMethodOption: string | null;
    status: string | null;
    total: { amount: number; formattedAmount: string };
  }>;
};

export type PageContextFragment = {
  slugInfo: {
    redirectUrl: string | null;
    entityInfo: {
      id: string;
      name: string | null;
      semanticUrl: string;
      outline: string | null;
      pageTitle: string | null;
      metaDescription: string | null;
      imageAltDescription: string | null;
      metaKeywords: string | null;
      storeId: string | null;
      objectId: string;
      objectType: string;
      isActive: boolean;
      languageCode: string | null;
    } | null;
  } | null;
  store: {
    storeId: string;
    storeName: string;
    catalogId: string;
    storeUrl: string | null;
    defaultLanguage: { cultureName: string; nativeName: string };
    availableLanguages: Array<{ cultureName: string; nativeName: string }>;
    defaultCurrency: { code: string };
    availableCurrencies: Array<{ code: string }>;
    settings: { anonymousUsersAllowed: boolean; taxCalculationEnabled: boolean; seoLinkType: string };
  } | null;
  whiteLabelingSettings: {
    logoUrl: string | null;
    secondaryLogoUrl: string | null;
    faviconUrl: string | null;
    themePresetName: string | null;
    footerLinks: Array<{ title: string; url: string; priority: number } | null> | null;
    mainMenuLinks: Array<{ title: string; url: string; priority: number } | null> | null;
  } | null;
  user: {
    id: string;
    userName: string;
    email: string | null;
    emailConfirmed: boolean;
    isAdministrator: boolean;
    memberId: string | null;
    storeId: string | null;
    roles: Array<{ id: string; name: string; normalizedName: string } | null> | null;
  } | null;
};

export type PaymentFragment = {
  id: string;
  outerId: string | null;
  paymentGatewayCode: string | null;
  currency: { code: string };
  total: { amount: number; formattedAmount: string };
  billingAddress: {
    id: string | null;
    key: string | null;
    city: string | null;
    countryCode: string | null;
    countryName: string | null;
    email: string | null;
    firstName: string | null;
    middleName: string | null;
    lastName: string | null;
    line1: string | null;
    line2: string | null;
    name: string | null;
    organization: string | null;
    phone: string | null;
    postalCode: string;
    regionId: string | null;
    regionName: string | null;
    zip: string | null;
    outerId: string | null;
    description: string | null;
    addressType: number | null;
  } | null;
};

export type PickupAddressFragment = {
  id: string;
  key: string | null;
  name: string | null;
  organization: string | null;
  countryCode: string | null;
  countryName: string | null;
  city: string | null;
  postalCode: string | null;
  line1: string | null;
  line2: string | null;
  regionId: string | null;
  regionName: string | null;
  phone: string | null;
  email: string | null;
  outerId: string | null;
  description: string | null;
  addressType: number | null;
};

export type PickupLocationAddressFragment = {
  id: string;
  key: string | null;
  name: string | null;
  organization: string | null;
  countryCode: string | null;
  countryName: string | null;
  city: string | null;
  postalCode: string | null;
  line1: string | null;
  line2: string | null;
  regionId: string | null;
  regionName: string | null;
  phone: string | null;
  email: string | null;
  outerId: string | null;
  description: string | null;
  addressType: number | null;
};

export type PickupLocationFragment = {
  id: string;
  isActive: boolean;
  name: string;
  description: string | null;
  contactEmail: string | null;
  contactPhone: string | null;
  workingHours: string | null;
  geoLocation: string | null;
  address: {
    id: string;
    key: string | null;
    name: string | null;
    organization: string | null;
    countryCode: string | null;
    countryName: string | null;
    city: string | null;
    postalCode: string | null;
    line1: string | null;
    line2: string | null;
    regionId: string | null;
    regionName: string | null;
    phone: string | null;
    email: string | null;
    outerId: string | null;
    description: string | null;
    addressType: number | null;
  } | null;
};

export type ProductConfigurationFragment = {
  configurationSections: Array<{
    id: string;
    name: string | null;
    description: string | null;
    isRequired: boolean;
    type: string;
    allowCustomText: boolean;
    allowTextOptions: boolean;
    maxLength: number | null;
    options: Array<{
      id: string | null;
      text: string | null;
      quantity: number;
      product: {
        id: string;
        code: string;
        productType: string | null;
        isConfigurable: boolean;
        name: string;
        vendor: { id: string; name: string } | null;
        price: {
          list: { amount: number; formattedAmount: string };
          actual: { amount: number; formattedAmount: string };
        };
      } | null;
      listPrice: { amount: number; formattedAmount: string } | null;
      salePrice: { amount: number; formattedAmount: string } | null;
      extendedPrice: { amount: number; formattedAmount: string } | null;
      discountAmount: { amount: number; formattedAmount: string } | null;
    } | null> | null;
  } | null> | null;
};

export type ProductPickupLocationFragment = {
  id: string;
  isActive: boolean;
  name: string;
  description: string | null;
  contactEmail: string | null;
  contactPhone: string | null;
  workingHours: string | null;
  deliveryDays: number | null;
  storageDays: number | null;
  geoLocation: string | null;
  availabilityType: ProductPickupAvailabilityType | null;
  availabilityNote: string | null;
  availableQuantity: number | null;
  address: {
    id: string;
    key: string | null;
    name: string | null;
    organization: string | null;
    countryCode: string | null;
    countryName: string | null;
    city: string | null;
    postalCode: string | null;
    line1: string | null;
    line2: string | null;
    regionId: string | null;
    regionName: string | null;
    phone: string | null;
    email: string | null;
    outerId: string | null;
    description: string | null;
    addressType: number | null;
  } | null;
};

export type ProductPriceFragment = {
  list: { amount: number; formattedAmount: string };
  actual: { amount: number; formattedAmount: string };
};

export type ProductFragment = {
  id: string;
  code: string;
  productType: string | null;
  isConfigurable: boolean;
  name: string;
  vendor: { id: string; name: string } | null;
  price: { list: { amount: number; formattedAmount: string }; actual: { amount: number; formattedAmount: string } };
};

export type QuoteAddressFragment = {
  addressType: number | null;
  city: string;
  countryCode: string | null;
  countryName: string;
  line1: string | null;
  postalCode: string | null;
  regionId: string | null;
  regionName: string | null;
};

export type QuoteItemFragment = {
  id: string;
  name: string;
  sku: string | null;
  productId: string | null;
  quantity: number;
  listPrice: { amount: number; formattedAmount: string };
  salePrice: { amount: number; formattedAmount: string };
  proposalPrices: Array<{ quantity: number; price: { amount: number; formattedAmount: string } }>;
};

export type QuoteTotalsFragment = {
  originalSubTotalExlTax: { amount: number; formattedAmount: string };
  subTotalExlTax: { amount: number; formattedAmount: string };
  shippingTotal: { amount: number; formattedAmount: string };
  discountTotal: { amount: number; formattedAmount: string };
  taxTotal: { amount: number; formattedAmount: string };
  grandTotalExlTax: { amount: number; formattedAmount: string };
  grandTotalInclTax: { amount: number; formattedAmount: string };
};

export type QuoteFragment = {
  id: string;
  number: string;
  status: string | null;
  storeId: string;
  customerId: string | null;
  comment: string | null;
  isAnonymous: boolean;
  isCancelled: boolean;
  totals: {
    originalSubTotalExlTax: { amount: number; formattedAmount: string };
    subTotalExlTax: { amount: number; formattedAmount: string };
    shippingTotal: { amount: number; formattedAmount: string };
    discountTotal: { amount: number; formattedAmount: string };
    taxTotal: { amount: number; formattedAmount: string };
    grandTotalExlTax: { amount: number; formattedAmount: string };
    grandTotalInclTax: { amount: number; formattedAmount: string };
  };
  items: Array<{
    id: string;
    name: string;
    sku: string | null;
    productId: string | null;
    quantity: number;
    listPrice: { amount: number; formattedAmount: string };
    salePrice: { amount: number; formattedAmount: string };
    proposalPrices: Array<{ quantity: number; price: { amount: number; formattedAmount: string } }>;
  }>;
};

export type RoleFragment = { id: string; name: string; normalizedName: string };

export type SeoInfoFragment = {
  id: string;
  name: string | null;
  semanticUrl: string;
  outline: string | null;
  pageTitle: string | null;
  metaDescription: string | null;
  imageAltDescription: string | null;
  metaKeywords: string | null;
  storeId: string | null;
  objectId: string;
  objectType: string;
  isActive: boolean;
  languageCode: string | null;
};

export type ShipmentFragment = {
  id: string;
  shipmentMethodCode: string | null;
  shipmentMethodOption: string | null;
  fulfillmentCenterId: string | null;
  price: { amount: number; formattedAmount: string };
  currency: { code: string };
  deliveryAddress: {
    id: string | null;
    key: string | null;
    city: string | null;
    countryCode: string | null;
    countryName: string | null;
    email: string | null;
    firstName: string | null;
    middleName: string | null;
    lastName: string | null;
    line1: string | null;
    line2: string | null;
    name: string | null;
    organization: string | null;
    phone: string | null;
    postalCode: string;
    regionId: string | null;
    regionName: string | null;
    zip: string | null;
    outerId: string | null;
    description: string | null;
    addressType: number | null;
  } | null;
};

export type ShoppingListFragment = {
  id: string;
  name: string;
  storeId: string | null;
  customerId: string | null;
  customerName: string | null;
  itemsCount: number | null;
  description: string | null;
  items: Array<{ id: string; sku: string; productId: string; name: string; quantity: number } | null> | null;
  subTotal: { amount: number; formattedAmount: string };
  sharingSetting: { id: string; scope: WishlistScopeType | null } | null;
};

export type SlugInfoFragment = {
  redirectUrl: string | null;
  entityInfo: {
    id: string;
    name: string | null;
    semanticUrl: string;
    outline: string | null;
    pageTitle: string | null;
    metaDescription: string | null;
    imageAltDescription: string | null;
    metaKeywords: string | null;
    storeId: string | null;
    objectId: string;
    objectType: string;
    isActive: boolean;
    languageCode: string | null;
  } | null;
};

export type StoreInfoFragment = {
  storeId: string;
  storeName: string;
  catalogId: string;
  storeUrl: string | null;
  defaultLanguage: { cultureName: string; nativeName: string };
  availableLanguages: Array<{ cultureName: string; nativeName: string }>;
  defaultCurrency: { code: string };
  availableCurrencies: Array<{ code: string }>;
  settings: { anonymousUsersAllowed: boolean; taxCalculationEnabled: boolean; seoLinkType: string };
};

export type StoreSettingsFragment = {
  anonymousUsersAllowed: boolean;
  taxCalculationEnabled: boolean;
  seoLinkType: string;
};

export type UserFragment = {
  id: string;
  userName: string;
  email: string | null;
  emailConfirmed: boolean;
  isAdministrator: boolean;
  memberId: string | null;
  storeId: string | null;
  roles: Array<{ id: string; name: string; normalizedName: string } | null> | null;
};

export type VendorFragment = { id: string; name: string };

export type WhiteLabelingSettingsFragment = {
  logoUrl: string | null;
  secondaryLogoUrl: string | null;
  faviconUrl: string | null;
  themePresetName: string | null;
  footerLinks: Array<{ title: string; url: string; priority: number } | null> | null;
  mainMenuLinks: Array<{ title: string; url: string; priority: number } | null> | null;
};

export type WishlistLineItemFragment = { id: string; sku: string; productId: string; name: string; quantity: number };

export type AddBulkItemsCartMutationVariables = Exact<{
  command: InputAddBulkItemsType;
}>;

export type AddBulkItemsCartMutation = {
  addBulkItemsCart: {
    cart: {
      id: string;
      storeId: string;
      isAnonymous: boolean;
      hasPhysicalProducts: boolean | null;
      customerId: string;
      itemsCount: number;
      itemsQuantity: number;
      total: { amount: number; formattedAmount: string };
      subTotal: { amount: number; formattedAmount: string };
      subTotalDiscount: { amount: number; formattedAmount: string };
      shippingTotal: { amount: number; formattedAmount: string };
      items: Array<{
        id: string;
        sku: string;
        productId: string;
        name: string;
        quantity: number;
        selectedForCheckout: boolean;
        isValid: boolean;
        listPrice: { amount: number; formattedAmount: string };
        salePrice: { amount: number; formattedAmount: string };
        placedPrice: { amount: number; formattedAmount: string };
        extendedPrice: { amount: number; formattedAmount: string };
        discountAmount: { amount: number; formattedAmount: string };
        validationErrors: Array<{
          errorCode: string | null;
          errorMessage: string | null;
          objectType: string | null;
          objectId: string | null;
          errorParameters: Array<{ key: string; value: string } | null> | null;
        }>;
        configurationItems: Array<{
          id: string;
          sectionId: string;
          type: string;
          productId: string | null;
          name: string | null;
          sku: string | null;
          imageUrl: string | null;
          quantity: number | null;
          customText: string | null;
          selectedForCheckout: boolean;
        } | null> | null;
      }>;
      payments: Array<{
        id: string;
        outerId: string | null;
        paymentGatewayCode: string | null;
        currency: { code: string };
        total: { amount: number; formattedAmount: string };
        billingAddress: {
          id: string | null;
          key: string | null;
          city: string | null;
          countryCode: string | null;
          countryName: string | null;
          email: string | null;
          firstName: string | null;
          middleName: string | null;
          lastName: string | null;
          line1: string | null;
          line2: string | null;
          name: string | null;
          organization: string | null;
          phone: string | null;
          postalCode: string;
          regionId: string | null;
          regionName: string | null;
          zip: string | null;
          outerId: string | null;
          description: string | null;
          addressType: number | null;
        } | null;
      }>;
      shipments: Array<{
        id: string;
        shipmentMethodCode: string | null;
        shipmentMethodOption: string | null;
        fulfillmentCenterId: string | null;
        price: { amount: number; formattedAmount: string };
        currency: { code: string };
        deliveryAddress: {
          id: string | null;
          key: string | null;
          city: string | null;
          countryCode: string | null;
          countryName: string | null;
          email: string | null;
          firstName: string | null;
          middleName: string | null;
          lastName: string | null;
          line1: string | null;
          line2: string | null;
          name: string | null;
          organization: string | null;
          phone: string | null;
          postalCode: string;
          regionId: string | null;
          regionName: string | null;
          zip: string | null;
          outerId: string | null;
          description: string | null;
          addressType: number | null;
        } | null;
      }>;
      coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
      gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
      addresses: Array<{
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      }>;
      validationErrors: Array<{
        errorCode: string | null;
        errorMessage: string | null;
        objectType: string | null;
        objectId: string | null;
        errorParameters: Array<{ key: string; value: string } | null> | null;
      }>;
    } | null;
    errors: Array<{ errorCode: string | null; errorMessage: string | null; objectId: string | null } | null> | null;
  } | null;
};

export type AddCouponMutationVariables = Exact<{
  command: InputAddCouponType;
}>;

export type AddCouponMutation = {
  addCoupon: {
    id: string;
    storeId: string;
    isAnonymous: boolean;
    hasPhysicalProducts: boolean | null;
    customerId: string;
    itemsCount: number;
    itemsQuantity: number;
    total: { amount: number; formattedAmount: string };
    subTotal: { amount: number; formattedAmount: string };
    subTotalDiscount: { amount: number; formattedAmount: string };
    shippingTotal: { amount: number; formattedAmount: string };
    items: Array<{
      id: string;
      sku: string;
      productId: string;
      name: string;
      quantity: number;
      selectedForCheckout: boolean;
      isValid: boolean;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      placedPrice: { amount: number; formattedAmount: string };
      extendedPrice: { amount: number; formattedAmount: string };
      discountAmount: { amount: number; formattedAmount: string };
      validationErrors: Array<{
        errorCode: string | null;
        errorMessage: string | null;
        objectType: string | null;
        objectId: string | null;
        errorParameters: Array<{ key: string; value: string } | null> | null;
      }>;
      configurationItems: Array<{
        id: string;
        sectionId: string;
        type: string;
        productId: string | null;
        name: string | null;
        sku: string | null;
        imageUrl: string | null;
        quantity: number | null;
        customText: string | null;
        selectedForCheckout: boolean;
      } | null> | null;
    }>;
    payments: Array<{
      id: string;
      outerId: string | null;
      paymentGatewayCode: string | null;
      currency: { code: string };
      total: { amount: number; formattedAmount: string };
      billingAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    shipments: Array<{
      id: string;
      shipmentMethodCode: string | null;
      shipmentMethodOption: string | null;
      fulfillmentCenterId: string | null;
      price: { amount: number; formattedAmount: string };
      currency: { code: string };
      deliveryAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
    gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
    addresses: Array<{
      id: string | null;
      key: string | null;
      city: string | null;
      countryCode: string | null;
      countryName: string | null;
      email: string | null;
      firstName: string | null;
      middleName: string | null;
      lastName: string | null;
      line1: string | null;
      line2: string | null;
      name: string | null;
      organization: string | null;
      phone: string | null;
      postalCode: string;
      regionId: string | null;
      regionName: string | null;
      zip: string | null;
      outerId: string | null;
      description: string | null;
      addressType: number | null;
    }>;
    validationErrors: Array<{
      errorCode: string | null;
      errorMessage: string | null;
      objectType: string | null;
      objectId: string | null;
      errorParameters: Array<{ key: string; value: string } | null> | null;
    }>;
  } | null;
};

export type AddItemMutationVariables = Exact<{
  command: InputAddItemType;
}>;

export type AddItemMutation = {
  addItem: {
    id: string;
    storeId: string;
    isAnonymous: boolean;
    hasPhysicalProducts: boolean | null;
    customerId: string;
    itemsCount: number;
    itemsQuantity: number;
    total: { amount: number; formattedAmount: string };
    subTotal: { amount: number; formattedAmount: string };
    subTotalDiscount: { amount: number; formattedAmount: string };
    shippingTotal: { amount: number; formattedAmount: string };
    items: Array<{
      id: string;
      sku: string;
      productId: string;
      name: string;
      quantity: number;
      selectedForCheckout: boolean;
      isValid: boolean;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      placedPrice: { amount: number; formattedAmount: string };
      extendedPrice: { amount: number; formattedAmount: string };
      discountAmount: { amount: number; formattedAmount: string };
      validationErrors: Array<{
        errorCode: string | null;
        errorMessage: string | null;
        objectType: string | null;
        objectId: string | null;
        errorParameters: Array<{ key: string; value: string } | null> | null;
      }>;
      configurationItems: Array<{
        id: string;
        sectionId: string;
        type: string;
        productId: string | null;
        name: string | null;
        sku: string | null;
        imageUrl: string | null;
        quantity: number | null;
        customText: string | null;
        selectedForCheckout: boolean;
      } | null> | null;
    }>;
    payments: Array<{
      id: string;
      outerId: string | null;
      paymentGatewayCode: string | null;
      currency: { code: string };
      total: { amount: number; formattedAmount: string };
      billingAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    shipments: Array<{
      id: string;
      shipmentMethodCode: string | null;
      shipmentMethodOption: string | null;
      fulfillmentCenterId: string | null;
      price: { amount: number; formattedAmount: string };
      currency: { code: string };
      deliveryAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
    gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
    addresses: Array<{
      id: string | null;
      key: string | null;
      city: string | null;
      countryCode: string | null;
      countryName: string | null;
      email: string | null;
      firstName: string | null;
      middleName: string | null;
      lastName: string | null;
      line1: string | null;
      line2: string | null;
      name: string | null;
      organization: string | null;
      phone: string | null;
      postalCode: string;
      regionId: string | null;
      regionName: string | null;
      zip: string | null;
      outerId: string | null;
      description: string | null;
      addressType: number | null;
    }>;
    validationErrors: Array<{
      errorCode: string | null;
      errorMessage: string | null;
      objectType: string | null;
      objectId: string | null;
      errorParameters: Array<{ key: string; value: string } | null> | null;
    }>;
  } | null;
};

export type AddItemsCartMutationVariables = Exact<{
  command: InputAddItemsType;
}>;

export type AddItemsCartMutation = {
  addItemsCart: {
    id: string;
    storeId: string;
    isAnonymous: boolean;
    hasPhysicalProducts: boolean | null;
    customerId: string;
    itemsCount: number;
    itemsQuantity: number;
    total: { amount: number; formattedAmount: string };
    subTotal: { amount: number; formattedAmount: string };
    subTotalDiscount: { amount: number; formattedAmount: string };
    shippingTotal: { amount: number; formattedAmount: string };
    items: Array<{
      id: string;
      sku: string;
      productId: string;
      name: string;
      quantity: number;
      selectedForCheckout: boolean;
      isValid: boolean;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      placedPrice: { amount: number; formattedAmount: string };
      extendedPrice: { amount: number; formattedAmount: string };
      discountAmount: { amount: number; formattedAmount: string };
      validationErrors: Array<{
        errorCode: string | null;
        errorMessage: string | null;
        objectType: string | null;
        objectId: string | null;
        errorParameters: Array<{ key: string; value: string } | null> | null;
      }>;
      configurationItems: Array<{
        id: string;
        sectionId: string;
        type: string;
        productId: string | null;
        name: string | null;
        sku: string | null;
        imageUrl: string | null;
        quantity: number | null;
        customText: string | null;
        selectedForCheckout: boolean;
      } | null> | null;
    }>;
    payments: Array<{
      id: string;
      outerId: string | null;
      paymentGatewayCode: string | null;
      currency: { code: string };
      total: { amount: number; formattedAmount: string };
      billingAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    shipments: Array<{
      id: string;
      shipmentMethodCode: string | null;
      shipmentMethodOption: string | null;
      fulfillmentCenterId: string | null;
      price: { amount: number; formattedAmount: string };
      currency: { code: string };
      deliveryAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
    gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
    addresses: Array<{
      id: string | null;
      key: string | null;
      city: string | null;
      countryCode: string | null;
      countryName: string | null;
      email: string | null;
      firstName: string | null;
      middleName: string | null;
      lastName: string | null;
      line1: string | null;
      line2: string | null;
      name: string | null;
      organization: string | null;
      phone: string | null;
      postalCode: string;
      regionId: string | null;
      regionName: string | null;
      zip: string | null;
      outerId: string | null;
      description: string | null;
      addressType: number | null;
    }>;
    validationErrors: Array<{
      errorCode: string | null;
      errorMessage: string | null;
      objectType: string | null;
      objectId: string | null;
      errorParameters: Array<{ key: string; value: string } | null> | null;
    }>;
  } | null;
};

export type AddOrUpdateCartPaymentMutationVariables = Exact<{
  command: InputAddOrUpdateCartPaymentType;
}>;

export type AddOrUpdateCartPaymentMutation = {
  addOrUpdateCartPayment: {
    id: string;
    storeId: string;
    isAnonymous: boolean;
    hasPhysicalProducts: boolean | null;
    customerId: string;
    itemsCount: number;
    itemsQuantity: number;
    total: { amount: number; formattedAmount: string };
    subTotal: { amount: number; formattedAmount: string };
    subTotalDiscount: { amount: number; formattedAmount: string };
    shippingTotal: { amount: number; formattedAmount: string };
    items: Array<{
      id: string;
      sku: string;
      productId: string;
      name: string;
      quantity: number;
      selectedForCheckout: boolean;
      isValid: boolean;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      placedPrice: { amount: number; formattedAmount: string };
      extendedPrice: { amount: number; formattedAmount: string };
      discountAmount: { amount: number; formattedAmount: string };
      validationErrors: Array<{
        errorCode: string | null;
        errorMessage: string | null;
        objectType: string | null;
        objectId: string | null;
        errorParameters: Array<{ key: string; value: string } | null> | null;
      }>;
      configurationItems: Array<{
        id: string;
        sectionId: string;
        type: string;
        productId: string | null;
        name: string | null;
        sku: string | null;
        imageUrl: string | null;
        quantity: number | null;
        customText: string | null;
        selectedForCheckout: boolean;
      } | null> | null;
    }>;
    payments: Array<{
      id: string;
      outerId: string | null;
      paymentGatewayCode: string | null;
      currency: { code: string };
      total: { amount: number; formattedAmount: string };
      billingAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    shipments: Array<{
      id: string;
      shipmentMethodCode: string | null;
      shipmentMethodOption: string | null;
      fulfillmentCenterId: string | null;
      price: { amount: number; formattedAmount: string };
      currency: { code: string };
      deliveryAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
    gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
    addresses: Array<{
      id: string | null;
      key: string | null;
      city: string | null;
      countryCode: string | null;
      countryName: string | null;
      email: string | null;
      firstName: string | null;
      middleName: string | null;
      lastName: string | null;
      line1: string | null;
      line2: string | null;
      name: string | null;
      organization: string | null;
      phone: string | null;
      postalCode: string;
      regionId: string | null;
      regionName: string | null;
      zip: string | null;
      outerId: string | null;
      description: string | null;
      addressType: number | null;
    }>;
    validationErrors: Array<{
      errorCode: string | null;
      errorMessage: string | null;
      objectType: string | null;
      objectId: string | null;
      errorParameters: Array<{ key: string; value: string } | null> | null;
    }>;
  } | null;
};

export type AddOrUpdateCartShipmentMutationVariables = Exact<{
  command: InputAddOrUpdateCartShipmentType;
}>;

export type AddOrUpdateCartShipmentMutation = {
  addOrUpdateCartShipment: {
    id: string;
    storeId: string;
    isAnonymous: boolean;
    hasPhysicalProducts: boolean | null;
    customerId: string;
    itemsCount: number;
    itemsQuantity: number;
    total: { amount: number; formattedAmount: string };
    subTotal: { amount: number; formattedAmount: string };
    subTotalDiscount: { amount: number; formattedAmount: string };
    shippingTotal: { amount: number; formattedAmount: string };
    items: Array<{
      id: string;
      sku: string;
      productId: string;
      name: string;
      quantity: number;
      selectedForCheckout: boolean;
      isValid: boolean;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      placedPrice: { amount: number; formattedAmount: string };
      extendedPrice: { amount: number; formattedAmount: string };
      discountAmount: { amount: number; formattedAmount: string };
      validationErrors: Array<{
        errorCode: string | null;
        errorMessage: string | null;
        objectType: string | null;
        objectId: string | null;
        errorParameters: Array<{ key: string; value: string } | null> | null;
      }>;
      configurationItems: Array<{
        id: string;
        sectionId: string;
        type: string;
        productId: string | null;
        name: string | null;
        sku: string | null;
        imageUrl: string | null;
        quantity: number | null;
        customText: string | null;
        selectedForCheckout: boolean;
      } | null> | null;
    }>;
    payments: Array<{
      id: string;
      outerId: string | null;
      paymentGatewayCode: string | null;
      currency: { code: string };
      total: { amount: number; formattedAmount: string };
      billingAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    shipments: Array<{
      id: string;
      shipmentMethodCode: string | null;
      shipmentMethodOption: string | null;
      fulfillmentCenterId: string | null;
      price: { amount: number; formattedAmount: string };
      currency: { code: string };
      deliveryAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
    gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
    addresses: Array<{
      id: string | null;
      key: string | null;
      city: string | null;
      countryCode: string | null;
      countryName: string | null;
      email: string | null;
      firstName: string | null;
      middleName: string | null;
      lastName: string | null;
      line1: string | null;
      line2: string | null;
      name: string | null;
      organization: string | null;
      phone: string | null;
      postalCode: string;
      regionId: string | null;
      regionName: string | null;
      zip: string | null;
      outerId: string | null;
      description: string | null;
      addressType: number | null;
    }>;
    validationErrors: Array<{
      errorCode: string | null;
      errorMessage: string | null;
      objectType: string | null;
      objectId: string | null;
      errorParameters: Array<{ key: string; value: string } | null> | null;
    }>;
  } | null;
};

export type ChangeCartConfiguredItemMutationVariables = Exact<{
  command: InputChangeCartConfiguredItemType;
}>;

export type ChangeCartConfiguredItemMutation = {
  changeCartConfiguredItem: {
    id: string;
    storeId: string;
    isAnonymous: boolean;
    hasPhysicalProducts: boolean | null;
    customerId: string;
    itemsCount: number;
    itemsQuantity: number;
    total: { amount: number; formattedAmount: string };
    subTotal: { amount: number; formattedAmount: string };
    subTotalDiscount: { amount: number; formattedAmount: string };
    shippingTotal: { amount: number; formattedAmount: string };
    items: Array<{
      id: string;
      sku: string;
      productId: string;
      name: string;
      quantity: number;
      selectedForCheckout: boolean;
      isValid: boolean;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      placedPrice: { amount: number; formattedAmount: string };
      extendedPrice: { amount: number; formattedAmount: string };
      discountAmount: { amount: number; formattedAmount: string };
      validationErrors: Array<{
        errorCode: string | null;
        errorMessage: string | null;
        objectType: string | null;
        objectId: string | null;
        errorParameters: Array<{ key: string; value: string } | null> | null;
      }>;
      configurationItems: Array<{
        id: string;
        sectionId: string;
        type: string;
        productId: string | null;
        name: string | null;
        sku: string | null;
        imageUrl: string | null;
        quantity: number | null;
        customText: string | null;
        selectedForCheckout: boolean;
      } | null> | null;
    }>;
    payments: Array<{
      id: string;
      outerId: string | null;
      paymentGatewayCode: string | null;
      currency: { code: string };
      total: { amount: number; formattedAmount: string };
      billingAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    shipments: Array<{
      id: string;
      shipmentMethodCode: string | null;
      shipmentMethodOption: string | null;
      fulfillmentCenterId: string | null;
      price: { amount: number; formattedAmount: string };
      currency: { code: string };
      deliveryAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
    gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
    addresses: Array<{
      id: string | null;
      key: string | null;
      city: string | null;
      countryCode: string | null;
      countryName: string | null;
      email: string | null;
      firstName: string | null;
      middleName: string | null;
      lastName: string | null;
      line1: string | null;
      line2: string | null;
      name: string | null;
      organization: string | null;
      phone: string | null;
      postalCode: string;
      regionId: string | null;
      regionName: string | null;
      zip: string | null;
      outerId: string | null;
      description: string | null;
      addressType: number | null;
    }>;
    validationErrors: Array<{
      errorCode: string | null;
      errorMessage: string | null;
      objectType: string | null;
      objectId: string | null;
      errorParameters: Array<{ key: string; value: string } | null> | null;
    }>;
  } | null;
};

export type ClearCartMutationVariables = Exact<{
  command: InputClearCartType;
}>;

export type ClearCartMutation = {
  clearCart: {
    id: string;
    storeId: string;
    isAnonymous: boolean;
    hasPhysicalProducts: boolean | null;
    customerId: string;
    itemsCount: number;
    itemsQuantity: number;
    total: { amount: number; formattedAmount: string };
    subTotal: { amount: number; formattedAmount: string };
    subTotalDiscount: { amount: number; formattedAmount: string };
    shippingTotal: { amount: number; formattedAmount: string };
    items: Array<{
      id: string;
      sku: string;
      productId: string;
      name: string;
      quantity: number;
      selectedForCheckout: boolean;
      isValid: boolean;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      placedPrice: { amount: number; formattedAmount: string };
      extendedPrice: { amount: number; formattedAmount: string };
      discountAmount: { amount: number; formattedAmount: string };
      validationErrors: Array<{
        errorCode: string | null;
        errorMessage: string | null;
        objectType: string | null;
        objectId: string | null;
        errorParameters: Array<{ key: string; value: string } | null> | null;
      }>;
      configurationItems: Array<{
        id: string;
        sectionId: string;
        type: string;
        productId: string | null;
        name: string | null;
        sku: string | null;
        imageUrl: string | null;
        quantity: number | null;
        customText: string | null;
        selectedForCheckout: boolean;
      } | null> | null;
    }>;
    payments: Array<{
      id: string;
      outerId: string | null;
      paymentGatewayCode: string | null;
      currency: { code: string };
      total: { amount: number; formattedAmount: string };
      billingAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    shipments: Array<{
      id: string;
      shipmentMethodCode: string | null;
      shipmentMethodOption: string | null;
      fulfillmentCenterId: string | null;
      price: { amount: number; formattedAmount: string };
      currency: { code: string };
      deliveryAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
    gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
    addresses: Array<{
      id: string | null;
      key: string | null;
      city: string | null;
      countryCode: string | null;
      countryName: string | null;
      email: string | null;
      firstName: string | null;
      middleName: string | null;
      lastName: string | null;
      line1: string | null;
      line2: string | null;
      name: string | null;
      organization: string | null;
      phone: string | null;
      postalCode: string;
      regionId: string | null;
      regionName: string | null;
      zip: string | null;
      outerId: string | null;
      description: string | null;
      addressType: number | null;
    }>;
    validationErrors: Array<{
      errorCode: string | null;
      errorMessage: string | null;
      objectType: string | null;
      objectId: string | null;
      errorParameters: Array<{ key: string; value: string } | null> | null;
    }>;
  } | null;
};

export type CreateOrderFromCartMutationVariables = Exact<{
  command: InputCreateOrderFromCartType;
}>;

export type CreateOrderFromCartMutation = {
  createOrderFromCart: {
    id: string;
    number: string;
    status: string | null;
    createdDate: string;
    total: { amount: number; formattedAmount: string };
    items: Array<{
      id: string;
      name: string;
      sku: string;
      productId: string;
      quantity: number;
      price: { amount: number; formattedAmount: string };
      extendedPrice: { amount: number; formattedAmount: string };
    }>;
    inPayments: Array<{
      id: string;
      number: string;
      gatewayCode: string | null;
      status: string | null;
      sum: { amount: number; formattedAmount: string };
    }>;
    shipments: Array<{
      id: string;
      number: string;
      shipmentMethodCode: string | null;
      shipmentMethodOption: string | null;
      status: string | null;
      total: { amount: number; formattedAmount: string };
    }>;
  } | null;
};

export type GetCartLineValidationQueryVariables = Exact<{
  storeId: string;
  userId: string;
  currencyCode: string;
  cultureName: string;
  cartId?: string | null | undefined;
}>;

export type GetCartLineValidationQuery = {
  cart: {
    itemsCount: number;
    items: Array<{
      id: string;
      sku: string;
      productId: string;
      quantity: number;
      isValid: boolean;
      validationErrors: Array<{
        errorCode: string | null;
        objectType: string | null;
        objectId: string | null;
        errorMessage: string | null;
      }>;
    }>;
  } | null;
};

export type GetCartValidationAliasedQueryVariables = Exact<{
  storeId: string;
  userId: string;
  currencyCode: string;
  cultureName: string;
  ruleSetA?: string | null | undefined;
  ruleSetB?: string | null | undefined;
  cartId?: string | null | undefined;
}>;

export type GetCartValidationAliasedQuery = {
  cart: {
    itemsCount: number;
    errorsA: Array<{
      errorCode: string | null;
      objectType: string | null;
      objectId: string | null;
      errorMessage: string | null;
    }>;
    errorsB: Array<{
      errorCode: string | null;
      objectType: string | null;
      objectId: string | null;
      errorMessage: string | null;
    }>;
  } | null;
};

export type GetCartValidationQueryVariables = Exact<{
  storeId: string;
  userId: string;
  currencyCode: string;
  cultureName: string;
  ruleSet?: string | null | undefined;
  cartId?: string | null | undefined;
}>;

export type GetCartValidationQuery = {
  cart: {
    itemsCount: number;
    validationErrors: Array<{
      errorCode: string | null;
      objectType: string | null;
      objectId: string | null;
      errorMessage: string | null;
    }>;
    items: Array<{
      id: string;
      sku: string;
      productId: string;
      quantity: number;
      isValid: boolean;
      validationErrors: Array<{
        errorCode: string | null;
        objectType: string | null;
        objectId: string | null;
        errorMessage: string | null;
      }>;
    }>;
  } | null;
};

export type GetCartQueryVariables = Exact<{
  storeId: string;
  userId: string;
  currencyCode: string;
  cultureName: string;
  cartId?: string | null | undefined;
  cartName?: string | null | undefined;
}>;

export type GetCartQuery = {
  cart: {
    id: string;
    storeId: string;
    isAnonymous: boolean;
    hasPhysicalProducts: boolean | null;
    customerId: string;
    itemsCount: number;
    itemsQuantity: number;
    total: { amount: number; formattedAmount: string };
    subTotal: { amount: number; formattedAmount: string };
    subTotalDiscount: { amount: number; formattedAmount: string };
    shippingTotal: { amount: number; formattedAmount: string };
    items: Array<{
      id: string;
      sku: string;
      productId: string;
      name: string;
      quantity: number;
      selectedForCheckout: boolean;
      isValid: boolean;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      placedPrice: { amount: number; formattedAmount: string };
      extendedPrice: { amount: number; formattedAmount: string };
      discountAmount: { amount: number; formattedAmount: string };
      validationErrors: Array<{
        errorCode: string | null;
        errorMessage: string | null;
        objectType: string | null;
        objectId: string | null;
        errorParameters: Array<{ key: string; value: string } | null> | null;
      }>;
      configurationItems: Array<{
        id: string;
        sectionId: string;
        type: string;
        productId: string | null;
        name: string | null;
        sku: string | null;
        imageUrl: string | null;
        quantity: number | null;
        customText: string | null;
        selectedForCheckout: boolean;
      } | null> | null;
    }>;
    payments: Array<{
      id: string;
      outerId: string | null;
      paymentGatewayCode: string | null;
      currency: { code: string };
      total: { amount: number; formattedAmount: string };
      billingAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    shipments: Array<{
      id: string;
      shipmentMethodCode: string | null;
      shipmentMethodOption: string | null;
      fulfillmentCenterId: string | null;
      price: { amount: number; formattedAmount: string };
      currency: { code: string };
      deliveryAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
    gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
    addresses: Array<{
      id: string | null;
      key: string | null;
      city: string | null;
      countryCode: string | null;
      countryName: string | null;
      email: string | null;
      firstName: string | null;
      middleName: string | null;
      lastName: string | null;
      line1: string | null;
      line2: string | null;
      name: string | null;
      organization: string | null;
      phone: string | null;
      postalCode: string;
      regionId: string | null;
      regionName: string | null;
      zip: string | null;
      outerId: string | null;
      description: string | null;
      addressType: number | null;
    }>;
    validationErrors: Array<{
      errorCode: string | null;
      errorMessage: string | null;
      objectType: string | null;
      objectId: string | null;
      errorParameters: Array<{ key: string; value: string } | null> | null;
    }>;
  } | null;
};

export type MergeCartMutationVariables = Exact<{
  command: InputMergeCartType;
}>;

export type MergeCartMutation = {
  mergeCart: {
    id: string;
    storeId: string;
    isAnonymous: boolean;
    hasPhysicalProducts: boolean | null;
    customerId: string;
    itemsCount: number;
    itemsQuantity: number;
    total: { amount: number; formattedAmount: string };
    subTotal: { amount: number; formattedAmount: string };
    subTotalDiscount: { amount: number; formattedAmount: string };
    shippingTotal: { amount: number; formattedAmount: string };
    items: Array<{
      id: string;
      sku: string;
      productId: string;
      name: string;
      quantity: number;
      selectedForCheckout: boolean;
      isValid: boolean;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      placedPrice: { amount: number; formattedAmount: string };
      extendedPrice: { amount: number; formattedAmount: string };
      discountAmount: { amount: number; formattedAmount: string };
      validationErrors: Array<{
        errorCode: string | null;
        errorMessage: string | null;
        objectType: string | null;
        objectId: string | null;
        errorParameters: Array<{ key: string; value: string } | null> | null;
      }>;
      configurationItems: Array<{
        id: string;
        sectionId: string;
        type: string;
        productId: string | null;
        name: string | null;
        sku: string | null;
        imageUrl: string | null;
        quantity: number | null;
        customText: string | null;
        selectedForCheckout: boolean;
      } | null> | null;
    }>;
    payments: Array<{
      id: string;
      outerId: string | null;
      paymentGatewayCode: string | null;
      currency: { code: string };
      total: { amount: number; formattedAmount: string };
      billingAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    shipments: Array<{
      id: string;
      shipmentMethodCode: string | null;
      shipmentMethodOption: string | null;
      fulfillmentCenterId: string | null;
      price: { amount: number; formattedAmount: string };
      currency: { code: string };
      deliveryAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
    gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
    addresses: Array<{
      id: string | null;
      key: string | null;
      city: string | null;
      countryCode: string | null;
      countryName: string | null;
      email: string | null;
      firstName: string | null;
      middleName: string | null;
      lastName: string | null;
      line1: string | null;
      line2: string | null;
      name: string | null;
      organization: string | null;
      phone: string | null;
      postalCode: string;
      regionId: string | null;
      regionName: string | null;
      zip: string | null;
      outerId: string | null;
      description: string | null;
      addressType: number | null;
    }>;
    validationErrors: Array<{
      errorCode: string | null;
      errorMessage: string | null;
      objectType: string | null;
      objectId: string | null;
      errorParameters: Array<{ key: string; value: string } | null> | null;
    }>;
  } | null;
};

export type RemoveCartItemMutationVariables = Exact<{
  command: InputRemoveItemType;
}>;

export type RemoveCartItemMutation = {
  removeCartItem: {
    id: string;
    storeId: string;
    isAnonymous: boolean;
    hasPhysicalProducts: boolean | null;
    customerId: string;
    itemsCount: number;
    itemsQuantity: number;
    total: { amount: number; formattedAmount: string };
    subTotal: { amount: number; formattedAmount: string };
    subTotalDiscount: { amount: number; formattedAmount: string };
    shippingTotal: { amount: number; formattedAmount: string };
    items: Array<{
      id: string;
      sku: string;
      productId: string;
      name: string;
      quantity: number;
      selectedForCheckout: boolean;
      isValid: boolean;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      placedPrice: { amount: number; formattedAmount: string };
      extendedPrice: { amount: number; formattedAmount: string };
      discountAmount: { amount: number; formattedAmount: string };
      validationErrors: Array<{
        errorCode: string | null;
        errorMessage: string | null;
        objectType: string | null;
        objectId: string | null;
        errorParameters: Array<{ key: string; value: string } | null> | null;
      }>;
      configurationItems: Array<{
        id: string;
        sectionId: string;
        type: string;
        productId: string | null;
        name: string | null;
        sku: string | null;
        imageUrl: string | null;
        quantity: number | null;
        customText: string | null;
        selectedForCheckout: boolean;
      } | null> | null;
    }>;
    payments: Array<{
      id: string;
      outerId: string | null;
      paymentGatewayCode: string | null;
      currency: { code: string };
      total: { amount: number; formattedAmount: string };
      billingAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    shipments: Array<{
      id: string;
      shipmentMethodCode: string | null;
      shipmentMethodOption: string | null;
      fulfillmentCenterId: string | null;
      price: { amount: number; formattedAmount: string };
      currency: { code: string };
      deliveryAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
    gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
    addresses: Array<{
      id: string | null;
      key: string | null;
      city: string | null;
      countryCode: string | null;
      countryName: string | null;
      email: string | null;
      firstName: string | null;
      middleName: string | null;
      lastName: string | null;
      line1: string | null;
      line2: string | null;
      name: string | null;
      organization: string | null;
      phone: string | null;
      postalCode: string;
      regionId: string | null;
      regionName: string | null;
      zip: string | null;
      outerId: string | null;
      description: string | null;
      addressType: number | null;
    }>;
    validationErrors: Array<{
      errorCode: string | null;
      errorMessage: string | null;
      objectType: string | null;
      objectId: string | null;
      errorParameters: Array<{ key: string; value: string } | null> | null;
    }>;
  } | null;
};

export type RemoveCartMutationVariables = Exact<{
  command: InputRemoveCartType;
}>;

export type RemoveCartMutation = { removeCart: boolean | null };

export type RemoveCouponMutationVariables = Exact<{
  command: InputRemoveCouponType;
}>;

export type RemoveCouponMutation = {
  removeCoupon: {
    id: string;
    storeId: string;
    isAnonymous: boolean;
    hasPhysicalProducts: boolean | null;
    customerId: string;
    itemsCount: number;
    itemsQuantity: number;
    total: { amount: number; formattedAmount: string };
    subTotal: { amount: number; formattedAmount: string };
    subTotalDiscount: { amount: number; formattedAmount: string };
    shippingTotal: { amount: number; formattedAmount: string };
    items: Array<{
      id: string;
      sku: string;
      productId: string;
      name: string;
      quantity: number;
      selectedForCheckout: boolean;
      isValid: boolean;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      placedPrice: { amount: number; formattedAmount: string };
      extendedPrice: { amount: number; formattedAmount: string };
      discountAmount: { amount: number; formattedAmount: string };
      validationErrors: Array<{
        errorCode: string | null;
        errorMessage: string | null;
        objectType: string | null;
        objectId: string | null;
        errorParameters: Array<{ key: string; value: string } | null> | null;
      }>;
      configurationItems: Array<{
        id: string;
        sectionId: string;
        type: string;
        productId: string | null;
        name: string | null;
        sku: string | null;
        imageUrl: string | null;
        quantity: number | null;
        customText: string | null;
        selectedForCheckout: boolean;
      } | null> | null;
    }>;
    payments: Array<{
      id: string;
      outerId: string | null;
      paymentGatewayCode: string | null;
      currency: { code: string };
      total: { amount: number; formattedAmount: string };
      billingAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    shipments: Array<{
      id: string;
      shipmentMethodCode: string | null;
      shipmentMethodOption: string | null;
      fulfillmentCenterId: string | null;
      price: { amount: number; formattedAmount: string };
      currency: { code: string };
      deliveryAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
    gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
    addresses: Array<{
      id: string | null;
      key: string | null;
      city: string | null;
      countryCode: string | null;
      countryName: string | null;
      email: string | null;
      firstName: string | null;
      middleName: string | null;
      lastName: string | null;
      line1: string | null;
      line2: string | null;
      name: string | null;
      organization: string | null;
      phone: string | null;
      postalCode: string;
      regionId: string | null;
      regionName: string | null;
      zip: string | null;
      outerId: string | null;
      description: string | null;
      addressType: number | null;
    }>;
    validationErrors: Array<{
      errorCode: string | null;
      errorMessage: string | null;
      objectType: string | null;
      objectId: string | null;
      errorParameters: Array<{ key: string; value: string } | null> | null;
    }>;
  } | null;
};

export type SelectCartItemsMutationVariables = Exact<{
  command: InputChangeCartItemsSelectedType;
}>;

export type SelectCartItemsMutation = {
  selectCartItems: {
    id: string;
    storeId: string;
    isAnonymous: boolean;
    hasPhysicalProducts: boolean | null;
    customerId: string;
    itemsCount: number;
    itemsQuantity: number;
    total: { amount: number; formattedAmount: string };
    subTotal: { amount: number; formattedAmount: string };
    subTotalDiscount: { amount: number; formattedAmount: string };
    shippingTotal: { amount: number; formattedAmount: string };
    items: Array<{
      id: string;
      sku: string;
      productId: string;
      name: string;
      quantity: number;
      selectedForCheckout: boolean;
      isValid: boolean;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      placedPrice: { amount: number; formattedAmount: string };
      extendedPrice: { amount: number; formattedAmount: string };
      discountAmount: { amount: number; formattedAmount: string };
      validationErrors: Array<{
        errorCode: string | null;
        errorMessage: string | null;
        objectType: string | null;
        objectId: string | null;
        errorParameters: Array<{ key: string; value: string } | null> | null;
      }>;
      configurationItems: Array<{
        id: string;
        sectionId: string;
        type: string;
        productId: string | null;
        name: string | null;
        sku: string | null;
        imageUrl: string | null;
        quantity: number | null;
        customText: string | null;
        selectedForCheckout: boolean;
      } | null> | null;
    }>;
    payments: Array<{
      id: string;
      outerId: string | null;
      paymentGatewayCode: string | null;
      currency: { code: string };
      total: { amount: number; formattedAmount: string };
      billingAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    shipments: Array<{
      id: string;
      shipmentMethodCode: string | null;
      shipmentMethodOption: string | null;
      fulfillmentCenterId: string | null;
      price: { amount: number; formattedAmount: string };
      currency: { code: string };
      deliveryAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
    gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
    addresses: Array<{
      id: string | null;
      key: string | null;
      city: string | null;
      countryCode: string | null;
      countryName: string | null;
      email: string | null;
      firstName: string | null;
      middleName: string | null;
      lastName: string | null;
      line1: string | null;
      line2: string | null;
      name: string | null;
      organization: string | null;
      phone: string | null;
      postalCode: string;
      regionId: string | null;
      regionName: string | null;
      zip: string | null;
      outerId: string | null;
      description: string | null;
      addressType: number | null;
    }>;
    validationErrors: Array<{
      errorCode: string | null;
      errorMessage: string | null;
      objectType: string | null;
      objectId: string | null;
      errorParameters: Array<{ key: string; value: string } | null> | null;
    }>;
  } | null;
};

export type UnSelectAllCartItemsMutationVariables = Exact<{
  command: InputChangeAllCartItemsSelectedType;
}>;

export type UnSelectAllCartItemsMutation = {
  unSelectAllCartItems: {
    id: string;
    storeId: string;
    isAnonymous: boolean;
    hasPhysicalProducts: boolean | null;
    customerId: string;
    itemsCount: number;
    itemsQuantity: number;
    total: { amount: number; formattedAmount: string };
    subTotal: { amount: number; formattedAmount: string };
    subTotalDiscount: { amount: number; formattedAmount: string };
    shippingTotal: { amount: number; formattedAmount: string };
    items: Array<{
      id: string;
      sku: string;
      productId: string;
      name: string;
      quantity: number;
      selectedForCheckout: boolean;
      isValid: boolean;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      placedPrice: { amount: number; formattedAmount: string };
      extendedPrice: { amount: number; formattedAmount: string };
      discountAmount: { amount: number; formattedAmount: string };
      validationErrors: Array<{
        errorCode: string | null;
        errorMessage: string | null;
        objectType: string | null;
        objectId: string | null;
        errorParameters: Array<{ key: string; value: string } | null> | null;
      }>;
      configurationItems: Array<{
        id: string;
        sectionId: string;
        type: string;
        productId: string | null;
        name: string | null;
        sku: string | null;
        imageUrl: string | null;
        quantity: number | null;
        customText: string | null;
        selectedForCheckout: boolean;
      } | null> | null;
    }>;
    payments: Array<{
      id: string;
      outerId: string | null;
      paymentGatewayCode: string | null;
      currency: { code: string };
      total: { amount: number; formattedAmount: string };
      billingAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    shipments: Array<{
      id: string;
      shipmentMethodCode: string | null;
      shipmentMethodOption: string | null;
      fulfillmentCenterId: string | null;
      price: { amount: number; formattedAmount: string };
      currency: { code: string };
      deliveryAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
    gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
    addresses: Array<{
      id: string | null;
      key: string | null;
      city: string | null;
      countryCode: string | null;
      countryName: string | null;
      email: string | null;
      firstName: string | null;
      middleName: string | null;
      lastName: string | null;
      line1: string | null;
      line2: string | null;
      name: string | null;
      organization: string | null;
      phone: string | null;
      postalCode: string;
      regionId: string | null;
      regionName: string | null;
      zip: string | null;
      outerId: string | null;
      description: string | null;
      addressType: number | null;
    }>;
    validationErrors: Array<{
      errorCode: string | null;
      errorMessage: string | null;
      objectType: string | null;
      objectId: string | null;
      errorParameters: Array<{ key: string; value: string } | null> | null;
    }>;
  } | null;
};

export type UnSelectCartItemsMutationVariables = Exact<{
  command: InputChangeCartItemsSelectedType;
}>;

export type UnSelectCartItemsMutation = {
  unSelectCartItems: {
    id: string;
    storeId: string;
    isAnonymous: boolean;
    hasPhysicalProducts: boolean | null;
    customerId: string;
    itemsCount: number;
    itemsQuantity: number;
    total: { amount: number; formattedAmount: string };
    subTotal: { amount: number; formattedAmount: string };
    subTotalDiscount: { amount: number; formattedAmount: string };
    shippingTotal: { amount: number; formattedAmount: string };
    items: Array<{
      id: string;
      sku: string;
      productId: string;
      name: string;
      quantity: number;
      selectedForCheckout: boolean;
      isValid: boolean;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      placedPrice: { amount: number; formattedAmount: string };
      extendedPrice: { amount: number; formattedAmount: string };
      discountAmount: { amount: number; formattedAmount: string };
      validationErrors: Array<{
        errorCode: string | null;
        errorMessage: string | null;
        objectType: string | null;
        objectId: string | null;
        errorParameters: Array<{ key: string; value: string } | null> | null;
      }>;
      configurationItems: Array<{
        id: string;
        sectionId: string;
        type: string;
        productId: string | null;
        name: string | null;
        sku: string | null;
        imageUrl: string | null;
        quantity: number | null;
        customText: string | null;
        selectedForCheckout: boolean;
      } | null> | null;
    }>;
    payments: Array<{
      id: string;
      outerId: string | null;
      paymentGatewayCode: string | null;
      currency: { code: string };
      total: { amount: number; formattedAmount: string };
      billingAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    shipments: Array<{
      id: string;
      shipmentMethodCode: string | null;
      shipmentMethodOption: string | null;
      fulfillmentCenterId: string | null;
      price: { amount: number; formattedAmount: string };
      currency: { code: string };
      deliveryAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
    gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
    addresses: Array<{
      id: string | null;
      key: string | null;
      city: string | null;
      countryCode: string | null;
      countryName: string | null;
      email: string | null;
      firstName: string | null;
      middleName: string | null;
      lastName: string | null;
      line1: string | null;
      line2: string | null;
      name: string | null;
      organization: string | null;
      phone: string | null;
      postalCode: string;
      regionId: string | null;
      regionName: string | null;
      zip: string | null;
      outerId: string | null;
      description: string | null;
      addressType: number | null;
    }>;
    validationErrors: Array<{
      errorCode: string | null;
      errorMessage: string | null;
      objectType: string | null;
      objectId: string | null;
      errorParameters: Array<{ key: string; value: string } | null> | null;
    }>;
  } | null;
};

export type UpdateCartQuantityMutationVariables = Exact<{
  command: InputUpdateCartQuantity;
}>;

export type UpdateCartQuantityMutation = {
  updateCartQuantity: {
    id: string;
    storeId: string;
    isAnonymous: boolean;
    hasPhysicalProducts: boolean | null;
    customerId: string;
    itemsCount: number;
    itemsQuantity: number;
    total: { amount: number; formattedAmount: string };
    subTotal: { amount: number; formattedAmount: string };
    subTotalDiscount: { amount: number; formattedAmount: string };
    shippingTotal: { amount: number; formattedAmount: string };
    items: Array<{
      id: string;
      sku: string;
      productId: string;
      name: string;
      quantity: number;
      selectedForCheckout: boolean;
      isValid: boolean;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      placedPrice: { amount: number; formattedAmount: string };
      extendedPrice: { amount: number; formattedAmount: string };
      discountAmount: { amount: number; formattedAmount: string };
      validationErrors: Array<{
        errorCode: string | null;
        errorMessage: string | null;
        objectType: string | null;
        objectId: string | null;
        errorParameters: Array<{ key: string; value: string } | null> | null;
      }>;
      configurationItems: Array<{
        id: string;
        sectionId: string;
        type: string;
        productId: string | null;
        name: string | null;
        sku: string | null;
        imageUrl: string | null;
        quantity: number | null;
        customText: string | null;
        selectedForCheckout: boolean;
      } | null> | null;
    }>;
    payments: Array<{
      id: string;
      outerId: string | null;
      paymentGatewayCode: string | null;
      currency: { code: string };
      total: { amount: number; formattedAmount: string };
      billingAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    shipments: Array<{
      id: string;
      shipmentMethodCode: string | null;
      shipmentMethodOption: string | null;
      fulfillmentCenterId: string | null;
      price: { amount: number; formattedAmount: string };
      currency: { code: string };
      deliveryAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
    gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
    addresses: Array<{
      id: string | null;
      key: string | null;
      city: string | null;
      countryCode: string | null;
      countryName: string | null;
      email: string | null;
      firstName: string | null;
      middleName: string | null;
      lastName: string | null;
      line1: string | null;
      line2: string | null;
      name: string | null;
      organization: string | null;
      phone: string | null;
      postalCode: string;
      regionId: string | null;
      regionName: string | null;
      zip: string | null;
      outerId: string | null;
      description: string | null;
      addressType: number | null;
    }>;
    validationErrors: Array<{
      errorCode: string | null;
      errorMessage: string | null;
      objectType: string | null;
      objectId: string | null;
      errorParameters: Array<{ key: string; value: string } | null> | null;
    }>;
  } | null;
};

export type CategoriesQueryVariables = Exact<{
  storeId: string;
  userId?: string | null | undefined;
  cultureName?: string | null | undefined;
  currencyCode?: string | null | undefined;
  filter?: string | null | undefined;
  first?: number | null | undefined;
}>;

export type CategoriesQuery = {
  categories: {
    totalCount: number | null;
    items: Array<{ id: string; code: string; name: string; outline: string | null; slug: string | null } | null> | null;
  } | null;
};

export type CategoryQueryVariables = Exact<{
  id: string;
  storeId: string;
  userId?: string | null | undefined;
  cultureName?: string | null | undefined;
  currencyCode?: string | null | undefined;
}>;

export type CategoryQuery = {
  category: { id: string; code: string; name: string; outline: string | null; slug: string | null } | null;
};

export type AddAddressToFavoritesMutationVariables = Exact<{
  command: AddAddressToFavoritesCommandType;
}>;

export type AddAddressToFavoritesMutation = { addAddressToFavorites: boolean | null };

export type ChangeOrganizationContactRoleMutationVariables = Exact<{
  command: InputChangeOrganizationContactRoleType;
}>;

export type ChangeOrganizationContactRoleMutation = {
  changeOrganizationContactRole: {
    succeeded: boolean;
    errors: Array<{ code: string; parameter: string | null; description: string | null } | null> | null;
  } | null;
};

export type DeleteContactMutationVariables = Exact<{
  command: InputDeleteContactType;
}>;

export type DeleteContactMutation = { deleteContact: boolean | null };

export type DeleteMemberAddressesMutationVariables = Exact<{
  command: InputDeleteMemberAddressType;
}>;

export type DeleteMemberAddressesMutation = {
  deleteMemberAddresses: {
    addresses: {
      items: Array<{
        id: string | null;
        key: string | null;
        isDefault: boolean;
        isFavorite: boolean;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null> | null;
    } | null;
  } | null;
};

export type GetContactAddressesQueryVariables = Exact<{
  id: string;
}>;

export type GetContactAddressesQuery = {
  contact: {
    addresses: {
      items: Array<{
        id: string | null;
        key: string | null;
        isDefault: boolean;
        isFavorite: boolean;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null> | null;
    } | null;
  } | null;
};

export type GetContactLockStatusQueryVariables = Exact<{
  id: string;
}>;

export type GetContactLockStatusQuery = { contact: { isLockedInOrganization: boolean | null } | null };

export type GetContactRolesInOrganizationQueryVariables = Exact<{
  id: string;
}>;

export type GetContactRolesInOrganizationQuery = {
  contact: { rolesInOrganization: Array<{ id: string; name: string } | null> | null } | null;
};

export type GetContactQueryVariables = Exact<{
  id: string;
}>;

export type GetContactQuery = {
  contact: {
    id: string;
    firstName: string;
    lastName: string;
    fullName: string;
    status: string | null;
    organizationId: string | null;
    organizationsIds: Array<string | null> | null;
    securityAccounts: Array<{
      id: string;
      userName: string;
      email: string | null;
      emailConfirmed: boolean;
      isAdministrator: boolean;
      memberId: string | null;
      storeId: string | null;
      roles: Array<{ id: string; name: string; normalizedName: string } | null> | null;
    } | null> | null;
  } | null;
};

export type GetCurrentCustomerAddressesQueryVariables = Exact<{
  after?: string | null | undefined;
  first?: number | null | undefined;
  countryCodes?: Array<string | null | undefined> | string | null | undefined;
  regionIds?: Array<string | null | undefined> | string | null | undefined;
  cities?: Array<string | null | undefined> | string | null | undefined;
  keyword?: string | null | undefined;
  sort?: string | null | undefined;
}>;

export type GetCurrentCustomerAddressesQuery = {
  currentCustomerAddresses: {
    totalCount: number | null;
    items: Array<{
      id: string | null;
      key: string | null;
      isDefault: boolean;
      isFavorite: boolean;
      city: string | null;
      countryCode: string | null;
      countryName: string | null;
      email: string | null;
      firstName: string | null;
      middleName: string | null;
      lastName: string | null;
      line1: string | null;
      line2: string | null;
      name: string | null;
      organization: string | null;
      phone: string | null;
      postalCode: string;
      regionId: string | null;
      regionName: string | null;
      zip: string | null;
      outerId: string | null;
      description: string | null;
      addressType: number | null;
    } | null> | null;
  } | null;
};

export type GetCurrentOrganizationAddressesQueryVariables = Exact<{
  after?: string | null | undefined;
  first?: number | null | undefined;
  countryCodes?: Array<string | null | undefined> | string | null | undefined;
  regionIds?: Array<string | null | undefined> | string | null | undefined;
  cities?: Array<string | null | undefined> | string | null | undefined;
  keyword?: string | null | undefined;
  sort?: string | null | undefined;
}>;

export type GetCurrentOrganizationAddressesQuery = {
  currentOrganizationAddresses: {
    totalCount: number | null;
    items: Array<{
      id: string | null;
      key: string | null;
      isDefault: boolean;
      isFavorite: boolean;
      city: string | null;
      countryCode: string | null;
      countryName: string | null;
      email: string | null;
      firstName: string | null;
      middleName: string | null;
      lastName: string | null;
      line1: string | null;
      line2: string | null;
      name: string | null;
      organization: string | null;
      phone: string | null;
      postalCode: string;
      regionId: string | null;
      regionName: string | null;
      zip: string | null;
      outerId: string | null;
      description: string | null;
      addressType: number | null;
    } | null> | null;
  } | null;
};

export type GetOrganizationContactsQueryVariables = Exact<{
  organizationId: string;
  searchPhrase?: string | null | undefined;
  sort?: string | null | undefined;
  first?: number | null | undefined;
  after?: string | null | undefined;
}>;

export type GetOrganizationContactsQuery = {
  organization: {
    contacts: {
      items: Array<{
        id: string;
        firstName: string;
        lastName: string;
        fullName: string;
        status: string | null;
        organizationId: string | null;
        organizationsIds: Array<string | null> | null;
        securityAccounts: Array<{
          id: string;
          userName: string;
          email: string | null;
          emailConfirmed: boolean;
          isAdministrator: boolean;
          memberId: string | null;
          storeId: string | null;
          roles: Array<{ id: string; name: string; normalizedName: string } | null> | null;
        } | null> | null;
      } | null> | null;
    } | null;
  } | null;
};

export type GetOrganizationsQueryVariables = Exact<{
  after?: string | null | undefined;
  first?: number | null | undefined;
  sort?: string | null | undefined;
  searchPhrase?: string | null | undefined;
  statuses?: Array<string | null | undefined> | string | null | undefined;
}>;

export type GetOrganizationsQuery = {
  me: {
    contact: {
      organizations: {
        totalCount: number | null;
        items: Array<{ id: string; name: string | null; isLockedForCurrentUser: boolean | null } | null> | null;
        pageInfo: { hasNextPage: boolean; endCursor: string | null };
      } | null;
    } | null;
  } | null;
};

export type LockOrganizationContactMutationVariables = Exact<{
  command: InputLockUnlockOrganizationContactType;
}>;

export type LockOrganizationContactMutation = {
  lockOrganizationContact: {
    id: string;
    firstName: string;
    lastName: string;
    fullName: string;
    status: string | null;
    organizationId: string | null;
    organizationsIds: Array<string | null> | null;
    securityAccounts: Array<{
      id: string;
      userName: string;
      email: string | null;
      emailConfirmed: boolean;
      isAdministrator: boolean;
      memberId: string | null;
      storeId: string | null;
      roles: Array<{ id: string; name: string; normalizedName: string } | null> | null;
    } | null> | null;
  } | null;
};

export type RemoveAddressFromFavoritesMutationVariables = Exact<{
  command: RemoveAddressFromFavoritesCommandType;
}>;

export type RemoveAddressFromFavoritesMutation = { removeAddressFromFavorites: boolean | null };

export type RequestRegistrationMutationVariables = Exact<{
  command: InputRequestRegistrationType;
}>;

export type RequestRegistrationMutation = {
  requestRegistration: {
    contact: { id: string; firstName: string; lastName: string; status: string | null } | null;
    organization: { id: string; name: string; status: string | null; ownerId: string | null } | null;
    account: { id: string; username: string; email: string; status: string | null } | null;
    result: { succeeded: boolean; requireEmailVerification: boolean } | null;
  } | null;
};

export type UnlockOrganizationContactMutationVariables = Exact<{
  command: InputLockUnlockOrganizationContactType;
}>;

export type UnlockOrganizationContactMutation = {
  unlockOrganizationContact: {
    id: string;
    firstName: string;
    lastName: string;
    fullName: string;
    status: string | null;
    organizationId: string | null;
    organizationsIds: Array<string | null> | null;
    securityAccounts: Array<{
      id: string;
      userName: string;
      email: string | null;
      emailConfirmed: boolean;
      isAdministrator: boolean;
      memberId: string | null;
      storeId: string | null;
      roles: Array<{ id: string; name: string; normalizedName: string } | null> | null;
    } | null> | null;
  } | null;
};

export type UpdateMemberAddressesMutationVariables = Exact<{
  command: InputUpdateMemberAddressType;
}>;

export type UpdateMemberAddressesMutation = {
  updateMemberAddresses: {
    addresses: {
      items: Array<{
        id: string | null;
        key: string | null;
        isDefault: boolean;
        isFavorite: boolean;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null> | null;
    } | null;
  } | null;
};

export type OrderQueryVariables = Exact<{
  number?: string | null | undefined;
  cultureName?: string | null | undefined;
}>;

export type OrderQuery = {
  order: {
    id: string;
    number: string;
    status: string | null;
    createdDate: string;
    total: { amount: number; formattedAmount: string };
    items: Array<{
      id: string;
      name: string;
      sku: string;
      productId: string;
      quantity: number;
      price: { amount: number; formattedAmount: string };
      extendedPrice: { amount: number; formattedAmount: string };
    }>;
    inPayments: Array<{
      id: string;
      number: string;
      gatewayCode: string | null;
      status: string | null;
      sum: { amount: number; formattedAmount: string };
    }>;
    shipments: Array<{
      id: string;
      number: string;
      shipmentMethodCode: string | null;
      shipmentMethodOption: string | null;
      status: string | null;
      total: { amount: number; formattedAmount: string };
    }>;
  } | null;
};

export type OrdersQueryVariables = Exact<{
  userId?: string | null | undefined;
  filter?: string | null | undefined;
  sort?: string | null | undefined;
  cultureName?: string | null | undefined;
  first?: number | null | undefined;
  after?: string | null | undefined;
}>;

export type OrdersQuery = {
  orders: {
    items: Array<{
      id: string;
      number: string;
      status: string | null;
      createdDate: string;
      total: { amount: number; formattedAmount: string };
      items: Array<{
        id: string;
        name: string;
        sku: string;
        productId: string;
        quantity: number;
        price: { amount: number; formattedAmount: string };
        extendedPrice: { amount: number; formattedAmount: string };
      }>;
      inPayments: Array<{
        id: string;
        number: string;
        gatewayCode: string | null;
        status: string | null;
        sum: { amount: number; formattedAmount: string };
      }>;
      shipments: Array<{
        id: string;
        number: string;
        shipmentMethodCode: string | null;
        shipmentMethodOption: string | null;
        status: string | null;
        total: { amount: number; formattedAmount: string };
      }>;
    } | null> | null;
  } | null;
};

export type OrganizationOrdersQueryVariables = Exact<{
  organizationId?: string | null | undefined;
  filter?: string | null | undefined;
  sort?: string | null | undefined;
  cultureName?: string | null | undefined;
  first?: number | null | undefined;
  after?: string | null | undefined;
}>;

export type OrganizationOrdersQuery = {
  organizationOrders: {
    items: Array<{
      id: string;
      number: string;
      status: string | null;
      createdDate: string;
      total: { amount: number; formattedAmount: string };
      items: Array<{
        id: string;
        name: string;
        sku: string;
        productId: string;
        quantity: number;
        price: { amount: number; formattedAmount: string };
        extendedPrice: { amount: number; formattedAmount: string };
      }>;
      inPayments: Array<{
        id: string;
        number: string;
        gatewayCode: string | null;
        status: string | null;
        sum: { amount: number; formattedAmount: string };
      }>;
      shipments: Array<{
        id: string;
        number: string;
        shipmentMethodCode: string | null;
        shipmentMethodOption: string | null;
        status: string | null;
        total: { amount: number; formattedAmount: string };
      }>;
    } | null> | null;
  } | null;
};

export type PageContextQueryVariables = Exact<{
  storeId?: string | null | undefined;
  userId?: string | null | undefined;
  cultureName?: string | null | undefined;
  permalink?: string | null | undefined;
  organizationId?: string | null | undefined;
}>;

export type PageContextQuery = {
  pageContext: {
    slugInfo: {
      redirectUrl: string | null;
      entityInfo: {
        id: string;
        name: string | null;
        semanticUrl: string;
        outline: string | null;
        pageTitle: string | null;
        metaDescription: string | null;
        imageAltDescription: string | null;
        metaKeywords: string | null;
        storeId: string | null;
        objectId: string;
        objectType: string;
        isActive: boolean;
        languageCode: string | null;
      } | null;
    } | null;
    store: {
      storeId: string;
      storeName: string;
      catalogId: string;
      storeUrl: string | null;
      defaultLanguage: { cultureName: string; nativeName: string };
      availableLanguages: Array<{ cultureName: string; nativeName: string }>;
      defaultCurrency: { code: string };
      availableCurrencies: Array<{ code: string }>;
      settings: { anonymousUsersAllowed: boolean; taxCalculationEnabled: boolean; seoLinkType: string };
    } | null;
    whiteLabelingSettings: {
      logoUrl: string | null;
      secondaryLogoUrl: string | null;
      faviconUrl: string | null;
      themePresetName: string | null;
      footerLinks: Array<{ title: string; url: string; priority: number } | null> | null;
      mainMenuLinks: Array<{ title: string; url: string; priority: number } | null> | null;
    } | null;
    user: {
      id: string;
      userName: string;
      email: string | null;
      emailConfirmed: boolean;
      isAdministrator: boolean;
      memberId: string | null;
      storeId: string | null;
      roles: Array<{ id: string; name: string; normalizedName: string } | null> | null;
    } | null;
  } | null;
};

export type CartPickupLocationsQueryVariables = Exact<{
  cartId: string;
  storeId: string;
  cultureName: string;
  keyword?: string | null | undefined;
  sort?: string | null | undefined;
  first?: number | null | undefined;
  after?: string | null | undefined;
  facet?: string | null | undefined;
  filter?: string | null | undefined;
}>;

export type CartPickupLocationsQuery = {
  cartPickupLocations: {
    items: Array<{
      id: string;
      isActive: boolean;
      name: string;
      description: string | null;
      contactEmail: string | null;
      contactPhone: string | null;
      workingHours: string | null;
      deliveryDays: number | null;
      storageDays: number | null;
      geoLocation: string | null;
      availabilityType: ProductPickupAvailabilityType | null;
      availabilityNote: string | null;
      availableQuantity: number | null;
      address: {
        id: string;
        key: string | null;
        name: string | null;
        organization: string | null;
        countryCode: string | null;
        countryName: string | null;
        city: string | null;
        postalCode: string | null;
        line1: string | null;
        line2: string | null;
        regionId: string | null;
        regionName: string | null;
        phone: string | null;
        email: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    } | null> | null;
  } | null;
};

export type PickupLocationsQueryVariables = Exact<{
  storeId?: string | null | undefined;
  keyword?: string | null | undefined;
  sort?: string | null | undefined;
  first?: number | null | undefined;
  after?: string | null | undefined;
}>;

export type PickupLocationsQuery = {
  pickupLocations: {
    items: Array<{
      id: string;
      isActive: boolean;
      name: string;
      description: string | null;
      contactEmail: string | null;
      contactPhone: string | null;
      workingHours: string | null;
      geoLocation: string | null;
      address: {
        id: string;
        key: string | null;
        name: string | null;
        organization: string | null;
        countryCode: string | null;
        countryName: string | null;
        city: string | null;
        postalCode: string | null;
        line1: string | null;
        line2: string | null;
        regionId: string | null;
        regionName: string | null;
        phone: string | null;
        email: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    } | null> | null;
  } | null;
};

export type ProductPickupLocationsQueryVariables = Exact<{
  productId: string;
  storeId: string;
  cultureName: string;
  keyword?: string | null | undefined;
  sort?: string | null | undefined;
  first?: number | null | undefined;
  after?: string | null | undefined;
}>;

export type ProductPickupLocationsQuery = {
  productPickupLocations: {
    items: Array<{
      id: string;
      isActive: boolean;
      name: string;
      description: string | null;
      contactEmail: string | null;
      contactPhone: string | null;
      workingHours: string | null;
      deliveryDays: number | null;
      storageDays: number | null;
      geoLocation: string | null;
      availabilityType: ProductPickupAvailabilityType | null;
      availabilityNote: string | null;
      availableQuantity: number | null;
      address: {
        id: string;
        key: string | null;
        name: string | null;
        organization: string | null;
        countryCode: string | null;
        countryName: string | null;
        city: string | null;
        postalCode: string | null;
        line1: string | null;
        line2: string | null;
        regionId: string | null;
        regionName: string | null;
        phone: string | null;
        email: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    } | null> | null;
  } | null;
};

export type CreateConfiguredLineItemMutationVariables = Exact<{
  command: InputCreateConfiguredLineItemCommand;
}>;

export type CreateConfiguredLineItemMutation = {
  createConfiguredLineItem: {
    id: string | null;
    text: string | null;
    quantity: number;
    product: {
      id: string;
      code: string;
      productType: string | null;
      isConfigurable: boolean;
      name: string;
      vendor: { id: string; name: string } | null;
      price: { list: { amount: number; formattedAmount: string }; actual: { amount: number; formattedAmount: string } };
    } | null;
    listPrice: { amount: number; formattedAmount: string } | null;
    salePrice: { amount: number; formattedAmount: string } | null;
    extendedPrice: { amount: number; formattedAmount: string } | null;
    discountAmount: { amount: number; formattedAmount: string } | null;
  } | null;
};

export type ProductConfigurationQueryVariables = Exact<{
  configurableProductId: string;
  storeId: string;
  userId?: string | null | undefined;
  cultureName?: string | null | undefined;
  currencyCode?: string | null | undefined;
}>;

export type ProductConfigurationQuery = {
  productConfiguration: {
    configurationSections: Array<{
      id: string;
      name: string | null;
      description: string | null;
      isRequired: boolean;
      type: string;
      allowCustomText: boolean;
      allowTextOptions: boolean;
      maxLength: number | null;
      options: Array<{
        id: string | null;
        text: string | null;
        quantity: number;
        product: {
          id: string;
          code: string;
          productType: string | null;
          isConfigurable: boolean;
          name: string;
          vendor: { id: string; name: string } | null;
          price: {
            list: { amount: number; formattedAmount: string };
            actual: { amount: number; formattedAmount: string };
          };
        } | null;
        listPrice: { amount: number; formattedAmount: string } | null;
        salePrice: { amount: number; formattedAmount: string } | null;
        extendedPrice: { amount: number; formattedAmount: string } | null;
        discountAmount: { amount: number; formattedAmount: string } | null;
      } | null> | null;
    } | null> | null;
  } | null;
};

export type ProductQueryVariables = Exact<{
  id: string;
  storeId: string;
  userId?: string | null | undefined;
  cultureName?: string | null | undefined;
  currencyCode?: string | null | undefined;
}>;

export type ProductQuery = {
  product: {
    id: string;
    code: string;
    productType: string | null;
    isConfigurable: boolean;
    name: string;
    vendor: { id: string; name: string } | null;
    price: { list: { amount: number; formattedAmount: string }; actual: { amount: number; formattedAmount: string } };
  } | null;
};

export type ProductsQueryVariables = Exact<{
  storeId: string;
  userId?: string | null | undefined;
  cultureName?: string | null | undefined;
  currencyCode?: string | null | undefined;
  query?: string | null | undefined;
  filter?: string | null | undefined;
  sort?: string | null | undefined;
  first?: number | null | undefined;
  after?: string | null | undefined;
}>;

export type ProductsQuery = {
  products: {
    items: Array<{
      id: string;
      code: string;
      productType: string | null;
      isConfigurable: boolean;
      name: string;
      vendor: { id: string; name: string } | null;
      price: { list: { amount: number; formattedAmount: string }; actual: { amount: number; formattedAmount: string } };
    } | null> | null;
  } | null;
};

export type CancelQuoteRequestMutationVariables = Exact<{
  command: CancelQuoteCommandType;
}>;

export type CancelQuoteRequestMutation = {
  cancelQuoteRequest: {
    id: string;
    number: string;
    status: string | null;
    storeId: string;
    customerId: string | null;
    comment: string | null;
    isAnonymous: boolean;
    isCancelled: boolean;
    totals: {
      originalSubTotalExlTax: { amount: number; formattedAmount: string };
      subTotalExlTax: { amount: number; formattedAmount: string };
      shippingTotal: { amount: number; formattedAmount: string };
      discountTotal: { amount: number; formattedAmount: string };
      taxTotal: { amount: number; formattedAmount: string };
      grandTotalExlTax: { amount: number; formattedAmount: string };
      grandTotalInclTax: { amount: number; formattedAmount: string };
    };
    items: Array<{
      id: string;
      name: string;
      sku: string | null;
      productId: string | null;
      quantity: number;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      proposalPrices: Array<{ quantity: number; price: { amount: number; formattedAmount: string } }>;
    }>;
  } | null;
};

export type ChangeQuoteCommentMutationVariables = Exact<{
  command: ChangeQuoteCommentCommandType;
}>;

export type ChangeQuoteCommentMutation = {
  changeQuoteComment: {
    id: string;
    number: string;
    status: string | null;
    storeId: string;
    customerId: string | null;
    comment: string | null;
    isAnonymous: boolean;
    isCancelled: boolean;
    totals: {
      originalSubTotalExlTax: { amount: number; formattedAmount: string };
      subTotalExlTax: { amount: number; formattedAmount: string };
      shippingTotal: { amount: number; formattedAmount: string };
      discountTotal: { amount: number; formattedAmount: string };
      taxTotal: { amount: number; formattedAmount: string };
      grandTotalExlTax: { amount: number; formattedAmount: string };
      grandTotalInclTax: { amount: number; formattedAmount: string };
    };
    items: Array<{
      id: string;
      name: string;
      sku: string | null;
      productId: string | null;
      quantity: number;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      proposalPrices: Array<{ quantity: number; price: { amount: number; formattedAmount: string } }>;
    }>;
  } | null;
};

export type ChangeQuoteItemQuantityMutationVariables = Exact<{
  command: ChangeQuoteItemQuantityCommandType;
}>;

export type ChangeQuoteItemQuantityMutation = {
  changeQuoteItemQuantity: {
    id: string;
    number: string;
    status: string | null;
    storeId: string;
    customerId: string | null;
    comment: string | null;
    isAnonymous: boolean;
    isCancelled: boolean;
    totals: {
      originalSubTotalExlTax: { amount: number; formattedAmount: string };
      subTotalExlTax: { amount: number; formattedAmount: string };
      shippingTotal: { amount: number; formattedAmount: string };
      discountTotal: { amount: number; formattedAmount: string };
      taxTotal: { amount: number; formattedAmount: string };
      grandTotalExlTax: { amount: number; formattedAmount: string };
      grandTotalInclTax: { amount: number; formattedAmount: string };
    };
    items: Array<{
      id: string;
      name: string;
      sku: string | null;
      productId: string | null;
      quantity: number;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      proposalPrices: Array<{ quantity: number; price: { amount: number; formattedAmount: string } }>;
    }>;
  } | null;
};

export type CreateQuoteFromCartMutationVariables = Exact<{
  command: CreateQuoteFromCartCommandType;
}>;

export type CreateQuoteFromCartMutation = {
  createQuoteFromCart: {
    id: string;
    number: string;
    status: string | null;
    storeId: string;
    customerId: string | null;
    comment: string | null;
    isAnonymous: boolean;
    isCancelled: boolean;
    totals: {
      originalSubTotalExlTax: { amount: number; formattedAmount: string };
      subTotalExlTax: { amount: number; formattedAmount: string };
      shippingTotal: { amount: number; formattedAmount: string };
      discountTotal: { amount: number; formattedAmount: string };
      taxTotal: { amount: number; formattedAmount: string };
      grandTotalExlTax: { amount: number; formattedAmount: string };
      grandTotalInclTax: { amount: number; formattedAmount: string };
    };
    items: Array<{
      id: string;
      name: string;
      sku: string | null;
      productId: string | null;
      quantity: number;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      proposalPrices: Array<{ quantity: number; price: { amount: number; formattedAmount: string } }>;
    }>;
  } | null;
};

export type CreateQuoteMutationVariables = Exact<{
  command: CreateQuoteCommandType;
}>;

export type CreateQuoteMutation = {
  createQuote: {
    id: string;
    number: string;
    status: string | null;
    storeId: string;
    customerId: string | null;
    comment: string | null;
    isAnonymous: boolean;
    isCancelled: boolean;
    totals: {
      originalSubTotalExlTax: { amount: number; formattedAmount: string };
      subTotalExlTax: { amount: number; formattedAmount: string };
      shippingTotal: { amount: number; formattedAmount: string };
      discountTotal: { amount: number; formattedAmount: string };
      taxTotal: { amount: number; formattedAmount: string };
      grandTotalExlTax: { amount: number; formattedAmount: string };
      grandTotalInclTax: { amount: number; formattedAmount: string };
    };
    items: Array<{
      id: string;
      name: string;
      sku: string | null;
      productId: string | null;
      quantity: number;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      proposalPrices: Array<{ quantity: number; price: { amount: number; formattedAmount: string } }>;
    }>;
  } | null;
};

export type GetQuoteQueryVariables = Exact<{
  id: string;
  storeId?: string | null | undefined;
  userId?: string | null | undefined;
  cultureName?: string | null | undefined;
  currencyCode?: string | null | undefined;
}>;

export type GetQuoteQuery = {
  quote: {
    id: string;
    number: string;
    status: string | null;
    storeId: string;
    customerId: string | null;
    comment: string | null;
    isAnonymous: boolean;
    isCancelled: boolean;
    addresses: Array<{
      addressType: number | null;
      city: string;
      countryCode: string | null;
      countryName: string;
      line1: string | null;
      postalCode: string | null;
      regionId: string | null;
      regionName: string | null;
    }>;
    totals: {
      originalSubTotalExlTax: { amount: number; formattedAmount: string };
      subTotalExlTax: { amount: number; formattedAmount: string };
      shippingTotal: { amount: number; formattedAmount: string };
      discountTotal: { amount: number; formattedAmount: string };
      taxTotal: { amount: number; formattedAmount: string };
      grandTotalExlTax: { amount: number; formattedAmount: string };
      grandTotalInclTax: { amount: number; formattedAmount: string };
    };
    items: Array<{
      id: string;
      name: string;
      sku: string | null;
      productId: string | null;
      quantity: number;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      proposalPrices: Array<{ quantity: number; price: { amount: number; formattedAmount: string } }>;
    }>;
  } | null;
};

export type RemoveQuoteItemMutationVariables = Exact<{
  command: RemoveQuoteItemCommandType;
}>;

export type RemoveQuoteItemMutation = {
  removeQuoteItem: {
    id: string;
    number: string;
    status: string | null;
    storeId: string;
    customerId: string | null;
    comment: string | null;
    isAnonymous: boolean;
    isCancelled: boolean;
    totals: {
      originalSubTotalExlTax: { amount: number; formattedAmount: string };
      subTotalExlTax: { amount: number; formattedAmount: string };
      shippingTotal: { amount: number; formattedAmount: string };
      discountTotal: { amount: number; formattedAmount: string };
      taxTotal: { amount: number; formattedAmount: string };
      grandTotalExlTax: { amount: number; formattedAmount: string };
      grandTotalInclTax: { amount: number; formattedAmount: string };
    };
    items: Array<{
      id: string;
      name: string;
      sku: string | null;
      productId: string | null;
      quantity: number;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      proposalPrices: Array<{ quantity: number; price: { amount: number; formattedAmount: string } }>;
    }>;
  } | null;
};

export type SubmitQuoteRequestMutationVariables = Exact<{
  command: SubmitQuoteCommandType;
}>;

export type SubmitQuoteRequestMutation = {
  submitQuoteRequest: {
    id: string;
    number: string;
    status: string | null;
    storeId: string;
    customerId: string | null;
    comment: string | null;
    isAnonymous: boolean;
    isCancelled: boolean;
    totals: {
      originalSubTotalExlTax: { amount: number; formattedAmount: string };
      subTotalExlTax: { amount: number; formattedAmount: string };
      shippingTotal: { amount: number; formattedAmount: string };
      discountTotal: { amount: number; formattedAmount: string };
      taxTotal: { amount: number; formattedAmount: string };
      grandTotalExlTax: { amount: number; formattedAmount: string };
      grandTotalInclTax: { amount: number; formattedAmount: string };
    };
    items: Array<{
      id: string;
      name: string;
      sku: string | null;
      productId: string | null;
      quantity: number;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      proposalPrices: Array<{ quantity: number; price: { amount: number; formattedAmount: string } }>;
    }>;
  } | null;
};

export type UpdateQuoteAddressesMutationVariables = Exact<{
  command: UpdateQuoteAddressesCommandType;
}>;

export type UpdateQuoteAddressesMutation = {
  updateQuoteAddresses: {
    id: string;
    number: string;
    status: string | null;
    storeId: string;
    customerId: string | null;
    comment: string | null;
    isAnonymous: boolean;
    isCancelled: boolean;
    addresses: Array<{
      addressType: number | null;
      city: string;
      countryCode: string | null;
      countryName: string;
      line1: string | null;
      postalCode: string | null;
      regionId: string | null;
      regionName: string | null;
    }>;
    totals: {
      originalSubTotalExlTax: { amount: number; formattedAmount: string };
      subTotalExlTax: { amount: number; formattedAmount: string };
      shippingTotal: { amount: number; formattedAmount: string };
      discountTotal: { amount: number; formattedAmount: string };
      taxTotal: { amount: number; formattedAmount: string };
      grandTotalExlTax: { amount: number; formattedAmount: string };
      grandTotalInclTax: { amount: number; formattedAmount: string };
    };
    items: Array<{
      id: string;
      name: string;
      sku: string | null;
      productId: string | null;
      quantity: number;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      proposalPrices: Array<{ quantity: number; price: { amount: number; formattedAmount: string } }>;
    }>;
  } | null;
};

export type GetSavedForLaterQueryVariables = Exact<{
  storeId: string;
  userId: string;
  currencyCode?: string | null | undefined;
  cultureName?: string | null | undefined;
}>;

export type GetSavedForLaterQuery = {
  getSavedForLater: {
    id: string;
    storeId: string;
    isAnonymous: boolean;
    hasPhysicalProducts: boolean | null;
    customerId: string;
    itemsCount: number;
    itemsQuantity: number;
    total: { amount: number; formattedAmount: string };
    subTotal: { amount: number; formattedAmount: string };
    subTotalDiscount: { amount: number; formattedAmount: string };
    shippingTotal: { amount: number; formattedAmount: string };
    items: Array<{
      id: string;
      sku: string;
      productId: string;
      name: string;
      quantity: number;
      selectedForCheckout: boolean;
      isValid: boolean;
      listPrice: { amount: number; formattedAmount: string };
      salePrice: { amount: number; formattedAmount: string };
      placedPrice: { amount: number; formattedAmount: string };
      extendedPrice: { amount: number; formattedAmount: string };
      discountAmount: { amount: number; formattedAmount: string };
      validationErrors: Array<{
        errorCode: string | null;
        errorMessage: string | null;
        objectType: string | null;
        objectId: string | null;
        errorParameters: Array<{ key: string; value: string } | null> | null;
      }>;
      configurationItems: Array<{
        id: string;
        sectionId: string;
        type: string;
        productId: string | null;
        name: string | null;
        sku: string | null;
        imageUrl: string | null;
        quantity: number | null;
        customText: string | null;
        selectedForCheckout: boolean;
      } | null> | null;
    }>;
    payments: Array<{
      id: string;
      outerId: string | null;
      paymentGatewayCode: string | null;
      currency: { code: string };
      total: { amount: number; formattedAmount: string };
      billingAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    shipments: Array<{
      id: string;
      shipmentMethodCode: string | null;
      shipmentMethodOption: string | null;
      fulfillmentCenterId: string | null;
      price: { amount: number; formattedAmount: string };
      currency: { code: string };
      deliveryAddress: {
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      } | null;
    }>;
    coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
    gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
    addresses: Array<{
      id: string | null;
      key: string | null;
      city: string | null;
      countryCode: string | null;
      countryName: string | null;
      email: string | null;
      firstName: string | null;
      middleName: string | null;
      lastName: string | null;
      line1: string | null;
      line2: string | null;
      name: string | null;
      organization: string | null;
      phone: string | null;
      postalCode: string;
      regionId: string | null;
      regionName: string | null;
      zip: string | null;
      outerId: string | null;
      description: string | null;
      addressType: number | null;
    }>;
    validationErrors: Array<{
      errorCode: string | null;
      errorMessage: string | null;
      objectType: string | null;
      objectId: string | null;
      errorParameters: Array<{ key: string; value: string } | null> | null;
    }>;
  } | null;
};

export type MoveFromSavedForLaterMutationVariables = Exact<{
  command: InputSaveForLaterType;
}>;

export type MoveFromSavedForLaterMutation = {
  moveFromSavedForLater: {
    cart: {
      id: string;
      storeId: string;
      isAnonymous: boolean;
      hasPhysicalProducts: boolean | null;
      customerId: string;
      itemsCount: number;
      itemsQuantity: number;
      total: { amount: number; formattedAmount: string };
      subTotal: { amount: number; formattedAmount: string };
      subTotalDiscount: { amount: number; formattedAmount: string };
      shippingTotal: { amount: number; formattedAmount: string };
      items: Array<{
        id: string;
        sku: string;
        productId: string;
        name: string;
        quantity: number;
        selectedForCheckout: boolean;
        isValid: boolean;
        listPrice: { amount: number; formattedAmount: string };
        salePrice: { amount: number; formattedAmount: string };
        placedPrice: { amount: number; formattedAmount: string };
        extendedPrice: { amount: number; formattedAmount: string };
        discountAmount: { amount: number; formattedAmount: string };
        validationErrors: Array<{
          errorCode: string | null;
          errorMessage: string | null;
          objectType: string | null;
          objectId: string | null;
          errorParameters: Array<{ key: string; value: string } | null> | null;
        }>;
        configurationItems: Array<{
          id: string;
          sectionId: string;
          type: string;
          productId: string | null;
          name: string | null;
          sku: string | null;
          imageUrl: string | null;
          quantity: number | null;
          customText: string | null;
          selectedForCheckout: boolean;
        } | null> | null;
      }>;
      payments: Array<{
        id: string;
        outerId: string | null;
        paymentGatewayCode: string | null;
        currency: { code: string };
        total: { amount: number; formattedAmount: string };
        billingAddress: {
          id: string | null;
          key: string | null;
          city: string | null;
          countryCode: string | null;
          countryName: string | null;
          email: string | null;
          firstName: string | null;
          middleName: string | null;
          lastName: string | null;
          line1: string | null;
          line2: string | null;
          name: string | null;
          organization: string | null;
          phone: string | null;
          postalCode: string;
          regionId: string | null;
          regionName: string | null;
          zip: string | null;
          outerId: string | null;
          description: string | null;
          addressType: number | null;
        } | null;
      }>;
      shipments: Array<{
        id: string;
        shipmentMethodCode: string | null;
        shipmentMethodOption: string | null;
        fulfillmentCenterId: string | null;
        price: { amount: number; formattedAmount: string };
        currency: { code: string };
        deliveryAddress: {
          id: string | null;
          key: string | null;
          city: string | null;
          countryCode: string | null;
          countryName: string | null;
          email: string | null;
          firstName: string | null;
          middleName: string | null;
          lastName: string | null;
          line1: string | null;
          line2: string | null;
          name: string | null;
          organization: string | null;
          phone: string | null;
          postalCode: string;
          regionId: string | null;
          regionName: string | null;
          zip: string | null;
          outerId: string | null;
          description: string | null;
          addressType: number | null;
        } | null;
      }>;
      coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
      gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
      addresses: Array<{
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      }>;
      validationErrors: Array<{
        errorCode: string | null;
        errorMessage: string | null;
        objectType: string | null;
        objectId: string | null;
        errorParameters: Array<{ key: string; value: string } | null> | null;
      }>;
    } | null;
    list: {
      id: string;
      storeId: string;
      isAnonymous: boolean;
      hasPhysicalProducts: boolean | null;
      customerId: string;
      itemsCount: number;
      itemsQuantity: number;
      total: { amount: number; formattedAmount: string };
      subTotal: { amount: number; formattedAmount: string };
      subTotalDiscount: { amount: number; formattedAmount: string };
      shippingTotal: { amount: number; formattedAmount: string };
      items: Array<{
        id: string;
        sku: string;
        productId: string;
        name: string;
        quantity: number;
        selectedForCheckout: boolean;
        isValid: boolean;
        listPrice: { amount: number; formattedAmount: string };
        salePrice: { amount: number; formattedAmount: string };
        placedPrice: { amount: number; formattedAmount: string };
        extendedPrice: { amount: number; formattedAmount: string };
        discountAmount: { amount: number; formattedAmount: string };
        validationErrors: Array<{
          errorCode: string | null;
          errorMessage: string | null;
          objectType: string | null;
          objectId: string | null;
          errorParameters: Array<{ key: string; value: string } | null> | null;
        }>;
        configurationItems: Array<{
          id: string;
          sectionId: string;
          type: string;
          productId: string | null;
          name: string | null;
          sku: string | null;
          imageUrl: string | null;
          quantity: number | null;
          customText: string | null;
          selectedForCheckout: boolean;
        } | null> | null;
      }>;
      payments: Array<{
        id: string;
        outerId: string | null;
        paymentGatewayCode: string | null;
        currency: { code: string };
        total: { amount: number; formattedAmount: string };
        billingAddress: {
          id: string | null;
          key: string | null;
          city: string | null;
          countryCode: string | null;
          countryName: string | null;
          email: string | null;
          firstName: string | null;
          middleName: string | null;
          lastName: string | null;
          line1: string | null;
          line2: string | null;
          name: string | null;
          organization: string | null;
          phone: string | null;
          postalCode: string;
          regionId: string | null;
          regionName: string | null;
          zip: string | null;
          outerId: string | null;
          description: string | null;
          addressType: number | null;
        } | null;
      }>;
      shipments: Array<{
        id: string;
        shipmentMethodCode: string | null;
        shipmentMethodOption: string | null;
        fulfillmentCenterId: string | null;
        price: { amount: number; formattedAmount: string };
        currency: { code: string };
        deliveryAddress: {
          id: string | null;
          key: string | null;
          city: string | null;
          countryCode: string | null;
          countryName: string | null;
          email: string | null;
          firstName: string | null;
          middleName: string | null;
          lastName: string | null;
          line1: string | null;
          line2: string | null;
          name: string | null;
          organization: string | null;
          phone: string | null;
          postalCode: string;
          regionId: string | null;
          regionName: string | null;
          zip: string | null;
          outerId: string | null;
          description: string | null;
          addressType: number | null;
        } | null;
      }>;
      coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
      gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
      addresses: Array<{
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      }>;
      validationErrors: Array<{
        errorCode: string | null;
        errorMessage: string | null;
        objectType: string | null;
        objectId: string | null;
        errorParameters: Array<{ key: string; value: string } | null> | null;
      }>;
    } | null;
  } | null;
};

export type MoveToSavedForLaterMutationVariables = Exact<{
  command: InputSaveForLaterType;
}>;

export type MoveToSavedForLaterMutation = {
  moveToSavedForLater: {
    cart: {
      id: string;
      storeId: string;
      isAnonymous: boolean;
      hasPhysicalProducts: boolean | null;
      customerId: string;
      itemsCount: number;
      itemsQuantity: number;
      total: { amount: number; formattedAmount: string };
      subTotal: { amount: number; formattedAmount: string };
      subTotalDiscount: { amount: number; formattedAmount: string };
      shippingTotal: { amount: number; formattedAmount: string };
      items: Array<{
        id: string;
        sku: string;
        productId: string;
        name: string;
        quantity: number;
        selectedForCheckout: boolean;
        isValid: boolean;
        listPrice: { amount: number; formattedAmount: string };
        salePrice: { amount: number; formattedAmount: string };
        placedPrice: { amount: number; formattedAmount: string };
        extendedPrice: { amount: number; formattedAmount: string };
        discountAmount: { amount: number; formattedAmount: string };
        validationErrors: Array<{
          errorCode: string | null;
          errorMessage: string | null;
          objectType: string | null;
          objectId: string | null;
          errorParameters: Array<{ key: string; value: string } | null> | null;
        }>;
        configurationItems: Array<{
          id: string;
          sectionId: string;
          type: string;
          productId: string | null;
          name: string | null;
          sku: string | null;
          imageUrl: string | null;
          quantity: number | null;
          customText: string | null;
          selectedForCheckout: boolean;
        } | null> | null;
      }>;
      payments: Array<{
        id: string;
        outerId: string | null;
        paymentGatewayCode: string | null;
        currency: { code: string };
        total: { amount: number; formattedAmount: string };
        billingAddress: {
          id: string | null;
          key: string | null;
          city: string | null;
          countryCode: string | null;
          countryName: string | null;
          email: string | null;
          firstName: string | null;
          middleName: string | null;
          lastName: string | null;
          line1: string | null;
          line2: string | null;
          name: string | null;
          organization: string | null;
          phone: string | null;
          postalCode: string;
          regionId: string | null;
          regionName: string | null;
          zip: string | null;
          outerId: string | null;
          description: string | null;
          addressType: number | null;
        } | null;
      }>;
      shipments: Array<{
        id: string;
        shipmentMethodCode: string | null;
        shipmentMethodOption: string | null;
        fulfillmentCenterId: string | null;
        price: { amount: number; formattedAmount: string };
        currency: { code: string };
        deliveryAddress: {
          id: string | null;
          key: string | null;
          city: string | null;
          countryCode: string | null;
          countryName: string | null;
          email: string | null;
          firstName: string | null;
          middleName: string | null;
          lastName: string | null;
          line1: string | null;
          line2: string | null;
          name: string | null;
          organization: string | null;
          phone: string | null;
          postalCode: string;
          regionId: string | null;
          regionName: string | null;
          zip: string | null;
          outerId: string | null;
          description: string | null;
          addressType: number | null;
        } | null;
      }>;
      coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
      gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
      addresses: Array<{
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      }>;
      validationErrors: Array<{
        errorCode: string | null;
        errorMessage: string | null;
        objectType: string | null;
        objectId: string | null;
        errorParameters: Array<{ key: string; value: string } | null> | null;
      }>;
    } | null;
    list: {
      id: string;
      storeId: string;
      isAnonymous: boolean;
      hasPhysicalProducts: boolean | null;
      customerId: string;
      itemsCount: number;
      itemsQuantity: number;
      total: { amount: number; formattedAmount: string };
      subTotal: { amount: number; formattedAmount: string };
      subTotalDiscount: { amount: number; formattedAmount: string };
      shippingTotal: { amount: number; formattedAmount: string };
      items: Array<{
        id: string;
        sku: string;
        productId: string;
        name: string;
        quantity: number;
        selectedForCheckout: boolean;
        isValid: boolean;
        listPrice: { amount: number; formattedAmount: string };
        salePrice: { amount: number; formattedAmount: string };
        placedPrice: { amount: number; formattedAmount: string };
        extendedPrice: { amount: number; formattedAmount: string };
        discountAmount: { amount: number; formattedAmount: string };
        validationErrors: Array<{
          errorCode: string | null;
          errorMessage: string | null;
          objectType: string | null;
          objectId: string | null;
          errorParameters: Array<{ key: string; value: string } | null> | null;
        }>;
        configurationItems: Array<{
          id: string;
          sectionId: string;
          type: string;
          productId: string | null;
          name: string | null;
          sku: string | null;
          imageUrl: string | null;
          quantity: number | null;
          customText: string | null;
          selectedForCheckout: boolean;
        } | null> | null;
      }>;
      payments: Array<{
        id: string;
        outerId: string | null;
        paymentGatewayCode: string | null;
        currency: { code: string };
        total: { amount: number; formattedAmount: string };
        billingAddress: {
          id: string | null;
          key: string | null;
          city: string | null;
          countryCode: string | null;
          countryName: string | null;
          email: string | null;
          firstName: string | null;
          middleName: string | null;
          lastName: string | null;
          line1: string | null;
          line2: string | null;
          name: string | null;
          organization: string | null;
          phone: string | null;
          postalCode: string;
          regionId: string | null;
          regionName: string | null;
          zip: string | null;
          outerId: string | null;
          description: string | null;
          addressType: number | null;
        } | null;
      }>;
      shipments: Array<{
        id: string;
        shipmentMethodCode: string | null;
        shipmentMethodOption: string | null;
        fulfillmentCenterId: string | null;
        price: { amount: number; formattedAmount: string };
        currency: { code: string };
        deliveryAddress: {
          id: string | null;
          key: string | null;
          city: string | null;
          countryCode: string | null;
          countryName: string | null;
          email: string | null;
          firstName: string | null;
          middleName: string | null;
          lastName: string | null;
          line1: string | null;
          line2: string | null;
          name: string | null;
          organization: string | null;
          phone: string | null;
          postalCode: string;
          regionId: string | null;
          regionName: string | null;
          zip: string | null;
          outerId: string | null;
          description: string | null;
          addressType: number | null;
        } | null;
      }>;
      coupons: Array<{ code: string | null; isAppliedSuccessfully: boolean }>;
      gifts: Array<{ id: string; quantity: number; productId: string | null; name: string; lineItemId: string | null }>;
      addresses: Array<{
        id: string | null;
        key: string | null;
        city: string | null;
        countryCode: string | null;
        countryName: string | null;
        email: string | null;
        firstName: string | null;
        middleName: string | null;
        lastName: string | null;
        line1: string | null;
        line2: string | null;
        name: string | null;
        organization: string | null;
        phone: string | null;
        postalCode: string;
        regionId: string | null;
        regionName: string | null;
        zip: string | null;
        outerId: string | null;
        description: string | null;
        addressType: number | null;
      }>;
      validationErrors: Array<{
        errorCode: string | null;
        errorMessage: string | null;
        objectType: string | null;
        objectId: string | null;
        errorParameters: Array<{ key: string; value: string } | null> | null;
      }>;
    } | null;
  } | null;
};

export type SlugInfoQueryVariables = Exact<{
  storeId?: string | null | undefined;
  slug?: string | null | undefined;
  permalink?: string | null | undefined;
  userId?: string | null | undefined;
  cultureName?: string | null | undefined;
}>;

export type SlugInfoQuery = {
  slugInfo: {
    redirectUrl: string | null;
    entityInfo: {
      id: string;
      name: string | null;
      semanticUrl: string;
      outline: string | null;
      pageTitle: string | null;
      metaDescription: string | null;
      imageAltDescription: string | null;
      metaKeywords: string | null;
      storeId: string | null;
      objectId: string;
      objectType: string;
      isActive: boolean;
      languageCode: string | null;
    } | null;
  } | null;
};

export type AddBulkItemToShoppingListMutationVariables = Exact<{
  command: InputAddWishlistBulkItemType;
}>;

export type AddBulkItemToShoppingListMutation = {
  addWishlistBulkItem: {
    wishlists: Array<{
      id: string;
      name: string;
      storeId: string | null;
      customerId: string | null;
      customerName: string | null;
      itemsCount: number | null;
      description: string | null;
      items: Array<{ id: string; sku: string; productId: string; name: string; quantity: number } | null> | null;
      subTotal: { amount: number; formattedAmount: string };
      sharingSetting: { id: string; scope: WishlistScopeType | null } | null;
    } | null> | null;
  } | null;
};

export type AddItemsToShoppingListMutationVariables = Exact<{
  command: InputAddWishlistItemsType;
}>;

export type AddItemsToShoppingListMutation = {
  addWishlistItems: {
    id: string;
    name: string;
    storeId: string | null;
    customerId: string | null;
    customerName: string | null;
    itemsCount: number | null;
    description: string | null;
    items: Array<{ id: string; sku: string; productId: string; name: string; quantity: number } | null> | null;
    subTotal: { amount: number; formattedAmount: string };
    sharingSetting: { id: string; scope: WishlistScopeType | null } | null;
  } | null;
};

export type ChangeShoppingListMutationVariables = Exact<{
  command: InputChangeWishlistType;
}>;

export type ChangeShoppingListMutation = {
  changeWishlist: {
    id: string;
    name: string;
    storeId: string | null;
    customerId: string | null;
    customerName: string | null;
    itemsCount: number | null;
    description: string | null;
    items: Array<{ id: string; sku: string; productId: string; name: string; quantity: number } | null> | null;
    subTotal: { amount: number; formattedAmount: string };
    sharingSetting: { id: string; scope: WishlistScopeType | null } | null;
  } | null;
};

export type CreateShoppingListMutationVariables = Exact<{
  command: InputCreateWishlistType;
}>;

export type CreateShoppingListMutation = {
  createWishlist: {
    id: string;
    name: string;
    storeId: string | null;
    customerId: string | null;
    customerName: string | null;
    itemsCount: number | null;
    description: string | null;
    items: Array<{ id: string; sku: string; productId: string; name: string; quantity: number } | null> | null;
    subTotal: { amount: number; formattedAmount: string };
    sharingSetting: { id: string; scope: WishlistScopeType | null } | null;
  } | null;
};

export type DeleteShoppingListMutationVariables = Exact<{
  command: InputRemoveWishlistType;
}>;

export type DeleteShoppingListMutation = { removeWishlist: boolean | null };

export type GetShoppingListQueryVariables = Exact<{
  listId: string;
  cultureName?: string | null | undefined;
}>;

export type GetShoppingListQuery = {
  wishlist: {
    id: string;
    name: string;
    storeId: string | null;
    customerId: string | null;
    customerName: string | null;
    itemsCount: number | null;
    description: string | null;
    items: Array<{ id: string; sku: string; productId: string; name: string; quantity: number } | null> | null;
    subTotal: { amount: number; formattedAmount: string };
    sharingSetting: { id: string; scope: WishlistScopeType | null } | null;
  } | null;
};

export type GetShoppingListsQueryVariables = Exact<{
  storeId?: string | null | undefined;
  userId?: string | null | undefined;
  currencyCode?: string | null | undefined;
  cultureName?: string | null | undefined;
}>;

export type GetShoppingListsQuery = {
  wishlists: {
    items: Array<{
      id: string;
      name: string;
      storeId: string | null;
      customerId: string | null;
      customerName: string | null;
      itemsCount: number | null;
      description: string | null;
      items: Array<{ id: string; sku: string; productId: string; name: string; quantity: number } | null> | null;
      subTotal: { amount: number; formattedAmount: string };
      sharingSetting: { id: string; scope: WishlistScopeType | null } | null;
    } | null> | null;
  } | null;
};

export type RemoveItemsFromShoppingListMutationVariables = Exact<{
  command: InputRemoveWishlistItemsType;
}>;

export type RemoveItemsFromShoppingListMutation = {
  removeWishlistItems: {
    id: string;
    name: string;
    storeId: string | null;
    customerId: string | null;
    customerName: string | null;
    itemsCount: number | null;
    description: string | null;
    items: Array<{ id: string; sku: string; productId: string; name: string; quantity: number } | null> | null;
    subTotal: { amount: number; formattedAmount: string };
    sharingSetting: { id: string; scope: WishlistScopeType | null } | null;
  } | null;
};

export type UpdateShoppingListItemsMutationVariables = Exact<{
  command: InputUpdateWishlistItemsType;
}>;

export type UpdateShoppingListItemsMutation = {
  updateWishListItems: {
    id: string;
    name: string;
    storeId: string | null;
    customerId: string | null;
    customerName: string | null;
    itemsCount: number | null;
    description: string | null;
    items: Array<{ id: string; sku: string; productId: string; name: string; quantity: number } | null> | null;
    subTotal: { amount: number; formattedAmount: string };
    sharingSetting: { id: string; scope: WishlistScopeType | null } | null;
  } | null;
};

export type DeleteUsersMutationVariables = Exact<{
  command: InputDeleteUserType;
}>;

export type DeleteUsersMutation = {
  deleteUsers: {
    succeeded: boolean;
    errors: Array<{ code: string | null; description: string | null } | null> | null;
  } | null;
};

export type GetMeQueryVariables = Exact<{ [key: string]: never }>;

export type GetMeQuery = {
  me: {
    id: string;
    userName: string;
    email: string | null;
    emailConfirmed: boolean;
    isAdministrator: boolean;
    memberId: string | null;
    storeId: string | null;
    roles: Array<{ id: string; name: string; normalizedName: string } | null> | null;
  } | null;
};

export type GetUserQueryVariables = Exact<{
  userName?: string | null | undefined;
  email?: string | null | undefined;
  id?: string | null | undefined;
}>;

export type GetUserQuery = {
  user: {
    id: string;
    userName: string;
    email: string | null;
    emailConfirmed: boolean;
    isAdministrator: boolean;
    memberId: string | null;
    storeId: string | null;
    roles: Array<{ id: string; name: string; normalizedName: string } | null> | null;
  } | null;
};

export type InviteUserMutationVariables = Exact<{
  command: InputInviteUserType;
}>;

export type InviteUserMutation = {
  inviteUser: {
    succeeded: boolean;
    errors: Array<{ code: string; parameter: string | null; description: string | null } | null> | null;
  } | null;
};

export type RegisterByInvitationMutationVariables = Exact<{
  command: InputRegisterByInvitationType;
}>;

export type RegisterByInvitationMutation = {
  registerByInvitation: {
    succeeded: boolean;
    errors: Array<{ code: string; parameter: string | null; description: string | null } | null> | null;
  } | null;
};

export type ResetPasswordByTokenMutationVariables = Exact<{
  command: InputResetPasswordByTokenType;
}>;

export type ResetPasswordByTokenMutation = {
  resetPasswordByToken: {
    succeeded: boolean;
    errors: Array<{ code: string; parameter: string | null; description: string | null } | null> | null;
  } | null;
};

export type SendPasswordResetEmailMutationVariables = Exact<{
  command: SendPasswordResetEmailCommandType;
}>;

export type SendPasswordResetEmailMutation = { sendPasswordResetEmail: boolean | null };

export class TypedDocumentString<TResult, TVariables>
  extends String
  implements DocumentTypeDecoration<TResult, TVariables>
{
  __apiType?: NonNullable<DocumentTypeDecoration<TResult, TVariables>["__apiType"]>;
  private value: string;
  public __meta__?: Record<string, any> | undefined;

  constructor(value: string, __meta__?: Record<string, any> | undefined) {
    super(value);
    this.value = value;
    this.__meta__ = __meta__;
  }

  override toString(): string & DocumentTypeDecoration<TResult, TVariables> {
    return this.value;
  }
}
export const MoneyFragmentDoc = new TypedDocumentString(
  `
    fragment Money on MoneyType {
  amount
  formattedAmount
}
    `,
  { fragmentName: "Money" },
) as unknown as TypedDocumentString<MoneyFragment, unknown>;
export const CartConfigurationItemFragmentDoc = new TypedDocumentString(
  `
    fragment CartConfigurationItem on CartConfigurationItemType {
  id
  sectionId
  type
  productId
  name
  sku
  imageUrl
  quantity
  customText
  selectedForCheckout
}
    `,
  { fragmentName: "CartConfigurationItem" },
) as unknown as TypedDocumentString<CartConfigurationItemFragment, unknown>;
export const LineItemFragmentDoc = new TypedDocumentString(
  `
    fragment LineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  placedPrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
  selectedForCheckout
  isValid
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
  configurationItems {
    ...CartConfigurationItem
  }
}
    fragment CartConfigurationItem on CartConfigurationItemType {
  id
  sectionId
  type
  productId
  name
  sku
  imageUrl
  quantity
  customText
  selectedForCheckout
}
fragment Money on MoneyType {
  amount
  formattedAmount
}`,
  { fragmentName: "LineItem" },
) as unknown as TypedDocumentString<LineItemFragment, unknown>;
export const CurrencyFragmentDoc = new TypedDocumentString(
  `
    fragment Currency on CurrencyType {
  code
}
    `,
  { fragmentName: "Currency" },
) as unknown as TypedDocumentString<CurrencyFragment, unknown>;
export const CartAddressFragmentDoc = new TypedDocumentString(
  `
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
    `,
  { fragmentName: "CartAddress" },
) as unknown as TypedDocumentString<CartAddressFragment, unknown>;
export const PaymentFragmentDoc = new TypedDocumentString(
  `
    fragment Payment on PaymentType {
  id
  outerId
  paymentGatewayCode
  currency {
    ...Currency
  }
  total {
    ...Money
  }
  billingAddress {
    ...CartAddress
  }
}
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
fragment Currency on CurrencyType {
  code
}
fragment Money on MoneyType {
  amount
  formattedAmount
}`,
  { fragmentName: "Payment" },
) as unknown as TypedDocumentString<PaymentFragment, unknown>;
export const ShipmentFragmentDoc = new TypedDocumentString(
  `
    fragment Shipment on ShipmentType {
  id
  shipmentMethodCode
  shipmentMethodOption
  fulfillmentCenterId
  price {
    ...Money
  }
  currency {
    ...Currency
  }
  deliveryAddress {
    ...CartAddress
  }
}
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
fragment Currency on CurrencyType {
  code
}
fragment Money on MoneyType {
  amount
  formattedAmount
}`,
  { fragmentName: "Shipment" },
) as unknown as TypedDocumentString<ShipmentFragment, unknown>;
export const CouponFragmentDoc = new TypedDocumentString(
  `
    fragment Coupon on CouponType {
  code
  isAppliedSuccessfully
}
    `,
  { fragmentName: "Coupon" },
) as unknown as TypedDocumentString<CouponFragment, unknown>;
export const GiftItemFragmentDoc = new TypedDocumentString(
  `
    fragment GiftItem on GiftItemType {
  id
  quantity
  productId
  name
  lineItemId
}
    `,
  { fragmentName: "GiftItem" },
) as unknown as TypedDocumentString<GiftItemFragment, unknown>;
export const CartFragmentDoc = new TypedDocumentString(
  `
    fragment Cart on CartType {
  id
  storeId
  isAnonymous
  hasPhysicalProducts
  customerId
  itemsCount
  itemsQuantity
  total {
    ...Money
  }
  subTotal {
    ...Money
  }
  subTotalDiscount {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  items {
    ...LineItem
  }
  payments {
    ...Payment
  }
  shipments {
    ...Shipment
  }
  coupons {
    ...Coupon
  }
  gifts {
    ...GiftItem
  }
  addresses {
    ...CartAddress
  }
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
}
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
fragment CartConfigurationItem on CartConfigurationItemType {
  id
  sectionId
  type
  productId
  name
  sku
  imageUrl
  quantity
  customText
  selectedForCheckout
}
fragment Coupon on CouponType {
  code
  isAppliedSuccessfully
}
fragment Currency on CurrencyType {
  code
}
fragment GiftItem on GiftItemType {
  id
  quantity
  productId
  name
  lineItemId
}
fragment LineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  placedPrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
  selectedForCheckout
  isValid
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
  configurationItems {
    ...CartConfigurationItem
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment Payment on PaymentType {
  id
  outerId
  paymentGatewayCode
  currency {
    ...Currency
  }
  total {
    ...Money
  }
  billingAddress {
    ...CartAddress
  }
}
fragment Shipment on ShipmentType {
  id
  shipmentMethodCode
  shipmentMethodOption
  fulfillmentCenterId
  price {
    ...Money
  }
  currency {
    ...Currency
  }
  deliveryAddress {
    ...CartAddress
  }
}`,
  { fragmentName: "Cart" },
) as unknown as TypedDocumentString<CartFragment, unknown>;
export const CartWithListFragmentDoc = new TypedDocumentString(
  `
    fragment CartWithList on CartWithListType {
  cart {
    ...Cart
  }
  list {
    ...Cart
  }
}
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
fragment CartConfigurationItem on CartConfigurationItemType {
  id
  sectionId
  type
  productId
  name
  sku
  imageUrl
  quantity
  customText
  selectedForCheckout
}
fragment Cart on CartType {
  id
  storeId
  isAnonymous
  hasPhysicalProducts
  customerId
  itemsCount
  itemsQuantity
  total {
    ...Money
  }
  subTotal {
    ...Money
  }
  subTotalDiscount {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  items {
    ...LineItem
  }
  payments {
    ...Payment
  }
  shipments {
    ...Shipment
  }
  coupons {
    ...Coupon
  }
  gifts {
    ...GiftItem
  }
  addresses {
    ...CartAddress
  }
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
}
fragment Coupon on CouponType {
  code
  isAppliedSuccessfully
}
fragment Currency on CurrencyType {
  code
}
fragment GiftItem on GiftItemType {
  id
  quantity
  productId
  name
  lineItemId
}
fragment LineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  placedPrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
  selectedForCheckout
  isValid
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
  configurationItems {
    ...CartConfigurationItem
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment Payment on PaymentType {
  id
  outerId
  paymentGatewayCode
  currency {
    ...Currency
  }
  total {
    ...Money
  }
  billingAddress {
    ...CartAddress
  }
}
fragment Shipment on ShipmentType {
  id
  shipmentMethodCode
  shipmentMethodOption
  fulfillmentCenterId
  price {
    ...Money
  }
  currency {
    ...Currency
  }
  deliveryAddress {
    ...CartAddress
  }
}`,
  { fragmentName: "CartWithList" },
) as unknown as TypedDocumentString<CartWithListFragment, unknown>;
export const CategoryFragmentDoc = new TypedDocumentString(
  `
    fragment Category on Category {
  id
  code
  name
  outline
  slug
}
    `,
  { fragmentName: "Category" },
) as unknown as TypedDocumentString<CategoryFragment, unknown>;
export const RoleFragmentDoc = new TypedDocumentString(
  `
    fragment Role on RoleType {
  id
  name
  normalizedName
}
    `,
  { fragmentName: "Role" },
) as unknown as TypedDocumentString<RoleFragment, unknown>;
export const UserFragmentDoc = new TypedDocumentString(
  `
    fragment User on UserType {
  id
  userName
  email
  emailConfirmed
  isAdministrator
  memberId
  storeId
  roles {
    ...Role
  }
}
    fragment Role on RoleType {
  id
  name
  normalizedName
}`,
  { fragmentName: "User" },
) as unknown as TypedDocumentString<UserFragment, unknown>;
export const ContactFragmentDoc = new TypedDocumentString(
  `
    fragment Contact on ContactType {
  id
  firstName
  lastName
  fullName
  status
  organizationId
  organizationsIds
  securityAccounts {
    ...User
  }
}
    fragment Role on RoleType {
  id
  name
  normalizedName
}
fragment User on UserType {
  id
  userName
  email
  emailConfirmed
  isAdministrator
  memberId
  storeId
  roles {
    ...Role
  }
}`,
  { fragmentName: "Contact" },
) as unknown as TypedDocumentString<ContactFragment, unknown>;
export const CustomIdentityResultFragmentDoc = new TypedDocumentString(
  `
    fragment CustomIdentityResult on CustomIdentityResultType {
  succeeded
  errors {
    code
    parameter
    description
  }
}
    `,
  { fragmentName: "CustomIdentityResult" },
) as unknown as TypedDocumentString<CustomIdentityResultFragment, unknown>;
export const IdentityResultFragmentDoc = new TypedDocumentString(
  `
    fragment IdentityResult on IdentityResultType {
  succeeded
  errors {
    code
    description
  }
}
    `,
  { fragmentName: "IdentityResult" },
) as unknown as TypedDocumentString<IdentityResultFragment, unknown>;
export const MemberAddressFragmentDoc = new TypedDocumentString(
  `
    fragment MemberAddress on MemberAddressType {
  id
  key
  isDefault
  isFavorite
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
    `,
  { fragmentName: "MemberAddress" },
) as unknown as TypedDocumentString<MemberAddressFragment, unknown>;
export const OrderLineItemFragmentDoc = new TypedDocumentString(
  `
    fragment OrderLineItem on OrderLineItemType {
  id
  name
  sku
  productId
  quantity
  price {
    ...Money
  }
  extendedPrice {
    ...Money
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}`,
  { fragmentName: "OrderLineItem" },
) as unknown as TypedDocumentString<OrderLineItemFragment, unknown>;
export const OrderPaymentFragmentDoc = new TypedDocumentString(
  `
    fragment OrderPayment on PaymentInType {
  id
  number
  gatewayCode
  status
  sum {
    ...Money
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}`,
  { fragmentName: "OrderPayment" },
) as unknown as TypedDocumentString<OrderPaymentFragment, unknown>;
export const OrderShipmentFragmentDoc = new TypedDocumentString(
  `
    fragment OrderShipment on OrderShipmentType {
  id
  number
  shipmentMethodCode
  shipmentMethodOption
  status
  total {
    ...Money
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}`,
  { fragmentName: "OrderShipment" },
) as unknown as TypedDocumentString<OrderShipmentFragment, unknown>;
export const OrderFragmentDoc = new TypedDocumentString(
  `
    fragment Order on CustomerOrderType {
  id
  number
  status
  createdDate
  total {
    ...Money
  }
  items {
    ...OrderLineItem
  }
  inPayments {
    ...OrderPayment
  }
  shipments {
    ...OrderShipment
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment OrderLineItem on OrderLineItemType {
  id
  name
  sku
  productId
  quantity
  price {
    ...Money
  }
  extendedPrice {
    ...Money
  }
}
fragment OrderPayment on PaymentInType {
  id
  number
  gatewayCode
  status
  sum {
    ...Money
  }
}
fragment OrderShipment on OrderShipmentType {
  id
  number
  shipmentMethodCode
  shipmentMethodOption
  status
  total {
    ...Money
  }
}`,
  { fragmentName: "Order" },
) as unknown as TypedDocumentString<OrderFragment, unknown>;
export const SeoInfoFragmentDoc = new TypedDocumentString(
  `
    fragment SeoInfo on SeoInfo {
  id
  name
  semanticUrl
  outline
  pageTitle
  metaDescription
  imageAltDescription
  metaKeywords
  storeId
  objectId
  objectType
  isActive
  languageCode
}
    `,
  { fragmentName: "SeoInfo" },
) as unknown as TypedDocumentString<SeoInfoFragment, unknown>;
export const SlugInfoFragmentDoc = new TypedDocumentString(
  `
    fragment SlugInfo on SlugInfoResponseType {
  entityInfo {
    ...SeoInfo
  }
  redirectUrl
}
    fragment SeoInfo on SeoInfo {
  id
  name
  semanticUrl
  outline
  pageTitle
  metaDescription
  imageAltDescription
  metaKeywords
  storeId
  objectId
  objectType
  isActive
  languageCode
}`,
  { fragmentName: "SlugInfo" },
) as unknown as TypedDocumentString<SlugInfoFragment, unknown>;
export const LanguageFragmentDoc = new TypedDocumentString(
  `
    fragment Language on LanguageType {
  cultureName
  nativeName
}
    `,
  { fragmentName: "Language" },
) as unknown as TypedDocumentString<LanguageFragment, unknown>;
export const StoreSettingsFragmentDoc = new TypedDocumentString(
  `
    fragment StoreSettings on StoreSettingsType {
  anonymousUsersAllowed
  taxCalculationEnabled
  seoLinkType
}
    `,
  { fragmentName: "StoreSettings" },
) as unknown as TypedDocumentString<StoreSettingsFragment, unknown>;
export const StoreInfoFragmentDoc = new TypedDocumentString(
  `
    fragment StoreInfo on StoreResponseType {
  storeId
  storeName
  catalogId
  storeUrl
  defaultLanguage {
    ...Language
  }
  availableLanguages {
    ...Language
  }
  defaultCurrency {
    ...Currency
  }
  availableCurrencies {
    ...Currency
  }
  settings {
    ...StoreSettings
  }
}
    fragment Currency on CurrencyType {
  code
}
fragment Language on LanguageType {
  cultureName
  nativeName
}
fragment StoreSettings on StoreSettingsType {
  anonymousUsersAllowed
  taxCalculationEnabled
  seoLinkType
}`,
  { fragmentName: "StoreInfo" },
) as unknown as TypedDocumentString<StoreInfoFragment, unknown>;
export const MenuLinkFragmentDoc = new TypedDocumentString(
  `
    fragment MenuLink on MenuLinkType {
  title
  url
  priority
}
    `,
  { fragmentName: "MenuLink" },
) as unknown as TypedDocumentString<MenuLinkFragment, unknown>;
export const WhiteLabelingSettingsFragmentDoc = new TypedDocumentString(
  `
    fragment WhiteLabelingSettings on WhiteLabelingSettingsType {
  logoUrl
  secondaryLogoUrl
  faviconUrl
  themePresetName
  footerLinks {
    ...MenuLink
  }
  mainMenuLinks {
    ...MenuLink
  }
}
    fragment MenuLink on MenuLinkType {
  title
  url
  priority
}`,
  { fragmentName: "WhiteLabelingSettings" },
) as unknown as TypedDocumentString<WhiteLabelingSettingsFragment, unknown>;
export const PageContextFragmentDoc = new TypedDocumentString(
  `
    fragment PageContext on PageContextResponseType {
  slugInfo {
    ...SlugInfo
  }
  store {
    ...StoreInfo
  }
  whiteLabelingSettings {
    ...WhiteLabelingSettings
  }
  user {
    ...User
  }
}
    fragment Currency on CurrencyType {
  code
}
fragment Language on LanguageType {
  cultureName
  nativeName
}
fragment MenuLink on MenuLinkType {
  title
  url
  priority
}
fragment Role on RoleType {
  id
  name
  normalizedName
}
fragment SeoInfo on SeoInfo {
  id
  name
  semanticUrl
  outline
  pageTitle
  metaDescription
  imageAltDescription
  metaKeywords
  storeId
  objectId
  objectType
  isActive
  languageCode
}
fragment SlugInfo on SlugInfoResponseType {
  entityInfo {
    ...SeoInfo
  }
  redirectUrl
}
fragment StoreInfo on StoreResponseType {
  storeId
  storeName
  catalogId
  storeUrl
  defaultLanguage {
    ...Language
  }
  availableLanguages {
    ...Language
  }
  defaultCurrency {
    ...Currency
  }
  availableCurrencies {
    ...Currency
  }
  settings {
    ...StoreSettings
  }
}
fragment StoreSettings on StoreSettingsType {
  anonymousUsersAllowed
  taxCalculationEnabled
  seoLinkType
}
fragment User on UserType {
  id
  userName
  email
  emailConfirmed
  isAdministrator
  memberId
  storeId
  roles {
    ...Role
  }
}
fragment WhiteLabelingSettings on WhiteLabelingSettingsType {
  logoUrl
  secondaryLogoUrl
  faviconUrl
  themePresetName
  footerLinks {
    ...MenuLink
  }
  mainMenuLinks {
    ...MenuLink
  }
}`,
  { fragmentName: "PageContext" },
) as unknown as TypedDocumentString<PageContextFragment, unknown>;
export const PickupAddressFragmentDoc = new TypedDocumentString(
  `
    fragment PickupAddress on PickupAddressType {
  id
  key
  name
  organization
  countryCode
  countryName
  city
  postalCode
  line1
  line2
  regionId
  regionName
  phone
  email
  outerId
  description
  addressType
}
    `,
  { fragmentName: "PickupAddress" },
) as unknown as TypedDocumentString<PickupAddressFragment, unknown>;
export const PickupLocationFragmentDoc = new TypedDocumentString(
  `
    fragment PickupLocation on PickupLocationType {
  id
  isActive
  name
  description
  contactEmail
  contactPhone
  workingHours
  geoLocation
  address {
    ...PickupAddress
  }
}
    fragment PickupAddress on PickupAddressType {
  id
  key
  name
  organization
  countryCode
  countryName
  city
  postalCode
  line1
  line2
  regionId
  regionName
  phone
  email
  outerId
  description
  addressType
}`,
  { fragmentName: "PickupLocation" },
) as unknown as TypedDocumentString<PickupLocationFragment, unknown>;
export const VendorFragmentDoc = new TypedDocumentString(
  `
    fragment Vendor on CommonVendor {
  id
  name
}
    `,
  { fragmentName: "Vendor" },
) as unknown as TypedDocumentString<VendorFragment, unknown>;
export const ProductPriceFragmentDoc = new TypedDocumentString(
  `
    fragment ProductPrice on PriceType {
  list {
    ...Money
  }
  actual {
    ...Money
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}`,
  { fragmentName: "ProductPrice" },
) as unknown as TypedDocumentString<ProductPriceFragment, unknown>;
export const ProductFragmentDoc = new TypedDocumentString(
  `
    fragment Product on Product {
  id
  code
  productType
  isConfigurable
  name
  vendor {
    ...Vendor
  }
  price {
    ...ProductPrice
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment ProductPrice on PriceType {
  list {
    ...Money
  }
  actual {
    ...Money
  }
}
fragment Vendor on CommonVendor {
  id
  name
}`,
  { fragmentName: "Product" },
) as unknown as TypedDocumentString<ProductFragment, unknown>;
export const ConfigurationLineItemFragmentDoc = new TypedDocumentString(
  `
    fragment ConfigurationLineItem on ConfigurationLineItemType {
  id
  text
  quantity
  product {
    ...Product
  }
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment ProductPrice on PriceType {
  list {
    ...Money
  }
  actual {
    ...Money
  }
}
fragment Product on Product {
  id
  code
  productType
  isConfigurable
  name
  vendor {
    ...Vendor
  }
  price {
    ...ProductPrice
  }
}
fragment Vendor on CommonVendor {
  id
  name
}`,
  { fragmentName: "ConfigurationLineItem" },
) as unknown as TypedDocumentString<ConfigurationLineItemFragment, unknown>;
export const ProductConfigurationFragmentDoc = new TypedDocumentString(
  `
    fragment ProductConfiguration on ConfigurationQueryResponseType {
  configurationSections {
    id
    name
    description
    isRequired
    type
    allowCustomText
    allowTextOptions
    maxLength
    options {
      ...ConfigurationLineItem
    }
  }
}
    fragment ConfigurationLineItem on ConfigurationLineItemType {
  id
  text
  quantity
  product {
    ...Product
  }
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment ProductPrice on PriceType {
  list {
    ...Money
  }
  actual {
    ...Money
  }
}
fragment Product on Product {
  id
  code
  productType
  isConfigurable
  name
  vendor {
    ...Vendor
  }
  price {
    ...ProductPrice
  }
}
fragment Vendor on CommonVendor {
  id
  name
}`,
  { fragmentName: "ProductConfiguration" },
) as unknown as TypedDocumentString<ProductConfigurationFragment, unknown>;
export const PickupLocationAddressFragmentDoc = new TypedDocumentString(
  `
    fragment PickupLocationAddress on PickupLocationAddressType {
  id
  key
  name
  organization
  countryCode
  countryName
  city
  postalCode
  line1
  line2
  regionId
  regionName
  phone
  email
  outerId
  description
  addressType
}
    `,
  { fragmentName: "PickupLocationAddress" },
) as unknown as TypedDocumentString<PickupLocationAddressFragment, unknown>;
export const ProductPickupLocationFragmentDoc = new TypedDocumentString(
  `
    fragment ProductPickupLocation on ProductPickupLocation {
  id
  isActive
  name
  description
  contactEmail
  contactPhone
  workingHours
  deliveryDays
  storageDays
  geoLocation
  address {
    ...PickupLocationAddress
  }
  availabilityType
  availabilityNote
  availableQuantity
}
    fragment PickupLocationAddress on PickupLocationAddressType {
  id
  key
  name
  organization
  countryCode
  countryName
  city
  postalCode
  line1
  line2
  regionId
  regionName
  phone
  email
  outerId
  description
  addressType
}`,
  { fragmentName: "ProductPickupLocation" },
) as unknown as TypedDocumentString<ProductPickupLocationFragment, unknown>;
export const QuoteAddressFragmentDoc = new TypedDocumentString(
  `
    fragment QuoteAddress on QuoteAddressType {
  addressType
  city
  countryCode
  countryName
  line1
  postalCode
  regionId
  regionName
}
    `,
  { fragmentName: "QuoteAddress" },
) as unknown as TypedDocumentString<QuoteAddressFragment, unknown>;
export const QuoteTotalsFragmentDoc = new TypedDocumentString(
  `
    fragment QuoteTotals on QuoteTotalsType {
  originalSubTotalExlTax {
    ...Money
  }
  subTotalExlTax {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  discountTotal {
    ...Money
  }
  taxTotal {
    ...Money
  }
  grandTotalExlTax {
    ...Money
  }
  grandTotalInclTax {
    ...Money
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}`,
  { fragmentName: "QuoteTotals" },
) as unknown as TypedDocumentString<QuoteTotalsFragment, unknown>;
export const QuoteItemFragmentDoc = new TypedDocumentString(
  `
    fragment QuoteItem on QuoteItemType {
  id
  name
  sku
  productId
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  proposalPrices {
    quantity
    price {
      ...Money
    }
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}`,
  { fragmentName: "QuoteItem" },
) as unknown as TypedDocumentString<QuoteItemFragment, unknown>;
export const QuoteFragmentDoc = new TypedDocumentString(
  `
    fragment Quote on QuoteType {
  id
  number
  status
  storeId
  customerId
  comment
  isAnonymous
  isCancelled
  totals {
    ...QuoteTotals
  }
  items {
    ...QuoteItem
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment QuoteItem on QuoteItemType {
  id
  name
  sku
  productId
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  proposalPrices {
    quantity
    price {
      ...Money
    }
  }
}
fragment QuoteTotals on QuoteTotalsType {
  originalSubTotalExlTax {
    ...Money
  }
  subTotalExlTax {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  discountTotal {
    ...Money
  }
  taxTotal {
    ...Money
  }
  grandTotalExlTax {
    ...Money
  }
  grandTotalInclTax {
    ...Money
  }
}`,
  { fragmentName: "Quote" },
) as unknown as TypedDocumentString<QuoteFragment, unknown>;
export const WishlistLineItemFragmentDoc = new TypedDocumentString(
  `
    fragment WishlistLineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
}
    `,
  { fragmentName: "WishlistLineItem" },
) as unknown as TypedDocumentString<WishlistLineItemFragment, unknown>;
export const ShoppingListFragmentDoc = new TypedDocumentString(
  `
    fragment ShoppingList on WishlistType {
  id
  name
  storeId
  customerId
  customerName
  items {
    ...WishlistLineItem
  }
  itemsCount
  description
  subTotal {
    ...Money
  }
  sharingSetting {
    id
    scope
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment WishlistLineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
}`,
  { fragmentName: "ShoppingList" },
) as unknown as TypedDocumentString<ShoppingListFragment, unknown>;
export const AddBulkItemsCartDocument = new TypedDocumentString(`
    mutation AddBulkItemsCart($command: InputAddBulkItemsType!) {
  addBulkItemsCart(command: $command) {
    cart {
      ...Cart
    }
    errors {
      errorCode
      errorMessage
      objectId
    }
  }
}
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
fragment CartConfigurationItem on CartConfigurationItemType {
  id
  sectionId
  type
  productId
  name
  sku
  imageUrl
  quantity
  customText
  selectedForCheckout
}
fragment Cart on CartType {
  id
  storeId
  isAnonymous
  hasPhysicalProducts
  customerId
  itemsCount
  itemsQuantity
  total {
    ...Money
  }
  subTotal {
    ...Money
  }
  subTotalDiscount {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  items {
    ...LineItem
  }
  payments {
    ...Payment
  }
  shipments {
    ...Shipment
  }
  coupons {
    ...Coupon
  }
  gifts {
    ...GiftItem
  }
  addresses {
    ...CartAddress
  }
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
}
fragment Coupon on CouponType {
  code
  isAppliedSuccessfully
}
fragment Currency on CurrencyType {
  code
}
fragment GiftItem on GiftItemType {
  id
  quantity
  productId
  name
  lineItemId
}
fragment LineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  placedPrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
  selectedForCheckout
  isValid
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
  configurationItems {
    ...CartConfigurationItem
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment Payment on PaymentType {
  id
  outerId
  paymentGatewayCode
  currency {
    ...Currency
  }
  total {
    ...Money
  }
  billingAddress {
    ...CartAddress
  }
}
fragment Shipment on ShipmentType {
  id
  shipmentMethodCode
  shipmentMethodOption
  fulfillmentCenterId
  price {
    ...Money
  }
  currency {
    ...Currency
  }
  deliveryAddress {
    ...CartAddress
  }
}`) as unknown as TypedDocumentString<AddBulkItemsCartMutation, AddBulkItemsCartMutationVariables>;
export const AddCouponDocument = new TypedDocumentString(`
    mutation AddCoupon($command: InputAddCouponType!) {
  addCoupon(command: $command) {
    ...Cart
  }
}
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
fragment CartConfigurationItem on CartConfigurationItemType {
  id
  sectionId
  type
  productId
  name
  sku
  imageUrl
  quantity
  customText
  selectedForCheckout
}
fragment Cart on CartType {
  id
  storeId
  isAnonymous
  hasPhysicalProducts
  customerId
  itemsCount
  itemsQuantity
  total {
    ...Money
  }
  subTotal {
    ...Money
  }
  subTotalDiscount {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  items {
    ...LineItem
  }
  payments {
    ...Payment
  }
  shipments {
    ...Shipment
  }
  coupons {
    ...Coupon
  }
  gifts {
    ...GiftItem
  }
  addresses {
    ...CartAddress
  }
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
}
fragment Coupon on CouponType {
  code
  isAppliedSuccessfully
}
fragment Currency on CurrencyType {
  code
}
fragment GiftItem on GiftItemType {
  id
  quantity
  productId
  name
  lineItemId
}
fragment LineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  placedPrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
  selectedForCheckout
  isValid
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
  configurationItems {
    ...CartConfigurationItem
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment Payment on PaymentType {
  id
  outerId
  paymentGatewayCode
  currency {
    ...Currency
  }
  total {
    ...Money
  }
  billingAddress {
    ...CartAddress
  }
}
fragment Shipment on ShipmentType {
  id
  shipmentMethodCode
  shipmentMethodOption
  fulfillmentCenterId
  price {
    ...Money
  }
  currency {
    ...Currency
  }
  deliveryAddress {
    ...CartAddress
  }
}`) as unknown as TypedDocumentString<AddCouponMutation, AddCouponMutationVariables>;
export const AddItemDocument = new TypedDocumentString(`
    mutation AddItem($command: InputAddItemType!) {
  addItem(command: $command) {
    ...Cart
  }
}
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
fragment CartConfigurationItem on CartConfigurationItemType {
  id
  sectionId
  type
  productId
  name
  sku
  imageUrl
  quantity
  customText
  selectedForCheckout
}
fragment Cart on CartType {
  id
  storeId
  isAnonymous
  hasPhysicalProducts
  customerId
  itemsCount
  itemsQuantity
  total {
    ...Money
  }
  subTotal {
    ...Money
  }
  subTotalDiscount {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  items {
    ...LineItem
  }
  payments {
    ...Payment
  }
  shipments {
    ...Shipment
  }
  coupons {
    ...Coupon
  }
  gifts {
    ...GiftItem
  }
  addresses {
    ...CartAddress
  }
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
}
fragment Coupon on CouponType {
  code
  isAppliedSuccessfully
}
fragment Currency on CurrencyType {
  code
}
fragment GiftItem on GiftItemType {
  id
  quantity
  productId
  name
  lineItemId
}
fragment LineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  placedPrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
  selectedForCheckout
  isValid
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
  configurationItems {
    ...CartConfigurationItem
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment Payment on PaymentType {
  id
  outerId
  paymentGatewayCode
  currency {
    ...Currency
  }
  total {
    ...Money
  }
  billingAddress {
    ...CartAddress
  }
}
fragment Shipment on ShipmentType {
  id
  shipmentMethodCode
  shipmentMethodOption
  fulfillmentCenterId
  price {
    ...Money
  }
  currency {
    ...Currency
  }
  deliveryAddress {
    ...CartAddress
  }
}`) as unknown as TypedDocumentString<AddItemMutation, AddItemMutationVariables>;
export const AddItemsCartDocument = new TypedDocumentString(`
    mutation AddItemsCart($command: InputAddItemsType!) {
  addItemsCart(command: $command) {
    ...Cart
  }
}
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
fragment CartConfigurationItem on CartConfigurationItemType {
  id
  sectionId
  type
  productId
  name
  sku
  imageUrl
  quantity
  customText
  selectedForCheckout
}
fragment Cart on CartType {
  id
  storeId
  isAnonymous
  hasPhysicalProducts
  customerId
  itemsCount
  itemsQuantity
  total {
    ...Money
  }
  subTotal {
    ...Money
  }
  subTotalDiscount {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  items {
    ...LineItem
  }
  payments {
    ...Payment
  }
  shipments {
    ...Shipment
  }
  coupons {
    ...Coupon
  }
  gifts {
    ...GiftItem
  }
  addresses {
    ...CartAddress
  }
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
}
fragment Coupon on CouponType {
  code
  isAppliedSuccessfully
}
fragment Currency on CurrencyType {
  code
}
fragment GiftItem on GiftItemType {
  id
  quantity
  productId
  name
  lineItemId
}
fragment LineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  placedPrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
  selectedForCheckout
  isValid
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
  configurationItems {
    ...CartConfigurationItem
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment Payment on PaymentType {
  id
  outerId
  paymentGatewayCode
  currency {
    ...Currency
  }
  total {
    ...Money
  }
  billingAddress {
    ...CartAddress
  }
}
fragment Shipment on ShipmentType {
  id
  shipmentMethodCode
  shipmentMethodOption
  fulfillmentCenterId
  price {
    ...Money
  }
  currency {
    ...Currency
  }
  deliveryAddress {
    ...CartAddress
  }
}`) as unknown as TypedDocumentString<AddItemsCartMutation, AddItemsCartMutationVariables>;
export const AddOrUpdateCartPaymentDocument = new TypedDocumentString(`
    mutation AddOrUpdateCartPayment($command: InputAddOrUpdateCartPaymentType!) {
  addOrUpdateCartPayment(command: $command) {
    ...Cart
  }
}
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
fragment CartConfigurationItem on CartConfigurationItemType {
  id
  sectionId
  type
  productId
  name
  sku
  imageUrl
  quantity
  customText
  selectedForCheckout
}
fragment Cart on CartType {
  id
  storeId
  isAnonymous
  hasPhysicalProducts
  customerId
  itemsCount
  itemsQuantity
  total {
    ...Money
  }
  subTotal {
    ...Money
  }
  subTotalDiscount {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  items {
    ...LineItem
  }
  payments {
    ...Payment
  }
  shipments {
    ...Shipment
  }
  coupons {
    ...Coupon
  }
  gifts {
    ...GiftItem
  }
  addresses {
    ...CartAddress
  }
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
}
fragment Coupon on CouponType {
  code
  isAppliedSuccessfully
}
fragment Currency on CurrencyType {
  code
}
fragment GiftItem on GiftItemType {
  id
  quantity
  productId
  name
  lineItemId
}
fragment LineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  placedPrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
  selectedForCheckout
  isValid
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
  configurationItems {
    ...CartConfigurationItem
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment Payment on PaymentType {
  id
  outerId
  paymentGatewayCode
  currency {
    ...Currency
  }
  total {
    ...Money
  }
  billingAddress {
    ...CartAddress
  }
}
fragment Shipment on ShipmentType {
  id
  shipmentMethodCode
  shipmentMethodOption
  fulfillmentCenterId
  price {
    ...Money
  }
  currency {
    ...Currency
  }
  deliveryAddress {
    ...CartAddress
  }
}`) as unknown as TypedDocumentString<AddOrUpdateCartPaymentMutation, AddOrUpdateCartPaymentMutationVariables>;
export const AddOrUpdateCartShipmentDocument = new TypedDocumentString(`
    mutation AddOrUpdateCartShipment($command: InputAddOrUpdateCartShipmentType!) {
  addOrUpdateCartShipment(command: $command) {
    ...Cart
  }
}
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
fragment CartConfigurationItem on CartConfigurationItemType {
  id
  sectionId
  type
  productId
  name
  sku
  imageUrl
  quantity
  customText
  selectedForCheckout
}
fragment Cart on CartType {
  id
  storeId
  isAnonymous
  hasPhysicalProducts
  customerId
  itemsCount
  itemsQuantity
  total {
    ...Money
  }
  subTotal {
    ...Money
  }
  subTotalDiscount {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  items {
    ...LineItem
  }
  payments {
    ...Payment
  }
  shipments {
    ...Shipment
  }
  coupons {
    ...Coupon
  }
  gifts {
    ...GiftItem
  }
  addresses {
    ...CartAddress
  }
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
}
fragment Coupon on CouponType {
  code
  isAppliedSuccessfully
}
fragment Currency on CurrencyType {
  code
}
fragment GiftItem on GiftItemType {
  id
  quantity
  productId
  name
  lineItemId
}
fragment LineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  placedPrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
  selectedForCheckout
  isValid
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
  configurationItems {
    ...CartConfigurationItem
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment Payment on PaymentType {
  id
  outerId
  paymentGatewayCode
  currency {
    ...Currency
  }
  total {
    ...Money
  }
  billingAddress {
    ...CartAddress
  }
}
fragment Shipment on ShipmentType {
  id
  shipmentMethodCode
  shipmentMethodOption
  fulfillmentCenterId
  price {
    ...Money
  }
  currency {
    ...Currency
  }
  deliveryAddress {
    ...CartAddress
  }
}`) as unknown as TypedDocumentString<AddOrUpdateCartShipmentMutation, AddOrUpdateCartShipmentMutationVariables>;
export const ChangeCartConfiguredItemDocument = new TypedDocumentString(`
    mutation ChangeCartConfiguredItem($command: InputChangeCartConfiguredItemType!) {
  changeCartConfiguredItem(command: $command) {
    ...Cart
  }
}
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
fragment CartConfigurationItem on CartConfigurationItemType {
  id
  sectionId
  type
  productId
  name
  sku
  imageUrl
  quantity
  customText
  selectedForCheckout
}
fragment Cart on CartType {
  id
  storeId
  isAnonymous
  hasPhysicalProducts
  customerId
  itemsCount
  itemsQuantity
  total {
    ...Money
  }
  subTotal {
    ...Money
  }
  subTotalDiscount {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  items {
    ...LineItem
  }
  payments {
    ...Payment
  }
  shipments {
    ...Shipment
  }
  coupons {
    ...Coupon
  }
  gifts {
    ...GiftItem
  }
  addresses {
    ...CartAddress
  }
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
}
fragment Coupon on CouponType {
  code
  isAppliedSuccessfully
}
fragment Currency on CurrencyType {
  code
}
fragment GiftItem on GiftItemType {
  id
  quantity
  productId
  name
  lineItemId
}
fragment LineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  placedPrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
  selectedForCheckout
  isValid
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
  configurationItems {
    ...CartConfigurationItem
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment Payment on PaymentType {
  id
  outerId
  paymentGatewayCode
  currency {
    ...Currency
  }
  total {
    ...Money
  }
  billingAddress {
    ...CartAddress
  }
}
fragment Shipment on ShipmentType {
  id
  shipmentMethodCode
  shipmentMethodOption
  fulfillmentCenterId
  price {
    ...Money
  }
  currency {
    ...Currency
  }
  deliveryAddress {
    ...CartAddress
  }
}`) as unknown as TypedDocumentString<ChangeCartConfiguredItemMutation, ChangeCartConfiguredItemMutationVariables>;
export const ClearCartDocument = new TypedDocumentString(`
    mutation ClearCart($command: InputClearCartType!) {
  clearCart(command: $command) {
    ...Cart
  }
}
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
fragment CartConfigurationItem on CartConfigurationItemType {
  id
  sectionId
  type
  productId
  name
  sku
  imageUrl
  quantity
  customText
  selectedForCheckout
}
fragment Cart on CartType {
  id
  storeId
  isAnonymous
  hasPhysicalProducts
  customerId
  itemsCount
  itemsQuantity
  total {
    ...Money
  }
  subTotal {
    ...Money
  }
  subTotalDiscount {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  items {
    ...LineItem
  }
  payments {
    ...Payment
  }
  shipments {
    ...Shipment
  }
  coupons {
    ...Coupon
  }
  gifts {
    ...GiftItem
  }
  addresses {
    ...CartAddress
  }
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
}
fragment Coupon on CouponType {
  code
  isAppliedSuccessfully
}
fragment Currency on CurrencyType {
  code
}
fragment GiftItem on GiftItemType {
  id
  quantity
  productId
  name
  lineItemId
}
fragment LineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  placedPrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
  selectedForCheckout
  isValid
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
  configurationItems {
    ...CartConfigurationItem
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment Payment on PaymentType {
  id
  outerId
  paymentGatewayCode
  currency {
    ...Currency
  }
  total {
    ...Money
  }
  billingAddress {
    ...CartAddress
  }
}
fragment Shipment on ShipmentType {
  id
  shipmentMethodCode
  shipmentMethodOption
  fulfillmentCenterId
  price {
    ...Money
  }
  currency {
    ...Currency
  }
  deliveryAddress {
    ...CartAddress
  }
}`) as unknown as TypedDocumentString<ClearCartMutation, ClearCartMutationVariables>;
export const CreateOrderFromCartDocument = new TypedDocumentString(`
    mutation CreateOrderFromCart($command: InputCreateOrderFromCartType!) {
  createOrderFromCart(command: $command) {
    ...Order
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment OrderLineItem on OrderLineItemType {
  id
  name
  sku
  productId
  quantity
  price {
    ...Money
  }
  extendedPrice {
    ...Money
  }
}
fragment OrderPayment on PaymentInType {
  id
  number
  gatewayCode
  status
  sum {
    ...Money
  }
}
fragment OrderShipment on OrderShipmentType {
  id
  number
  shipmentMethodCode
  shipmentMethodOption
  status
  total {
    ...Money
  }
}
fragment Order on CustomerOrderType {
  id
  number
  status
  createdDate
  total {
    ...Money
  }
  items {
    ...OrderLineItem
  }
  inPayments {
    ...OrderPayment
  }
  shipments {
    ...OrderShipment
  }
}`) as unknown as TypedDocumentString<CreateOrderFromCartMutation, CreateOrderFromCartMutationVariables>;
export const GetCartLineValidationDocument = new TypedDocumentString(`
    query GetCartLineValidation($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String!, $cartId: String) {
  cart(
    storeId: $storeId
    userId: $userId
    currencyCode: $currencyCode
    cultureName: $cultureName
    cartId: $cartId
  ) {
    itemsCount
    items {
      id
      sku
      productId
      quantity
      isValid
      validationErrors {
        errorCode
        objectType
        objectId
        errorMessage
      }
    }
  }
}
    `) as unknown as TypedDocumentString<GetCartLineValidationQuery, GetCartLineValidationQueryVariables>;
export const GetCartValidationAliasedDocument = new TypedDocumentString(`
    query GetCartValidationAliased($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String!, $ruleSetA: String, $ruleSetB: String, $cartId: String) {
  cart(
    storeId: $storeId
    userId: $userId
    currencyCode: $currencyCode
    cultureName: $cultureName
    cartId: $cartId
  ) {
    itemsCount
    errorsA: validationErrors(ruleSet: $ruleSetA) {
      errorCode
      objectType
      objectId
      errorMessage
    }
    errorsB: validationErrors(ruleSet: $ruleSetB) {
      errorCode
      objectType
      objectId
      errorMessage
    }
  }
}
    `) as unknown as TypedDocumentString<GetCartValidationAliasedQuery, GetCartValidationAliasedQueryVariables>;
export const GetCartValidationDocument = new TypedDocumentString(`
    query GetCartValidation($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String!, $ruleSet: String, $cartId: String) {
  cart(
    storeId: $storeId
    userId: $userId
    currencyCode: $currencyCode
    cultureName: $cultureName
    cartId: $cartId
  ) {
    itemsCount
    validationErrors(ruleSet: $ruleSet) {
      errorCode
      objectType
      objectId
      errorMessage
    }
    items {
      id
      sku
      productId
      quantity
      isValid
      validationErrors {
        errorCode
        objectType
        objectId
        errorMessage
      }
    }
  }
}
    `) as unknown as TypedDocumentString<GetCartValidationQuery, GetCartValidationQueryVariables>;
export const GetCartDocument = new TypedDocumentString(`
    query GetCart($storeId: String!, $userId: String!, $currencyCode: String!, $cultureName: String!, $cartId: String, $cartName: String) {
  cart(
    storeId: $storeId
    userId: $userId
    currencyCode: $currencyCode
    cultureName: $cultureName
    cartId: $cartId
    cartName: $cartName
  ) {
    ...Cart
  }
}
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
fragment CartConfigurationItem on CartConfigurationItemType {
  id
  sectionId
  type
  productId
  name
  sku
  imageUrl
  quantity
  customText
  selectedForCheckout
}
fragment Cart on CartType {
  id
  storeId
  isAnonymous
  hasPhysicalProducts
  customerId
  itemsCount
  itemsQuantity
  total {
    ...Money
  }
  subTotal {
    ...Money
  }
  subTotalDiscount {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  items {
    ...LineItem
  }
  payments {
    ...Payment
  }
  shipments {
    ...Shipment
  }
  coupons {
    ...Coupon
  }
  gifts {
    ...GiftItem
  }
  addresses {
    ...CartAddress
  }
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
}
fragment Coupon on CouponType {
  code
  isAppliedSuccessfully
}
fragment Currency on CurrencyType {
  code
}
fragment GiftItem on GiftItemType {
  id
  quantity
  productId
  name
  lineItemId
}
fragment LineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  placedPrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
  selectedForCheckout
  isValid
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
  configurationItems {
    ...CartConfigurationItem
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment Payment on PaymentType {
  id
  outerId
  paymentGatewayCode
  currency {
    ...Currency
  }
  total {
    ...Money
  }
  billingAddress {
    ...CartAddress
  }
}
fragment Shipment on ShipmentType {
  id
  shipmentMethodCode
  shipmentMethodOption
  fulfillmentCenterId
  price {
    ...Money
  }
  currency {
    ...Currency
  }
  deliveryAddress {
    ...CartAddress
  }
}`) as unknown as TypedDocumentString<GetCartQuery, GetCartQueryVariables>;
export const MergeCartDocument = new TypedDocumentString(`
    mutation MergeCart($command: InputMergeCartType!) {
  mergeCart(command: $command) {
    ...Cart
  }
}
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
fragment CartConfigurationItem on CartConfigurationItemType {
  id
  sectionId
  type
  productId
  name
  sku
  imageUrl
  quantity
  customText
  selectedForCheckout
}
fragment Cart on CartType {
  id
  storeId
  isAnonymous
  hasPhysicalProducts
  customerId
  itemsCount
  itemsQuantity
  total {
    ...Money
  }
  subTotal {
    ...Money
  }
  subTotalDiscount {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  items {
    ...LineItem
  }
  payments {
    ...Payment
  }
  shipments {
    ...Shipment
  }
  coupons {
    ...Coupon
  }
  gifts {
    ...GiftItem
  }
  addresses {
    ...CartAddress
  }
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
}
fragment Coupon on CouponType {
  code
  isAppliedSuccessfully
}
fragment Currency on CurrencyType {
  code
}
fragment GiftItem on GiftItemType {
  id
  quantity
  productId
  name
  lineItemId
}
fragment LineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  placedPrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
  selectedForCheckout
  isValid
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
  configurationItems {
    ...CartConfigurationItem
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment Payment on PaymentType {
  id
  outerId
  paymentGatewayCode
  currency {
    ...Currency
  }
  total {
    ...Money
  }
  billingAddress {
    ...CartAddress
  }
}
fragment Shipment on ShipmentType {
  id
  shipmentMethodCode
  shipmentMethodOption
  fulfillmentCenterId
  price {
    ...Money
  }
  currency {
    ...Currency
  }
  deliveryAddress {
    ...CartAddress
  }
}`) as unknown as TypedDocumentString<MergeCartMutation, MergeCartMutationVariables>;
export const RemoveCartItemDocument = new TypedDocumentString(`
    mutation RemoveCartItem($command: InputRemoveItemType!) {
  removeCartItem(command: $command) {
    ...Cart
  }
}
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
fragment CartConfigurationItem on CartConfigurationItemType {
  id
  sectionId
  type
  productId
  name
  sku
  imageUrl
  quantity
  customText
  selectedForCheckout
}
fragment Cart on CartType {
  id
  storeId
  isAnonymous
  hasPhysicalProducts
  customerId
  itemsCount
  itemsQuantity
  total {
    ...Money
  }
  subTotal {
    ...Money
  }
  subTotalDiscount {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  items {
    ...LineItem
  }
  payments {
    ...Payment
  }
  shipments {
    ...Shipment
  }
  coupons {
    ...Coupon
  }
  gifts {
    ...GiftItem
  }
  addresses {
    ...CartAddress
  }
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
}
fragment Coupon on CouponType {
  code
  isAppliedSuccessfully
}
fragment Currency on CurrencyType {
  code
}
fragment GiftItem on GiftItemType {
  id
  quantity
  productId
  name
  lineItemId
}
fragment LineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  placedPrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
  selectedForCheckout
  isValid
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
  configurationItems {
    ...CartConfigurationItem
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment Payment on PaymentType {
  id
  outerId
  paymentGatewayCode
  currency {
    ...Currency
  }
  total {
    ...Money
  }
  billingAddress {
    ...CartAddress
  }
}
fragment Shipment on ShipmentType {
  id
  shipmentMethodCode
  shipmentMethodOption
  fulfillmentCenterId
  price {
    ...Money
  }
  currency {
    ...Currency
  }
  deliveryAddress {
    ...CartAddress
  }
}`) as unknown as TypedDocumentString<RemoveCartItemMutation, RemoveCartItemMutationVariables>;
export const RemoveCartDocument = new TypedDocumentString(`
    mutation RemoveCart($command: InputRemoveCartType!) {
  removeCart(command: $command)
}
    `) as unknown as TypedDocumentString<RemoveCartMutation, RemoveCartMutationVariables>;
export const RemoveCouponDocument = new TypedDocumentString(`
    mutation RemoveCoupon($command: InputRemoveCouponType!) {
  removeCoupon(command: $command) {
    ...Cart
  }
}
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
fragment CartConfigurationItem on CartConfigurationItemType {
  id
  sectionId
  type
  productId
  name
  sku
  imageUrl
  quantity
  customText
  selectedForCheckout
}
fragment Cart on CartType {
  id
  storeId
  isAnonymous
  hasPhysicalProducts
  customerId
  itemsCount
  itemsQuantity
  total {
    ...Money
  }
  subTotal {
    ...Money
  }
  subTotalDiscount {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  items {
    ...LineItem
  }
  payments {
    ...Payment
  }
  shipments {
    ...Shipment
  }
  coupons {
    ...Coupon
  }
  gifts {
    ...GiftItem
  }
  addresses {
    ...CartAddress
  }
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
}
fragment Coupon on CouponType {
  code
  isAppliedSuccessfully
}
fragment Currency on CurrencyType {
  code
}
fragment GiftItem on GiftItemType {
  id
  quantity
  productId
  name
  lineItemId
}
fragment LineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  placedPrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
  selectedForCheckout
  isValid
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
  configurationItems {
    ...CartConfigurationItem
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment Payment on PaymentType {
  id
  outerId
  paymentGatewayCode
  currency {
    ...Currency
  }
  total {
    ...Money
  }
  billingAddress {
    ...CartAddress
  }
}
fragment Shipment on ShipmentType {
  id
  shipmentMethodCode
  shipmentMethodOption
  fulfillmentCenterId
  price {
    ...Money
  }
  currency {
    ...Currency
  }
  deliveryAddress {
    ...CartAddress
  }
}`) as unknown as TypedDocumentString<RemoveCouponMutation, RemoveCouponMutationVariables>;
export const SelectCartItemsDocument = new TypedDocumentString(`
    mutation SelectCartItems($command: InputChangeCartItemsSelectedType!) {
  selectCartItems(command: $command) {
    ...Cart
  }
}
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
fragment CartConfigurationItem on CartConfigurationItemType {
  id
  sectionId
  type
  productId
  name
  sku
  imageUrl
  quantity
  customText
  selectedForCheckout
}
fragment Cart on CartType {
  id
  storeId
  isAnonymous
  hasPhysicalProducts
  customerId
  itemsCount
  itemsQuantity
  total {
    ...Money
  }
  subTotal {
    ...Money
  }
  subTotalDiscount {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  items {
    ...LineItem
  }
  payments {
    ...Payment
  }
  shipments {
    ...Shipment
  }
  coupons {
    ...Coupon
  }
  gifts {
    ...GiftItem
  }
  addresses {
    ...CartAddress
  }
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
}
fragment Coupon on CouponType {
  code
  isAppliedSuccessfully
}
fragment Currency on CurrencyType {
  code
}
fragment GiftItem on GiftItemType {
  id
  quantity
  productId
  name
  lineItemId
}
fragment LineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  placedPrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
  selectedForCheckout
  isValid
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
  configurationItems {
    ...CartConfigurationItem
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment Payment on PaymentType {
  id
  outerId
  paymentGatewayCode
  currency {
    ...Currency
  }
  total {
    ...Money
  }
  billingAddress {
    ...CartAddress
  }
}
fragment Shipment on ShipmentType {
  id
  shipmentMethodCode
  shipmentMethodOption
  fulfillmentCenterId
  price {
    ...Money
  }
  currency {
    ...Currency
  }
  deliveryAddress {
    ...CartAddress
  }
}`) as unknown as TypedDocumentString<SelectCartItemsMutation, SelectCartItemsMutationVariables>;
export const UnSelectAllCartItemsDocument = new TypedDocumentString(`
    mutation UnSelectAllCartItems($command: InputChangeAllCartItemsSelectedType!) {
  unSelectAllCartItems(command: $command) {
    ...Cart
  }
}
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
fragment CartConfigurationItem on CartConfigurationItemType {
  id
  sectionId
  type
  productId
  name
  sku
  imageUrl
  quantity
  customText
  selectedForCheckout
}
fragment Cart on CartType {
  id
  storeId
  isAnonymous
  hasPhysicalProducts
  customerId
  itemsCount
  itemsQuantity
  total {
    ...Money
  }
  subTotal {
    ...Money
  }
  subTotalDiscount {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  items {
    ...LineItem
  }
  payments {
    ...Payment
  }
  shipments {
    ...Shipment
  }
  coupons {
    ...Coupon
  }
  gifts {
    ...GiftItem
  }
  addresses {
    ...CartAddress
  }
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
}
fragment Coupon on CouponType {
  code
  isAppliedSuccessfully
}
fragment Currency on CurrencyType {
  code
}
fragment GiftItem on GiftItemType {
  id
  quantity
  productId
  name
  lineItemId
}
fragment LineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  placedPrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
  selectedForCheckout
  isValid
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
  configurationItems {
    ...CartConfigurationItem
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment Payment on PaymentType {
  id
  outerId
  paymentGatewayCode
  currency {
    ...Currency
  }
  total {
    ...Money
  }
  billingAddress {
    ...CartAddress
  }
}
fragment Shipment on ShipmentType {
  id
  shipmentMethodCode
  shipmentMethodOption
  fulfillmentCenterId
  price {
    ...Money
  }
  currency {
    ...Currency
  }
  deliveryAddress {
    ...CartAddress
  }
}`) as unknown as TypedDocumentString<UnSelectAllCartItemsMutation, UnSelectAllCartItemsMutationVariables>;
export const UnSelectCartItemsDocument = new TypedDocumentString(`
    mutation UnSelectCartItems($command: InputChangeCartItemsSelectedType!) {
  unSelectCartItems(command: $command) {
    ...Cart
  }
}
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
fragment CartConfigurationItem on CartConfigurationItemType {
  id
  sectionId
  type
  productId
  name
  sku
  imageUrl
  quantity
  customText
  selectedForCheckout
}
fragment Cart on CartType {
  id
  storeId
  isAnonymous
  hasPhysicalProducts
  customerId
  itemsCount
  itemsQuantity
  total {
    ...Money
  }
  subTotal {
    ...Money
  }
  subTotalDiscount {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  items {
    ...LineItem
  }
  payments {
    ...Payment
  }
  shipments {
    ...Shipment
  }
  coupons {
    ...Coupon
  }
  gifts {
    ...GiftItem
  }
  addresses {
    ...CartAddress
  }
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
}
fragment Coupon on CouponType {
  code
  isAppliedSuccessfully
}
fragment Currency on CurrencyType {
  code
}
fragment GiftItem on GiftItemType {
  id
  quantity
  productId
  name
  lineItemId
}
fragment LineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  placedPrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
  selectedForCheckout
  isValid
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
  configurationItems {
    ...CartConfigurationItem
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment Payment on PaymentType {
  id
  outerId
  paymentGatewayCode
  currency {
    ...Currency
  }
  total {
    ...Money
  }
  billingAddress {
    ...CartAddress
  }
}
fragment Shipment on ShipmentType {
  id
  shipmentMethodCode
  shipmentMethodOption
  fulfillmentCenterId
  price {
    ...Money
  }
  currency {
    ...Currency
  }
  deliveryAddress {
    ...CartAddress
  }
}`) as unknown as TypedDocumentString<UnSelectCartItemsMutation, UnSelectCartItemsMutationVariables>;
export const UpdateCartQuantityDocument = new TypedDocumentString(`
    mutation UpdateCartQuantity($command: InputUpdateCartQuantity!) {
  updateCartQuantity(command: $command) {
    ...Cart
  }
}
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
fragment CartConfigurationItem on CartConfigurationItemType {
  id
  sectionId
  type
  productId
  name
  sku
  imageUrl
  quantity
  customText
  selectedForCheckout
}
fragment Cart on CartType {
  id
  storeId
  isAnonymous
  hasPhysicalProducts
  customerId
  itemsCount
  itemsQuantity
  total {
    ...Money
  }
  subTotal {
    ...Money
  }
  subTotalDiscount {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  items {
    ...LineItem
  }
  payments {
    ...Payment
  }
  shipments {
    ...Shipment
  }
  coupons {
    ...Coupon
  }
  gifts {
    ...GiftItem
  }
  addresses {
    ...CartAddress
  }
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
}
fragment Coupon on CouponType {
  code
  isAppliedSuccessfully
}
fragment Currency on CurrencyType {
  code
}
fragment GiftItem on GiftItemType {
  id
  quantity
  productId
  name
  lineItemId
}
fragment LineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  placedPrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
  selectedForCheckout
  isValid
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
  configurationItems {
    ...CartConfigurationItem
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment Payment on PaymentType {
  id
  outerId
  paymentGatewayCode
  currency {
    ...Currency
  }
  total {
    ...Money
  }
  billingAddress {
    ...CartAddress
  }
}
fragment Shipment on ShipmentType {
  id
  shipmentMethodCode
  shipmentMethodOption
  fulfillmentCenterId
  price {
    ...Money
  }
  currency {
    ...Currency
  }
  deliveryAddress {
    ...CartAddress
  }
}`) as unknown as TypedDocumentString<UpdateCartQuantityMutation, UpdateCartQuantityMutationVariables>;
export const CategoriesDocument = new TypedDocumentString(`
    query Categories($storeId: String!, $userId: String, $cultureName: String, $currencyCode: String, $filter: String, $first: Int) {
  categories(
    storeId: $storeId
    userId: $userId
    cultureName: $cultureName
    currencyCode: $currencyCode
    filter: $filter
    first: $first
  ) {
    totalCount
    items {
      ...Category
    }
  }
}
    fragment Category on Category {
  id
  code
  name
  outline
  slug
}`) as unknown as TypedDocumentString<CategoriesQuery, CategoriesQueryVariables>;
export const CategoryDocument = new TypedDocumentString(`
    query Category($id: String!, $storeId: String!, $userId: String, $cultureName: String, $currencyCode: String) {
  category(
    id: $id
    storeId: $storeId
    userId: $userId
    cultureName: $cultureName
    currencyCode: $currencyCode
  ) {
    ...Category
  }
}
    fragment Category on Category {
  id
  code
  name
  outline
  slug
}`) as unknown as TypedDocumentString<CategoryQuery, CategoryQueryVariables>;
export const AddAddressToFavoritesDocument = new TypedDocumentString(`
    mutation AddAddressToFavorites($command: AddAddressToFavoritesCommandType!) {
  addAddressToFavorites(command: $command)
}
    `) as unknown as TypedDocumentString<AddAddressToFavoritesMutation, AddAddressToFavoritesMutationVariables>;
export const ChangeOrganizationContactRoleDocument = new TypedDocumentString(`
    mutation ChangeOrganizationContactRole($command: InputChangeOrganizationContactRoleType!) {
  changeOrganizationContactRole(command: $command) {
    ...CustomIdentityResult
  }
}
    fragment CustomIdentityResult on CustomIdentityResultType {
  succeeded
  errors {
    code
    parameter
    description
  }
}`) as unknown as TypedDocumentString<
  ChangeOrganizationContactRoleMutation,
  ChangeOrganizationContactRoleMutationVariables
>;
export const DeleteContactDocument = new TypedDocumentString(`
    mutation DeleteContact($command: InputDeleteContactType!) {
  deleteContact(command: $command)
}
    `) as unknown as TypedDocumentString<DeleteContactMutation, DeleteContactMutationVariables>;
export const DeleteMemberAddressesDocument = new TypedDocumentString(`
    mutation DeleteMemberAddresses($command: InputDeleteMemberAddressType!) {
  deleteMemberAddresses(command: $command) {
    addresses {
      items {
        ...MemberAddress
      }
    }
  }
}
    fragment MemberAddress on MemberAddressType {
  id
  key
  isDefault
  isFavorite
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}`) as unknown as TypedDocumentString<DeleteMemberAddressesMutation, DeleteMemberAddressesMutationVariables>;
export const GetContactAddressesDocument = new TypedDocumentString(`
    query GetContactAddresses($id: String!) {
  contact(id: $id) {
    addresses {
      items {
        ...MemberAddress
      }
    }
  }
}
    fragment MemberAddress on MemberAddressType {
  id
  key
  isDefault
  isFavorite
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}`) as unknown as TypedDocumentString<GetContactAddressesQuery, GetContactAddressesQueryVariables>;
export const GetContactLockStatusDocument = new TypedDocumentString(`
    query GetContactLockStatus($id: String!) {
  contact(id: $id) {
    isLockedInOrganization
  }
}
    `) as unknown as TypedDocumentString<GetContactLockStatusQuery, GetContactLockStatusQueryVariables>;
export const GetContactRolesInOrganizationDocument = new TypedDocumentString(`
    query GetContactRolesInOrganization($id: String!) {
  contact(id: $id) {
    rolesInOrganization {
      id
      name
    }
  }
}
    `) as unknown as TypedDocumentString<
  GetContactRolesInOrganizationQuery,
  GetContactRolesInOrganizationQueryVariables
>;
export const GetContactDocument = new TypedDocumentString(`
    query GetContact($id: String!) {
  contact(id: $id) {
    ...Contact
  }
}
    fragment Contact on ContactType {
  id
  firstName
  lastName
  fullName
  status
  organizationId
  organizationsIds
  securityAccounts {
    ...User
  }
}
fragment Role on RoleType {
  id
  name
  normalizedName
}
fragment User on UserType {
  id
  userName
  email
  emailConfirmed
  isAdministrator
  memberId
  storeId
  roles {
    ...Role
  }
}`) as unknown as TypedDocumentString<GetContactQuery, GetContactQueryVariables>;
export const GetCurrentCustomerAddressesDocument = new TypedDocumentString(`
    query GetCurrentCustomerAddresses($after: String, $first: Int, $countryCodes: [String], $regionIds: [String], $cities: [String], $keyword: String, $sort: String) {
  currentCustomerAddresses(
    after: $after
    first: $first
    countryCodes: $countryCodes
    regionIds: $regionIds
    cities: $cities
    keyword: $keyword
    sort: $sort
  ) {
    totalCount
    items {
      ...MemberAddress
    }
  }
}
    fragment MemberAddress on MemberAddressType {
  id
  key
  isDefault
  isFavorite
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}`) as unknown as TypedDocumentString<GetCurrentCustomerAddressesQuery, GetCurrentCustomerAddressesQueryVariables>;
export const GetCurrentOrganizationAddressesDocument = new TypedDocumentString(`
    query GetCurrentOrganizationAddresses($after: String, $first: Int, $countryCodes: [String], $regionIds: [String], $cities: [String], $keyword: String, $sort: String) {
  currentOrganizationAddresses(
    after: $after
    first: $first
    countryCodes: $countryCodes
    regionIds: $regionIds
    cities: $cities
    keyword: $keyword
    sort: $sort
  ) {
    totalCount
    items {
      ...MemberAddress
    }
  }
}
    fragment MemberAddress on MemberAddressType {
  id
  key
  isDefault
  isFavorite
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}`) as unknown as TypedDocumentString<
  GetCurrentOrganizationAddressesQuery,
  GetCurrentOrganizationAddressesQueryVariables
>;
export const GetOrganizationContactsDocument = new TypedDocumentString(`
    query GetOrganizationContacts($organizationId: String!, $searchPhrase: String, $sort: String, $first: Int, $after: String) {
  organization(id: $organizationId) {
    contacts(searchPhrase: $searchPhrase, sort: $sort, first: $first, after: $after) {
      items {
        ...Contact
      }
    }
  }
}
    fragment Contact on ContactType {
  id
  firstName
  lastName
  fullName
  status
  organizationId
  organizationsIds
  securityAccounts {
    ...User
  }
}
fragment Role on RoleType {
  id
  name
  normalizedName
}
fragment User on UserType {
  id
  userName
  email
  emailConfirmed
  isAdministrator
  memberId
  storeId
  roles {
    ...Role
  }
}`) as unknown as TypedDocumentString<GetOrganizationContactsQuery, GetOrganizationContactsQueryVariables>;
export const GetOrganizationsDocument = new TypedDocumentString(`
    query GetOrganizations($after: String, $first: Int, $sort: String, $searchPhrase: String, $statuses: [String]) {
  me {
    contact {
      organizations(
        after: $after
        first: $first
        sort: $sort
        searchPhrase: $searchPhrase
        statuses: $statuses
      ) {
        items {
          id
          name
          isLockedForCurrentUser
        }
        totalCount
        pageInfo {
          hasNextPage
          endCursor
        }
      }
    }
  }
}
    `) as unknown as TypedDocumentString<GetOrganizationsQuery, GetOrganizationsQueryVariables>;
export const LockOrganizationContactDocument = new TypedDocumentString(`
    mutation LockOrganizationContact($command: InputLockUnlockOrganizationContactType!) {
  lockOrganizationContact(command: $command) {
    ...Contact
  }
}
    fragment Contact on ContactType {
  id
  firstName
  lastName
  fullName
  status
  organizationId
  organizationsIds
  securityAccounts {
    ...User
  }
}
fragment Role on RoleType {
  id
  name
  normalizedName
}
fragment User on UserType {
  id
  userName
  email
  emailConfirmed
  isAdministrator
  memberId
  storeId
  roles {
    ...Role
  }
}`) as unknown as TypedDocumentString<LockOrganizationContactMutation, LockOrganizationContactMutationVariables>;
export const RemoveAddressFromFavoritesDocument = new TypedDocumentString(`
    mutation RemoveAddressFromFavorites($command: RemoveAddressFromFavoritesCommandType!) {
  removeAddressFromFavorites(command: $command)
}
    `) as unknown as TypedDocumentString<
  RemoveAddressFromFavoritesMutation,
  RemoveAddressFromFavoritesMutationVariables
>;
export const RequestRegistrationDocument = new TypedDocumentString(`
    mutation RequestRegistration($command: InputRequestRegistrationType!) {
  requestRegistration(command: $command) {
    contact {
      id
      firstName
      lastName
      status
    }
    organization {
      id
      name
      status
      ownerId
    }
    account {
      id
      username
      email
      status
    }
    result {
      succeeded
      requireEmailVerification
    }
  }
}
    `) as unknown as TypedDocumentString<RequestRegistrationMutation, RequestRegistrationMutationVariables>;
export const UnlockOrganizationContactDocument = new TypedDocumentString(`
    mutation UnlockOrganizationContact($command: InputLockUnlockOrganizationContactType!) {
  unlockOrganizationContact(command: $command) {
    ...Contact
  }
}
    fragment Contact on ContactType {
  id
  firstName
  lastName
  fullName
  status
  organizationId
  organizationsIds
  securityAccounts {
    ...User
  }
}
fragment Role on RoleType {
  id
  name
  normalizedName
}
fragment User on UserType {
  id
  userName
  email
  emailConfirmed
  isAdministrator
  memberId
  storeId
  roles {
    ...Role
  }
}`) as unknown as TypedDocumentString<UnlockOrganizationContactMutation, UnlockOrganizationContactMutationVariables>;
export const UpdateMemberAddressesDocument = new TypedDocumentString(`
    mutation UpdateMemberAddresses($command: InputUpdateMemberAddressType!) {
  updateMemberAddresses(command: $command) {
    addresses {
      items {
        ...MemberAddress
      }
    }
  }
}
    fragment MemberAddress on MemberAddressType {
  id
  key
  isDefault
  isFavorite
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}`) as unknown as TypedDocumentString<UpdateMemberAddressesMutation, UpdateMemberAddressesMutationVariables>;
export const OrderDocument = new TypedDocumentString(`
    query Order($number: String, $cultureName: String) {
  order(number: $number, cultureName: $cultureName) {
    ...Order
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment OrderLineItem on OrderLineItemType {
  id
  name
  sku
  productId
  quantity
  price {
    ...Money
  }
  extendedPrice {
    ...Money
  }
}
fragment OrderPayment on PaymentInType {
  id
  number
  gatewayCode
  status
  sum {
    ...Money
  }
}
fragment OrderShipment on OrderShipmentType {
  id
  number
  shipmentMethodCode
  shipmentMethodOption
  status
  total {
    ...Money
  }
}
fragment Order on CustomerOrderType {
  id
  number
  status
  createdDate
  total {
    ...Money
  }
  items {
    ...OrderLineItem
  }
  inPayments {
    ...OrderPayment
  }
  shipments {
    ...OrderShipment
  }
}`) as unknown as TypedDocumentString<OrderQuery, OrderQueryVariables>;
export const OrdersDocument = new TypedDocumentString(`
    query Orders($userId: String, $filter: String, $sort: String, $cultureName: String, $first: Int, $after: String) {
  orders(
    userId: $userId
    filter: $filter
    sort: $sort
    cultureName: $cultureName
    first: $first
    after: $after
  ) {
    items {
      ...Order
    }
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment OrderLineItem on OrderLineItemType {
  id
  name
  sku
  productId
  quantity
  price {
    ...Money
  }
  extendedPrice {
    ...Money
  }
}
fragment OrderPayment on PaymentInType {
  id
  number
  gatewayCode
  status
  sum {
    ...Money
  }
}
fragment OrderShipment on OrderShipmentType {
  id
  number
  shipmentMethodCode
  shipmentMethodOption
  status
  total {
    ...Money
  }
}
fragment Order on CustomerOrderType {
  id
  number
  status
  createdDate
  total {
    ...Money
  }
  items {
    ...OrderLineItem
  }
  inPayments {
    ...OrderPayment
  }
  shipments {
    ...OrderShipment
  }
}`) as unknown as TypedDocumentString<OrdersQuery, OrdersQueryVariables>;
export const OrganizationOrdersDocument = new TypedDocumentString(`
    query OrganizationOrders($organizationId: String, $filter: String, $sort: String, $cultureName: String, $first: Int, $after: String) {
  organizationOrders(
    organizationId: $organizationId
    filter: $filter
    sort: $sort
    cultureName: $cultureName
    first: $first
    after: $after
  ) {
    items {
      ...Order
    }
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment OrderLineItem on OrderLineItemType {
  id
  name
  sku
  productId
  quantity
  price {
    ...Money
  }
  extendedPrice {
    ...Money
  }
}
fragment OrderPayment on PaymentInType {
  id
  number
  gatewayCode
  status
  sum {
    ...Money
  }
}
fragment OrderShipment on OrderShipmentType {
  id
  number
  shipmentMethodCode
  shipmentMethodOption
  status
  total {
    ...Money
  }
}
fragment Order on CustomerOrderType {
  id
  number
  status
  createdDate
  total {
    ...Money
  }
  items {
    ...OrderLineItem
  }
  inPayments {
    ...OrderPayment
  }
  shipments {
    ...OrderShipment
  }
}`) as unknown as TypedDocumentString<OrganizationOrdersQuery, OrganizationOrdersQueryVariables>;
export const PageContextDocument = new TypedDocumentString(`
    query PageContext($storeId: String, $userId: String, $cultureName: String, $permalink: String, $organizationId: String) {
  pageContext(
    storeId: $storeId
    userId: $userId
    cultureName: $cultureName
    permalink: $permalink
    organizationId: $organizationId
  ) {
    ...PageContext
  }
}
    fragment Currency on CurrencyType {
  code
}
fragment Language on LanguageType {
  cultureName
  nativeName
}
fragment MenuLink on MenuLinkType {
  title
  url
  priority
}
fragment PageContext on PageContextResponseType {
  slugInfo {
    ...SlugInfo
  }
  store {
    ...StoreInfo
  }
  whiteLabelingSettings {
    ...WhiteLabelingSettings
  }
  user {
    ...User
  }
}
fragment Role on RoleType {
  id
  name
  normalizedName
}
fragment SeoInfo on SeoInfo {
  id
  name
  semanticUrl
  outline
  pageTitle
  metaDescription
  imageAltDescription
  metaKeywords
  storeId
  objectId
  objectType
  isActive
  languageCode
}
fragment SlugInfo on SlugInfoResponseType {
  entityInfo {
    ...SeoInfo
  }
  redirectUrl
}
fragment StoreInfo on StoreResponseType {
  storeId
  storeName
  catalogId
  storeUrl
  defaultLanguage {
    ...Language
  }
  availableLanguages {
    ...Language
  }
  defaultCurrency {
    ...Currency
  }
  availableCurrencies {
    ...Currency
  }
  settings {
    ...StoreSettings
  }
}
fragment StoreSettings on StoreSettingsType {
  anonymousUsersAllowed
  taxCalculationEnabled
  seoLinkType
}
fragment User on UserType {
  id
  userName
  email
  emailConfirmed
  isAdministrator
  memberId
  storeId
  roles {
    ...Role
  }
}
fragment WhiteLabelingSettings on WhiteLabelingSettingsType {
  logoUrl
  secondaryLogoUrl
  faviconUrl
  themePresetName
  footerLinks {
    ...MenuLink
  }
  mainMenuLinks {
    ...MenuLink
  }
}`) as unknown as TypedDocumentString<PageContextQuery, PageContextQueryVariables>;
export const CartPickupLocationsDocument = new TypedDocumentString(`
    query CartPickupLocations($cartId: String!, $storeId: String!, $cultureName: String!, $keyword: String, $sort: String, $first: Int, $after: String, $facet: String, $filter: String) {
  cartPickupLocations(
    cartId: $cartId
    storeId: $storeId
    cultureName: $cultureName
    keyword: $keyword
    sort: $sort
    first: $first
    after: $after
    facet: $facet
    filter: $filter
  ) {
    items {
      ...ProductPickupLocation
    }
  }
}
    fragment PickupLocationAddress on PickupLocationAddressType {
  id
  key
  name
  organization
  countryCode
  countryName
  city
  postalCode
  line1
  line2
  regionId
  regionName
  phone
  email
  outerId
  description
  addressType
}
fragment ProductPickupLocation on ProductPickupLocation {
  id
  isActive
  name
  description
  contactEmail
  contactPhone
  workingHours
  deliveryDays
  storageDays
  geoLocation
  address {
    ...PickupLocationAddress
  }
  availabilityType
  availabilityNote
  availableQuantity
}`) as unknown as TypedDocumentString<CartPickupLocationsQuery, CartPickupLocationsQueryVariables>;
export const PickupLocationsDocument = new TypedDocumentString(`
    query PickupLocations($storeId: String, $keyword: String, $sort: String, $first: Int, $after: String) {
  pickupLocations(
    storeId: $storeId
    keyword: $keyword
    sort: $sort
    first: $first
    after: $after
  ) {
    items {
      ...PickupLocation
    }
  }
}
    fragment PickupAddress on PickupAddressType {
  id
  key
  name
  organization
  countryCode
  countryName
  city
  postalCode
  line1
  line2
  regionId
  regionName
  phone
  email
  outerId
  description
  addressType
}
fragment PickupLocation on PickupLocationType {
  id
  isActive
  name
  description
  contactEmail
  contactPhone
  workingHours
  geoLocation
  address {
    ...PickupAddress
  }
}`) as unknown as TypedDocumentString<PickupLocationsQuery, PickupLocationsQueryVariables>;
export const ProductPickupLocationsDocument = new TypedDocumentString(`
    query ProductPickupLocations($productId: String!, $storeId: String!, $cultureName: String!, $keyword: String, $sort: String, $first: Int, $after: String) {
  productPickupLocations(
    productId: $productId
    storeId: $storeId
    cultureName: $cultureName
    keyword: $keyword
    sort: $sort
    first: $first
    after: $after
  ) {
    items {
      ...ProductPickupLocation
    }
  }
}
    fragment PickupLocationAddress on PickupLocationAddressType {
  id
  key
  name
  organization
  countryCode
  countryName
  city
  postalCode
  line1
  line2
  regionId
  regionName
  phone
  email
  outerId
  description
  addressType
}
fragment ProductPickupLocation on ProductPickupLocation {
  id
  isActive
  name
  description
  contactEmail
  contactPhone
  workingHours
  deliveryDays
  storageDays
  geoLocation
  address {
    ...PickupLocationAddress
  }
  availabilityType
  availabilityNote
  availableQuantity
}`) as unknown as TypedDocumentString<ProductPickupLocationsQuery, ProductPickupLocationsQueryVariables>;
export const CreateConfiguredLineItemDocument = new TypedDocumentString(`
    mutation CreateConfiguredLineItem($command: InputCreateConfiguredLineItemCommand!) {
  createConfiguredLineItem(command: $command) {
    ...ConfigurationLineItem
  }
}
    fragment ConfigurationLineItem on ConfigurationLineItemType {
  id
  text
  quantity
  product {
    ...Product
  }
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment ProductPrice on PriceType {
  list {
    ...Money
  }
  actual {
    ...Money
  }
}
fragment Product on Product {
  id
  code
  productType
  isConfigurable
  name
  vendor {
    ...Vendor
  }
  price {
    ...ProductPrice
  }
}
fragment Vendor on CommonVendor {
  id
  name
}`) as unknown as TypedDocumentString<CreateConfiguredLineItemMutation, CreateConfiguredLineItemMutationVariables>;
export const ProductConfigurationDocument = new TypedDocumentString(`
    query ProductConfiguration($configurableProductId: String!, $storeId: String!, $userId: String, $cultureName: String, $currencyCode: String) {
  productConfiguration(
    configurableProductId: $configurableProductId
    storeId: $storeId
    userId: $userId
    cultureName: $cultureName
    currencyCode: $currencyCode
  ) {
    ...ProductConfiguration
  }
}
    fragment ConfigurationLineItem on ConfigurationLineItemType {
  id
  text
  quantity
  product {
    ...Product
  }
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment ProductConfiguration on ConfigurationQueryResponseType {
  configurationSections {
    id
    name
    description
    isRequired
    type
    allowCustomText
    allowTextOptions
    maxLength
    options {
      ...ConfigurationLineItem
    }
  }
}
fragment ProductPrice on PriceType {
  list {
    ...Money
  }
  actual {
    ...Money
  }
}
fragment Product on Product {
  id
  code
  productType
  isConfigurable
  name
  vendor {
    ...Vendor
  }
  price {
    ...ProductPrice
  }
}
fragment Vendor on CommonVendor {
  id
  name
}`) as unknown as TypedDocumentString<ProductConfigurationQuery, ProductConfigurationQueryVariables>;
export const ProductDocument = new TypedDocumentString(`
    query Product($id: String!, $storeId: String!, $userId: String, $cultureName: String, $currencyCode: String) {
  product(
    id: $id
    storeId: $storeId
    userId: $userId
    cultureName: $cultureName
    currencyCode: $currencyCode
  ) {
    ...Product
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment ProductPrice on PriceType {
  list {
    ...Money
  }
  actual {
    ...Money
  }
}
fragment Product on Product {
  id
  code
  productType
  isConfigurable
  name
  vendor {
    ...Vendor
  }
  price {
    ...ProductPrice
  }
}
fragment Vendor on CommonVendor {
  id
  name
}`) as unknown as TypedDocumentString<ProductQuery, ProductQueryVariables>;
export const ProductsDocument = new TypedDocumentString(`
    query Products($storeId: String!, $userId: String, $cultureName: String, $currencyCode: String, $query: String, $filter: String, $sort: String, $first: Int, $after: String) {
  products(
    storeId: $storeId
    userId: $userId
    cultureName: $cultureName
    currencyCode: $currencyCode
    query: $query
    filter: $filter
    sort: $sort
    first: $first
    after: $after
  ) {
    items {
      ...Product
    }
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment ProductPrice on PriceType {
  list {
    ...Money
  }
  actual {
    ...Money
  }
}
fragment Product on Product {
  id
  code
  productType
  isConfigurable
  name
  vendor {
    ...Vendor
  }
  price {
    ...ProductPrice
  }
}
fragment Vendor on CommonVendor {
  id
  name
}`) as unknown as TypedDocumentString<ProductsQuery, ProductsQueryVariables>;
export const CancelQuoteRequestDocument = new TypedDocumentString(`
    mutation CancelQuoteRequest($command: CancelQuoteCommandType!) {
  cancelQuoteRequest(command: $command) {
    ...Quote
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment QuoteItem on QuoteItemType {
  id
  name
  sku
  productId
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  proposalPrices {
    quantity
    price {
      ...Money
    }
  }
}
fragment QuoteTotals on QuoteTotalsType {
  originalSubTotalExlTax {
    ...Money
  }
  subTotalExlTax {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  discountTotal {
    ...Money
  }
  taxTotal {
    ...Money
  }
  grandTotalExlTax {
    ...Money
  }
  grandTotalInclTax {
    ...Money
  }
}
fragment Quote on QuoteType {
  id
  number
  status
  storeId
  customerId
  comment
  isAnonymous
  isCancelled
  totals {
    ...QuoteTotals
  }
  items {
    ...QuoteItem
  }
}`) as unknown as TypedDocumentString<CancelQuoteRequestMutation, CancelQuoteRequestMutationVariables>;
export const ChangeQuoteCommentDocument = new TypedDocumentString(`
    mutation ChangeQuoteComment($command: ChangeQuoteCommentCommandType!) {
  changeQuoteComment(command: $command) {
    ...Quote
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment QuoteItem on QuoteItemType {
  id
  name
  sku
  productId
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  proposalPrices {
    quantity
    price {
      ...Money
    }
  }
}
fragment QuoteTotals on QuoteTotalsType {
  originalSubTotalExlTax {
    ...Money
  }
  subTotalExlTax {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  discountTotal {
    ...Money
  }
  taxTotal {
    ...Money
  }
  grandTotalExlTax {
    ...Money
  }
  grandTotalInclTax {
    ...Money
  }
}
fragment Quote on QuoteType {
  id
  number
  status
  storeId
  customerId
  comment
  isAnonymous
  isCancelled
  totals {
    ...QuoteTotals
  }
  items {
    ...QuoteItem
  }
}`) as unknown as TypedDocumentString<ChangeQuoteCommentMutation, ChangeQuoteCommentMutationVariables>;
export const ChangeQuoteItemQuantityDocument = new TypedDocumentString(`
    mutation ChangeQuoteItemQuantity($command: ChangeQuoteItemQuantityCommandType!) {
  changeQuoteItemQuantity(command: $command) {
    ...Quote
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment QuoteItem on QuoteItemType {
  id
  name
  sku
  productId
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  proposalPrices {
    quantity
    price {
      ...Money
    }
  }
}
fragment QuoteTotals on QuoteTotalsType {
  originalSubTotalExlTax {
    ...Money
  }
  subTotalExlTax {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  discountTotal {
    ...Money
  }
  taxTotal {
    ...Money
  }
  grandTotalExlTax {
    ...Money
  }
  grandTotalInclTax {
    ...Money
  }
}
fragment Quote on QuoteType {
  id
  number
  status
  storeId
  customerId
  comment
  isAnonymous
  isCancelled
  totals {
    ...QuoteTotals
  }
  items {
    ...QuoteItem
  }
}`) as unknown as TypedDocumentString<ChangeQuoteItemQuantityMutation, ChangeQuoteItemQuantityMutationVariables>;
export const CreateQuoteFromCartDocument = new TypedDocumentString(`
    mutation CreateQuoteFromCart($command: CreateQuoteFromCartCommandType!) {
  createQuoteFromCart(command: $command) {
    ...Quote
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment QuoteItem on QuoteItemType {
  id
  name
  sku
  productId
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  proposalPrices {
    quantity
    price {
      ...Money
    }
  }
}
fragment QuoteTotals on QuoteTotalsType {
  originalSubTotalExlTax {
    ...Money
  }
  subTotalExlTax {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  discountTotal {
    ...Money
  }
  taxTotal {
    ...Money
  }
  grandTotalExlTax {
    ...Money
  }
  grandTotalInclTax {
    ...Money
  }
}
fragment Quote on QuoteType {
  id
  number
  status
  storeId
  customerId
  comment
  isAnonymous
  isCancelled
  totals {
    ...QuoteTotals
  }
  items {
    ...QuoteItem
  }
}`) as unknown as TypedDocumentString<CreateQuoteFromCartMutation, CreateQuoteFromCartMutationVariables>;
export const CreateQuoteDocument = new TypedDocumentString(`
    mutation CreateQuote($command: CreateQuoteCommandType!) {
  createQuote(command: $command) {
    ...Quote
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment QuoteItem on QuoteItemType {
  id
  name
  sku
  productId
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  proposalPrices {
    quantity
    price {
      ...Money
    }
  }
}
fragment QuoteTotals on QuoteTotalsType {
  originalSubTotalExlTax {
    ...Money
  }
  subTotalExlTax {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  discountTotal {
    ...Money
  }
  taxTotal {
    ...Money
  }
  grandTotalExlTax {
    ...Money
  }
  grandTotalInclTax {
    ...Money
  }
}
fragment Quote on QuoteType {
  id
  number
  status
  storeId
  customerId
  comment
  isAnonymous
  isCancelled
  totals {
    ...QuoteTotals
  }
  items {
    ...QuoteItem
  }
}`) as unknown as TypedDocumentString<CreateQuoteMutation, CreateQuoteMutationVariables>;
export const GetQuoteDocument = new TypedDocumentString(`
    query GetQuote($id: String!, $storeId: String, $userId: String, $cultureName: String, $currencyCode: String) {
  quote(
    id: $id
    storeId: $storeId
    userId: $userId
    cultureName: $cultureName
    currencyCode: $currencyCode
  ) {
    ...Quote
    addresses {
      ...QuoteAddress
    }
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment QuoteAddress on QuoteAddressType {
  addressType
  city
  countryCode
  countryName
  line1
  postalCode
  regionId
  regionName
}
fragment QuoteItem on QuoteItemType {
  id
  name
  sku
  productId
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  proposalPrices {
    quantity
    price {
      ...Money
    }
  }
}
fragment QuoteTotals on QuoteTotalsType {
  originalSubTotalExlTax {
    ...Money
  }
  subTotalExlTax {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  discountTotal {
    ...Money
  }
  taxTotal {
    ...Money
  }
  grandTotalExlTax {
    ...Money
  }
  grandTotalInclTax {
    ...Money
  }
}
fragment Quote on QuoteType {
  id
  number
  status
  storeId
  customerId
  comment
  isAnonymous
  isCancelled
  totals {
    ...QuoteTotals
  }
  items {
    ...QuoteItem
  }
}`) as unknown as TypedDocumentString<GetQuoteQuery, GetQuoteQueryVariables>;
export const RemoveQuoteItemDocument = new TypedDocumentString(`
    mutation RemoveQuoteItem($command: RemoveQuoteItemCommandType!) {
  removeQuoteItem(command: $command) {
    ...Quote
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment QuoteItem on QuoteItemType {
  id
  name
  sku
  productId
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  proposalPrices {
    quantity
    price {
      ...Money
    }
  }
}
fragment QuoteTotals on QuoteTotalsType {
  originalSubTotalExlTax {
    ...Money
  }
  subTotalExlTax {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  discountTotal {
    ...Money
  }
  taxTotal {
    ...Money
  }
  grandTotalExlTax {
    ...Money
  }
  grandTotalInclTax {
    ...Money
  }
}
fragment Quote on QuoteType {
  id
  number
  status
  storeId
  customerId
  comment
  isAnonymous
  isCancelled
  totals {
    ...QuoteTotals
  }
  items {
    ...QuoteItem
  }
}`) as unknown as TypedDocumentString<RemoveQuoteItemMutation, RemoveQuoteItemMutationVariables>;
export const SubmitQuoteRequestDocument = new TypedDocumentString(`
    mutation SubmitQuoteRequest($command: SubmitQuoteCommandType!) {
  submitQuoteRequest(command: $command) {
    ...Quote
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment QuoteItem on QuoteItemType {
  id
  name
  sku
  productId
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  proposalPrices {
    quantity
    price {
      ...Money
    }
  }
}
fragment QuoteTotals on QuoteTotalsType {
  originalSubTotalExlTax {
    ...Money
  }
  subTotalExlTax {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  discountTotal {
    ...Money
  }
  taxTotal {
    ...Money
  }
  grandTotalExlTax {
    ...Money
  }
  grandTotalInclTax {
    ...Money
  }
}
fragment Quote on QuoteType {
  id
  number
  status
  storeId
  customerId
  comment
  isAnonymous
  isCancelled
  totals {
    ...QuoteTotals
  }
  items {
    ...QuoteItem
  }
}`) as unknown as TypedDocumentString<SubmitQuoteRequestMutation, SubmitQuoteRequestMutationVariables>;
export const UpdateQuoteAddressesDocument = new TypedDocumentString(`
    mutation UpdateQuoteAddresses($command: UpdateQuoteAddressesCommandType!) {
  updateQuoteAddresses(command: $command) {
    ...Quote
    addresses {
      ...QuoteAddress
    }
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment QuoteAddress on QuoteAddressType {
  addressType
  city
  countryCode
  countryName
  line1
  postalCode
  regionId
  regionName
}
fragment QuoteItem on QuoteItemType {
  id
  name
  sku
  productId
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  proposalPrices {
    quantity
    price {
      ...Money
    }
  }
}
fragment QuoteTotals on QuoteTotalsType {
  originalSubTotalExlTax {
    ...Money
  }
  subTotalExlTax {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  discountTotal {
    ...Money
  }
  taxTotal {
    ...Money
  }
  grandTotalExlTax {
    ...Money
  }
  grandTotalInclTax {
    ...Money
  }
}
fragment Quote on QuoteType {
  id
  number
  status
  storeId
  customerId
  comment
  isAnonymous
  isCancelled
  totals {
    ...QuoteTotals
  }
  items {
    ...QuoteItem
  }
}`) as unknown as TypedDocumentString<UpdateQuoteAddressesMutation, UpdateQuoteAddressesMutationVariables>;
export const GetSavedForLaterDocument = new TypedDocumentString(`
    query GetSavedForLater($storeId: String!, $userId: String!, $currencyCode: String, $cultureName: String) {
  getSavedForLater(
    storeId: $storeId
    userId: $userId
    currencyCode: $currencyCode
    cultureName: $cultureName
  ) {
    ...Cart
  }
}
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
fragment CartConfigurationItem on CartConfigurationItemType {
  id
  sectionId
  type
  productId
  name
  sku
  imageUrl
  quantity
  customText
  selectedForCheckout
}
fragment Cart on CartType {
  id
  storeId
  isAnonymous
  hasPhysicalProducts
  customerId
  itemsCount
  itemsQuantity
  total {
    ...Money
  }
  subTotal {
    ...Money
  }
  subTotalDiscount {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  items {
    ...LineItem
  }
  payments {
    ...Payment
  }
  shipments {
    ...Shipment
  }
  coupons {
    ...Coupon
  }
  gifts {
    ...GiftItem
  }
  addresses {
    ...CartAddress
  }
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
}
fragment Coupon on CouponType {
  code
  isAppliedSuccessfully
}
fragment Currency on CurrencyType {
  code
}
fragment GiftItem on GiftItemType {
  id
  quantity
  productId
  name
  lineItemId
}
fragment LineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  placedPrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
  selectedForCheckout
  isValid
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
  configurationItems {
    ...CartConfigurationItem
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment Payment on PaymentType {
  id
  outerId
  paymentGatewayCode
  currency {
    ...Currency
  }
  total {
    ...Money
  }
  billingAddress {
    ...CartAddress
  }
}
fragment Shipment on ShipmentType {
  id
  shipmentMethodCode
  shipmentMethodOption
  fulfillmentCenterId
  price {
    ...Money
  }
  currency {
    ...Currency
  }
  deliveryAddress {
    ...CartAddress
  }
}`) as unknown as TypedDocumentString<GetSavedForLaterQuery, GetSavedForLaterQueryVariables>;
export const MoveFromSavedForLaterDocument = new TypedDocumentString(`
    mutation MoveFromSavedForLater($command: InputSaveForLaterType!) {
  moveFromSavedForLater(command: $command) {
    ...CartWithList
  }
}
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
fragment CartConfigurationItem on CartConfigurationItemType {
  id
  sectionId
  type
  productId
  name
  sku
  imageUrl
  quantity
  customText
  selectedForCheckout
}
fragment CartWithList on CartWithListType {
  cart {
    ...Cart
  }
  list {
    ...Cart
  }
}
fragment Cart on CartType {
  id
  storeId
  isAnonymous
  hasPhysicalProducts
  customerId
  itemsCount
  itemsQuantity
  total {
    ...Money
  }
  subTotal {
    ...Money
  }
  subTotalDiscount {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  items {
    ...LineItem
  }
  payments {
    ...Payment
  }
  shipments {
    ...Shipment
  }
  coupons {
    ...Coupon
  }
  gifts {
    ...GiftItem
  }
  addresses {
    ...CartAddress
  }
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
}
fragment Coupon on CouponType {
  code
  isAppliedSuccessfully
}
fragment Currency on CurrencyType {
  code
}
fragment GiftItem on GiftItemType {
  id
  quantity
  productId
  name
  lineItemId
}
fragment LineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  placedPrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
  selectedForCheckout
  isValid
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
  configurationItems {
    ...CartConfigurationItem
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment Payment on PaymentType {
  id
  outerId
  paymentGatewayCode
  currency {
    ...Currency
  }
  total {
    ...Money
  }
  billingAddress {
    ...CartAddress
  }
}
fragment Shipment on ShipmentType {
  id
  shipmentMethodCode
  shipmentMethodOption
  fulfillmentCenterId
  price {
    ...Money
  }
  currency {
    ...Currency
  }
  deliveryAddress {
    ...CartAddress
  }
}`) as unknown as TypedDocumentString<MoveFromSavedForLaterMutation, MoveFromSavedForLaterMutationVariables>;
export const MoveToSavedForLaterDocument = new TypedDocumentString(`
    mutation MoveToSavedForLater($command: InputSaveForLaterType!) {
  moveToSavedForLater(command: $command) {
    ...CartWithList
  }
}
    fragment CartAddress on CartAddressType {
  id
  key
  city
  countryCode
  countryName
  email
  firstName
  middleName
  lastName
  line1
  line2
  name
  organization
  phone
  postalCode
  regionId
  regionName
  zip
  outerId
  description
  addressType
}
fragment CartConfigurationItem on CartConfigurationItemType {
  id
  sectionId
  type
  productId
  name
  sku
  imageUrl
  quantity
  customText
  selectedForCheckout
}
fragment CartWithList on CartWithListType {
  cart {
    ...Cart
  }
  list {
    ...Cart
  }
}
fragment Cart on CartType {
  id
  storeId
  isAnonymous
  hasPhysicalProducts
  customerId
  itemsCount
  itemsQuantity
  total {
    ...Money
  }
  subTotal {
    ...Money
  }
  subTotalDiscount {
    ...Money
  }
  shippingTotal {
    ...Money
  }
  items {
    ...LineItem
  }
  payments {
    ...Payment
  }
  shipments {
    ...Shipment
  }
  coupons {
    ...Coupon
  }
  gifts {
    ...GiftItem
  }
  addresses {
    ...CartAddress
  }
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
}
fragment Coupon on CouponType {
  code
  isAppliedSuccessfully
}
fragment Currency on CurrencyType {
  code
}
fragment GiftItem on GiftItemType {
  id
  quantity
  productId
  name
  lineItemId
}
fragment LineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
  listPrice {
    ...Money
  }
  salePrice {
    ...Money
  }
  placedPrice {
    ...Money
  }
  extendedPrice {
    ...Money
  }
  discountAmount {
    ...Money
  }
  selectedForCheckout
  isValid
  validationErrors {
    errorCode
    errorMessage
    errorParameters {
      key
      value
    }
    objectType
    objectId
  }
  configurationItems {
    ...CartConfigurationItem
  }
}
fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment Payment on PaymentType {
  id
  outerId
  paymentGatewayCode
  currency {
    ...Currency
  }
  total {
    ...Money
  }
  billingAddress {
    ...CartAddress
  }
}
fragment Shipment on ShipmentType {
  id
  shipmentMethodCode
  shipmentMethodOption
  fulfillmentCenterId
  price {
    ...Money
  }
  currency {
    ...Currency
  }
  deliveryAddress {
    ...CartAddress
  }
}`) as unknown as TypedDocumentString<MoveToSavedForLaterMutation, MoveToSavedForLaterMutationVariables>;
export const SlugInfoDocument = new TypedDocumentString(`
    query SlugInfo($storeId: String, $slug: String, $permalink: String, $userId: String, $cultureName: String) {
  slugInfo(
    storeId: $storeId
    slug: $slug
    permalink: $permalink
    userId: $userId
    cultureName: $cultureName
  ) {
    ...SlugInfo
  }
}
    fragment SeoInfo on SeoInfo {
  id
  name
  semanticUrl
  outline
  pageTitle
  metaDescription
  imageAltDescription
  metaKeywords
  storeId
  objectId
  objectType
  isActive
  languageCode
}
fragment SlugInfo on SlugInfoResponseType {
  entityInfo {
    ...SeoInfo
  }
  redirectUrl
}`) as unknown as TypedDocumentString<SlugInfoQuery, SlugInfoQueryVariables>;
export const AddBulkItemToShoppingListDocument = new TypedDocumentString(`
    mutation AddBulkItemToShoppingList($command: InputAddWishlistBulkItemType!) {
  addWishlistBulkItem(command: $command) {
    wishlists {
      ...ShoppingList
    }
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment ShoppingList on WishlistType {
  id
  name
  storeId
  customerId
  customerName
  items {
    ...WishlistLineItem
  }
  itemsCount
  description
  subTotal {
    ...Money
  }
  sharingSetting {
    id
    scope
  }
}
fragment WishlistLineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
}`) as unknown as TypedDocumentString<AddBulkItemToShoppingListMutation, AddBulkItemToShoppingListMutationVariables>;
export const AddItemsToShoppingListDocument = new TypedDocumentString(`
    mutation AddItemsToShoppingList($command: InputAddWishlistItemsType!) {
  addWishlistItems(command: $command) {
    ...ShoppingList
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment ShoppingList on WishlistType {
  id
  name
  storeId
  customerId
  customerName
  items {
    ...WishlistLineItem
  }
  itemsCount
  description
  subTotal {
    ...Money
  }
  sharingSetting {
    id
    scope
  }
}
fragment WishlistLineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
}`) as unknown as TypedDocumentString<AddItemsToShoppingListMutation, AddItemsToShoppingListMutationVariables>;
export const ChangeShoppingListDocument = new TypedDocumentString(`
    mutation ChangeShoppingList($command: InputChangeWishlistType!) {
  changeWishlist(command: $command) {
    ...ShoppingList
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment ShoppingList on WishlistType {
  id
  name
  storeId
  customerId
  customerName
  items {
    ...WishlistLineItem
  }
  itemsCount
  description
  subTotal {
    ...Money
  }
  sharingSetting {
    id
    scope
  }
}
fragment WishlistLineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
}`) as unknown as TypedDocumentString<ChangeShoppingListMutation, ChangeShoppingListMutationVariables>;
export const CreateShoppingListDocument = new TypedDocumentString(`
    mutation CreateShoppingList($command: InputCreateWishlistType!) {
  createWishlist(command: $command) {
    ...ShoppingList
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment ShoppingList on WishlistType {
  id
  name
  storeId
  customerId
  customerName
  items {
    ...WishlistLineItem
  }
  itemsCount
  description
  subTotal {
    ...Money
  }
  sharingSetting {
    id
    scope
  }
}
fragment WishlistLineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
}`) as unknown as TypedDocumentString<CreateShoppingListMutation, CreateShoppingListMutationVariables>;
export const DeleteShoppingListDocument = new TypedDocumentString(`
    mutation DeleteShoppingList($command: InputRemoveWishlistType!) {
  removeWishlist(command: $command)
}
    `) as unknown as TypedDocumentString<DeleteShoppingListMutation, DeleteShoppingListMutationVariables>;
export const GetShoppingListDocument = new TypedDocumentString(`
    query GetShoppingList($listId: String!, $cultureName: String) {
  wishlist(listId: $listId, cultureName: $cultureName) {
    ...ShoppingList
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment ShoppingList on WishlistType {
  id
  name
  storeId
  customerId
  customerName
  items {
    ...WishlistLineItem
  }
  itemsCount
  description
  subTotal {
    ...Money
  }
  sharingSetting {
    id
    scope
  }
}
fragment WishlistLineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
}`) as unknown as TypedDocumentString<GetShoppingListQuery, GetShoppingListQueryVariables>;
export const GetShoppingListsDocument = new TypedDocumentString(`
    query GetShoppingLists($storeId: String, $userId: String, $currencyCode: String, $cultureName: String) {
  wishlists(
    storeId: $storeId
    userId: $userId
    currencyCode: $currencyCode
    cultureName: $cultureName
  ) {
    items {
      ...ShoppingList
    }
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment ShoppingList on WishlistType {
  id
  name
  storeId
  customerId
  customerName
  items {
    ...WishlistLineItem
  }
  itemsCount
  description
  subTotal {
    ...Money
  }
  sharingSetting {
    id
    scope
  }
}
fragment WishlistLineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
}`) as unknown as TypedDocumentString<GetShoppingListsQuery, GetShoppingListsQueryVariables>;
export const RemoveItemsFromShoppingListDocument = new TypedDocumentString(`
    mutation RemoveItemsFromShoppingList($command: InputRemoveWishlistItemsType!) {
  removeWishlistItems(command: $command) {
    ...ShoppingList
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment ShoppingList on WishlistType {
  id
  name
  storeId
  customerId
  customerName
  items {
    ...WishlistLineItem
  }
  itemsCount
  description
  subTotal {
    ...Money
  }
  sharingSetting {
    id
    scope
  }
}
fragment WishlistLineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
}`) as unknown as TypedDocumentString<
  RemoveItemsFromShoppingListMutation,
  RemoveItemsFromShoppingListMutationVariables
>;
export const UpdateShoppingListItemsDocument = new TypedDocumentString(`
    mutation UpdateShoppingListItems($command: InputUpdateWishlistItemsType!) {
  updateWishListItems(command: $command) {
    ...ShoppingList
  }
}
    fragment Money on MoneyType {
  amount
  formattedAmount
}
fragment ShoppingList on WishlistType {
  id
  name
  storeId
  customerId
  customerName
  items {
    ...WishlistLineItem
  }
  itemsCount
  description
  subTotal {
    ...Money
  }
  sharingSetting {
    id
    scope
  }
}
fragment WishlistLineItem on LineItemType {
  id
  sku
  productId
  name
  quantity
}`) as unknown as TypedDocumentString<UpdateShoppingListItemsMutation, UpdateShoppingListItemsMutationVariables>;
export const DeleteUsersDocument = new TypedDocumentString(`
    mutation DeleteUsers($command: InputDeleteUserType!) {
  deleteUsers(command: $command) {
    ...IdentityResult
  }
}
    fragment IdentityResult on IdentityResultType {
  succeeded
  errors {
    code
    description
  }
}`) as unknown as TypedDocumentString<DeleteUsersMutation, DeleteUsersMutationVariables>;
export const GetMeDocument = new TypedDocumentString(`
    query GetMe {
  me {
    ...User
  }
}
    fragment Role on RoleType {
  id
  name
  normalizedName
}
fragment User on UserType {
  id
  userName
  email
  emailConfirmed
  isAdministrator
  memberId
  storeId
  roles {
    ...Role
  }
}`) as unknown as TypedDocumentString<GetMeQuery, GetMeQueryVariables>;
export const GetUserDocument = new TypedDocumentString(`
    query GetUser($userName: String, $email: String, $id: String) {
  user(userName: $userName, email: $email, id: $id) {
    ...User
  }
}
    fragment Role on RoleType {
  id
  name
  normalizedName
}
fragment User on UserType {
  id
  userName
  email
  emailConfirmed
  isAdministrator
  memberId
  storeId
  roles {
    ...Role
  }
}`) as unknown as TypedDocumentString<GetUserQuery, GetUserQueryVariables>;
export const InviteUserDocument = new TypedDocumentString(`
    mutation InviteUser($command: InputInviteUserType!) {
  inviteUser(command: $command) {
    ...CustomIdentityResult
  }
}
    fragment CustomIdentityResult on CustomIdentityResultType {
  succeeded
  errors {
    code
    parameter
    description
  }
}`) as unknown as TypedDocumentString<InviteUserMutation, InviteUserMutationVariables>;
export const RegisterByInvitationDocument = new TypedDocumentString(`
    mutation RegisterByInvitation($command: InputRegisterByInvitationType!) {
  registerByInvitation(command: $command) {
    ...CustomIdentityResult
  }
}
    fragment CustomIdentityResult on CustomIdentityResultType {
  succeeded
  errors {
    code
    parameter
    description
  }
}`) as unknown as TypedDocumentString<RegisterByInvitationMutation, RegisterByInvitationMutationVariables>;
export const ResetPasswordByTokenDocument = new TypedDocumentString(`
    mutation ResetPasswordByToken($command: InputResetPasswordByTokenType!) {
  resetPasswordByToken(command: $command) {
    ...CustomIdentityResult
  }
}
    fragment CustomIdentityResult on CustomIdentityResultType {
  succeeded
  errors {
    code
    parameter
    description
  }
}`) as unknown as TypedDocumentString<ResetPasswordByTokenMutation, ResetPasswordByTokenMutationVariables>;
export const SendPasswordResetEmailDocument = new TypedDocumentString(`
    mutation SendPasswordResetEmail($command: SendPasswordResetEmailCommandType!) {
  sendPasswordResetEmail(command: $command)
}
    `) as unknown as TypedDocumentString<SendPasswordResetEmailMutation, SendPasswordResetEmailMutationVariables>;
