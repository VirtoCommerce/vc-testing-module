import type { WithRequired } from "@core/required-fields";
import type {
  VirtoCommerceCoreModuleCoreCurrencyCurrency as CurrencyData,
  VirtoCommerceCoreModuleCorePackagePackageType as PackageTypeData,
  VirtoCommerceSeoCoreModelsSeoInfo as SeoInfo,
} from "../generated/rest-api";

export type { CurrencyData, PackageTypeData, SeoInfo };

export const CURRENCY_FIELDS = ["code", "name"] as const;
export const PACKAGE_TYPE_FIELDS = ["id", "name"] as const;

export type Currency = WithRequired<CurrencyData, (typeof CURRENCY_FIELDS)[number]>;
export type PackageType = WithRequired<PackageTypeData, (typeof PACKAGE_TYPE_FIELDS)[number]>;
