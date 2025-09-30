from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class SiteBase(BaseModel):
    domain: str
    wp_base_url: Optional[str] = None


class SiteCreate(SiteBase):
    project_id: int


class SiteRead(SiteBase):
    id: int
    project_id: int
    created_at: datetime

    class Config:
        orm_mode = True
