from pydantic import BaseModel


class PropertyType(BaseModel):
    PRODUCT = "PRODUCT"
    VARIATION = "VARIATION"
    CATEGORY = "CATEGORY"
    CATALOG = "CATALOG"
