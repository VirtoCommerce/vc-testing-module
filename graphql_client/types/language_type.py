from pydantic import BaseModel


class LanguageType(BaseModel):
    def __init__(self):

        self.isInvariant: bool
        self.cultureName: str
        self.nativeName: str
        self.threeLetterLanguageName: str
        self.twoLetterLanguageName: str
        self.twoLetterRegionName: str
        self.threeLetterRegionName: str
