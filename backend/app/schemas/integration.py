from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.models.integration import IntegrationType


class CredentialRead(BaseModel):
    id: int
    key_name: str
    value_masked: str

    class Config:
        orm_mode = True


class CredentialCreate(BaseModel):
    key_name: str
    value: str


class IntegrationBase(BaseModel):
    type: IntegrationType
    enabled: bool = False


class IntegrationCreate(IntegrationBase):
    project_id: int


class IntegrationRead(IntegrationBase):
    id: int
    project_id: int
    created_at: datetime
    credentials: List[CredentialRead] = []

    class Config:
        orm_mode = True
