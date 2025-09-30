from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel

from app.schemas.site import SiteRead


class ProjectBase(BaseModel):
    name: str
    goals: Optional[str] = None


class ProjectCreate(ProjectBase):
    owner_id: int


class ProjectUpdate(ProjectBase):
    pass


class ProjectRead(ProjectBase):
    id: int
    owner_id: int
    created_at: datetime
    sites: List[SiteRead] = []

    class Config:
        orm_mode = True
