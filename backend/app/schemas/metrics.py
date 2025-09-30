from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel


class PageMetricRead(BaseModel):
    date: date
    clicks: float
    impressions: float
    ctr: float
    position: float

    class Config:
        orm_mode = True


class CWVMetricRead(BaseModel):
    date: date
    lcp: Optional[float]
    inp: Optional[float]
    cls: Optional[float]
    lab_json: Optional[dict]
    field_json: Optional[dict]

    class Config:
        orm_mode = True


class PageRead(BaseModel):
    id: int
    url: str
    title: Optional[str]
    metrics: list[PageMetricRead] = []

    class Config:
        orm_mode = True
