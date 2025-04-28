from pydantic import BaseModel


class DynamicPropertyValueTypes(BaseModel):
    UNDEFINED = "UNDEFINED"
    SHORT_TEXT = "SHORT_TEXT"
    LONG_TEXT = "LONG_TEXT"
    INTEGER = "INTEGER"
    DECIMAL = "DECIMAL"
    DATE_TIME = "DATE_TIME"
    BOOLEAN = "BOOLEAN"
    HTML = "HTML"
    IMAGE = "IMAGE"
