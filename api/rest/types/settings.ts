import type { WithRequired } from "@core/required-fields";
import type { VirtoCommercePlatformCoreSettingsObjectSettingEntry as ObjectSettingEntryData } from "../generated/rest-api";

export type SettingEntryData = Omit<ObjectSettingEntryData, "allowedValues" | "value"> & {
  allowedValues?: unknown[] | null;
  value?: unknown;
};

export const SETTING_FIELDS = ["name"] as const;

export type SettingEntry = WithRequired<SettingEntryData, (typeof SETTING_FIELDS)[number]>;
