from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.alert import Alert
from app.models.project import Project

router = APIRouter(prefix="/cron", tags=["cron"])


@router.post("/daily")
def run_daily(db: Session = Depends(get_db)) -> dict[str, str]:
    now = datetime.utcnow()
    projects = db.query(Project).all()
    for project in projects:
        alert = Alert(
            project_id=project.id,
            severity="info",
            title="Cron daily",
            detail=f"Cron daily chạy lúc {now.isoformat()}Z",
        )
        db.add(alert)
    db.commit()
    return {"status": "ok", "message": f"Cron daily chạy {len(projects)} dự án"}


@router.post("/weekly")
def run_weekly(db: Session = Depends(get_db)) -> dict[str, str]:
    now = datetime.utcnow()
    projects = db.query(Project).count()
    return {"status": "ok", "message": f"Cron weekly chạy lúc {now.isoformat()}Z cho {projects} dự án"}
