from datetime import datetime

from pydantic import BaseModel


class CredentialBase(BaseModel):
    key_name: str


class CredentialCreate(CredentialBase):
    value: str


class CredentialRead(CredentialBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
