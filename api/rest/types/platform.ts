import type { WithRequired } from "@core/required-fields";
import type {
  VirtoCommercePlatformWebModelModularityAppDescriptor as AppDescriptorData,
  VirtoCommercePlatformCoreChangeLogChangeLogSearchCriteria as ChangeLogSearchCriteria,
  VirtoCommercePlatformCoreChangeLogChangeLogSearchResult as ChangeLogSearchResult,
  VirtoCommercePlatformCoreDynamicPropertiesDynamicProperty as DynamicPropertyData,
  VirtoCommercePlatformCoreDynamicPropertiesDynamicPropertySearchCriteria as DynamicPropertySearchCriteria,
  VirtoCommercePlatformCoreDynamicPropertiesDynamicPropertySearchResult as DynamicPropertySearchResult,
  VirtoCommercePlatformWebModelLastModifiedResponse as LastModifiedResponse,
  VirtoCommercePlatformWebModularityModuleDescriptor as ModuleDescriptorData,
  VirtoCommercePlatformCorePushNotificationsPushNotificationSearchCriteria as PushNotificationSearchCriteria,
  VirtoCommercePlatformCorePushNotificationsPushNotificationSearchResult as PushNotificationSearchResult,
  VirtoCommercePlatformWebModelDiagnosticsSystemInfo as SystemInfo,
} from "../generated/rest-api";

export type {
  AppDescriptorData,
  ChangeLogSearchCriteria,
  ChangeLogSearchResult,
  DynamicPropertyData,
  DynamicPropertySearchCriteria,
  DynamicPropertySearchResult,
  LastModifiedResponse,
  ModuleDescriptorData,
  PushNotificationSearchCriteria,
  PushNotificationSearchResult,
  SystemInfo,
};

export const APP_DESCRIPTOR_FIELDS = ["id", "title"] as const;
export const DYNAMIC_PROPERTY_FIELDS = ["id", "name", "objectType", "valueType"] as const;

export type AppDescriptor = WithRequired<AppDescriptorData, (typeof APP_DESCRIPTOR_FIELDS)[number]>;
export type DynamicProperty = WithRequired<DynamicPropertyData, (typeof DYNAMIC_PROPERTY_FIELDS)[number]>;
