export const Route = {
  all: "page-builder",
  draft: "page-builder-draft",
  pending: "page-builder-pending",
  active: "page-builder-active",
  archived: "page-builder-archived",
} as const;

export type PageBuilderRoute = (typeof Route)[keyof typeof Route];

export const MenuItem = {
  draft: "DraftPagesList",
  pending: "PendingPagesList",
  active: "ActivePagesList",
  archived: "ArchivedPagesList",
  all: "AllPagesList",
  assets: "AssetsLibrary",
} as const;

export const ListToolbar = {
  add: "add",
  refresh: "refresh",
  archive: "delete",
} as const;

export const DetailsToolbar = {
  save: "save",
  archive: "delete",
  openDesigner: "openPageDesigner",
  downloadContent: "downloadContent",
  clone: "clonePage",
  publish: "publishPage",
  unpublish: "unpublishPage",
} as const;

export const Column = {
  name: "name",
  language: "cultureName",
  permalink: "permalink",
  modified: "modifiedDate",
  modifiedBy: "modifiedBy",
  status: "status",
} as const;

export const ALL_COLUMNS = Object.values(Column);

export const Field = {
  name: "Name*",
  permalink: "Permalink*",
  language: "Language",
  visibility: "Visibility",
  userGroups: "User groups",
  organization: "Organization",
  startDate: "Start date",
  endDate: "End date",
} as const;

export const Section = {
  basic: "Basic information",
  personalization: "Personalization & Access control",
  scheduling: "Scheduling",
} as const;

export const Status = {
  draft: "Draft",
  published: "Published",
  archived: "Archived",
  scheduled: "Scheduled",
} as const;
