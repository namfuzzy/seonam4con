from datetime import datetime
from typing import List

from pydantic import BaseModel


class IntegrationBase(BaseModel):
    type: str
    enabled: bool = False


class IntegrationCreate(IntegrationBase):
    site_id: int


class IntegrationRead(IntegrationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
