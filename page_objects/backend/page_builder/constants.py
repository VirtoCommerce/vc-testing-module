from typing import Final


class Route:
    ALL: Final = "page-builder"
    DRAFT: Final = "page-builder-draft"
    PENDING: Final = "page-builder-pending"
    ACTIVE: Final = "page-builder-active"
    ARCHIVED: Final = "page-builder-archived"


class Menu:
    DRAFT: Final = "DraftPagesList"
    PENDING: Final = "PendingPagesList"
    ACTIVE: Final = "ActivePagesList"
    ARCHIVED: Final = "ArchivedPagesList"
    ALL: Final = "AllPagesList"
    ASSETS: Final = "AssetsLibrary"


class ListToolbar:
    ADD: Final = "add"
    REFRESH: Final = "refresh"
    ARCHIVE: Final = "delete"


class DetailsToolbar:
    SAVE: Final = "save"
    ARCHIVE: Final = "delete"
    OPEN_DESIGNER: Final = "openPageDesigner"
    DOWNLOAD_CONTENT: Final = "downloadContent"
    CLONE: Final = "clonePage"
    PUBLISH: Final = "publishPage"
    UNPUBLISH: Final = "unpublishPage"


class Column:
    NAME: Final = "name"
    LANGUAGE: Final = "cultureName"
    PERMALINK: Final = "permalink"
    MODIFIED: Final = "modifiedDate"
    MODIFIED_BY: Final = "modifiedBy"
    STATUS: Final = "status"


class Field:
    NAME: Final = "Name*"
    PERMALINK: Final = "Permalink*"
    LANGUAGE: Final = "Language"
    VISIBILITY: Final = "Visibility"
    USER_GROUPS: Final = "User groups"
    ORGANIZATION: Final = "Organization"
    START_DATE: Final = "Start date"
    END_DATE: Final = "End date"


class Section:
    BASIC: Final = "Basic information"
    ADVANCED: Final = "Advanced options"
    PERSONALIZATION: Final = "Personalization & Access control"
    SCHEDULING: Final = "Scheduling"


class Status:
    DRAFT: Final = "Draft"
    PUBLISHED: Final = "Published"
    ARCHIVED: Final = "Archived"
    SCHEDULED: Final = "Scheduled"


ALL_COLUMNS: Final = [
    Column.NAME,
    Column.LANGUAGE,
    Column.PERMALINK,
    Column.MODIFIED,
    Column.MODIFIED_BY,
    Column.STATUS,
]
