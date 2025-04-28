from pydantic import BaseModel


class PropertyValueTypes(BaseModel):
    SHORT_TEXT = "SHORT_TEXT"
    LONG_TEXT = "LONG_TEXT"
    NUMBER = "NUMBER"
    DATE_TIME = "DATE_TIME"
    BOOLEAN = "BOOLEAN"
    INTEGER = "INTEGER"
    GEO_POINT = "GEO_POINT"
    HTML = "HTML"
    MEASURE = "MEASURE"
