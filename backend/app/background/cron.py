from datetime import datetime

from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.alert import Alert


def run_daily() -> None:
    db: Session = SessionLocal()
    try:
        alert = Alert(project_id=1, severity="info", title="Cron chạy", detail=f"Cập nhật lúc {datetime.utcnow().isoformat()}Z")
        db.add(alert)
        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    run_daily()
