from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import deps
from app.db.session import get_db
from app.models.gsc import Page, PageMetric
from app.models.site import Site
from app.models.user import User
from app.schemas.metrics import PageRead

router = APIRouter(prefix="/metrics", tags=["metrics"])


@router.get("/pages", response_model=list[PageRead])
def list_page_metrics(
    site_id: int,
    start_date: date | None = None,
    end_date: date | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
) -> list[PageRead]:
    query = (
        db.query(Page)
        .join(Site)
        .filter(Site.id == site_id, Site.project.has(owner_id=current_user.id))
    )
    pages = query.all()
    results: list[PageRead] = []
    for page in pages:
        metrics_query = db.query(PageMetric).filter(PageMetric.page_id == page.id)
        if start_date:
            metrics_query = metrics_query.filter(PageMetric.date >= start_date)
        if end_date:
            metrics_query = metrics_query.filter(PageMetric.date <= end_date)
        metrics = metrics_query.order_by(PageMetric.date.desc()).all()
        results.append(
            PageRead(
                id=page.id,
                url=page.url,
                title=page.title,
                metrics=[metric for metric in metrics],
            )
        )
    return results
