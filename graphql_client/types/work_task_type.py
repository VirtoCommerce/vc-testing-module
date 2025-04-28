from pydantic import BaseModel


class WorkTaskType(BaseModel):
    def __init__(self):
        from datetime import datetime

        self.completed: bool | None
        self.createdBy: str | None
        self.createdDate: datetime
        self.description: str | None
        self.dueDate: datetime | None
        self.id: str
        self.isActive: bool
        self.modifiedBy: str | None
        self.modifiedDate: datetime | None
        self.priority: int | None
        self.responsibleName: str | None
        self.storeId: str | None
        self.type: str | None
        self.workflowId: str | None
        self.parameters: str | None
