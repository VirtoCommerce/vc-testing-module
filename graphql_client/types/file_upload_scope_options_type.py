from pydantic import BaseModel


class FileUploadScopeOptionsType(BaseModel):
    def __init__(self):

        self.scope: str
        self.maxFileSize: int
        self.allowedExtensions: list[str]
        self.allowAnonymousUpload: bool
