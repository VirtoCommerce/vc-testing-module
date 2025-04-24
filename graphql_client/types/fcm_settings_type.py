from pydantic import BaseModel


class FcmSettingsType(BaseModel):
    def __init__(self):

        self.apiKey: str
        self.authDomain: str
        self.projectId: str
        self.storageBucket: str
        self.messagingSenderId: str
        self.appId: str
        self.vapidKey: str
