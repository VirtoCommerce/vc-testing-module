import type { WithRequired } from "@core/required-fields";
import type {
  VirtoCommercePlatformCoreSecurityApplicationUser as ApplicationUserData,
  MicrosoftAspNetCoreIdentityIdentityResult as IdentityResult,
  OpenIddictAbstractionsOpenIddictApplicationDescriptor as OAuthAppData,
  VirtoCommercePlatformWebModelSecurityOAuthAppSearchCriteria as OAuthAppSearchCriteria,
  VirtoCommercePlatformWebModelSecurityOAuthAppSearchResult as OAuthAppSearchResult,
  VirtoCommercePlatformCoreSecurityPermission as Permission,
  VirtoCommercePlatformCoreSecurityRole as RoleData,
  VirtoCommercePlatformCoreSecurityRoleSearchCriteria as RoleSearchCriteria,
  VirtoCommercePlatformCoreSecuritySearchRoleSearchResult as RoleSearchResult,
  VirtoCommercePlatformCoreSecuritySecurityResult as SecurityResult,
  VirtoCommercePlatformCoreSecurityUserApiKey as UserApiKeyData,
  VirtoCommercePlatformWebModelSecurityUserDetail as UserDetail,
  VirtoCommercePlatformCoreSecurityUserSearchCriteria as UserSearchCriteria,
  VirtoCommercePlatformCoreSecuritySearchUserSearchResult as UserSearchResult,
} from "../generated/rest-api";

export type {
  MicrosoftAspNetCoreIdentitySignInResult as SignInResultData,
  VirtoCommercePlatformWebModelSecurityLoginRequest as LoginRequestData,
} from "../generated/rest-api";

export type {
  ApplicationUserData,
  IdentityResult,
  OAuthAppData,
  OAuthAppSearchCriteria,
  OAuthAppSearchResult,
  Permission,
  RoleData,
  RoleSearchCriteria,
  RoleSearchResult,
  SecurityResult,
  UserApiKeyData,
  UserDetail,
  UserSearchCriteria,
  UserSearchResult,
};

export const APPLICATION_USER_FIELDS = ["id", "userName", "email"] as const;
export const ROLE_FIELDS = ["id", "name"] as const;
export const USER_API_KEY_FIELDS = ["id", "userId", "isActive"] as const;

export type ApplicationUser = WithRequired<ApplicationUserData, (typeof APPLICATION_USER_FIELDS)[number]>;
export type Role = WithRequired<RoleData, (typeof ROLE_FIELDS)[number]>;
export type UserApiKey = WithRequired<UserApiKeyData, (typeof USER_API_KEY_FIELDS)[number]>;
