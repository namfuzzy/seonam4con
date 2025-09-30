import json
from datetime import date, timedelta

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.db.session import SessionLocal
from app.models.gsc import Page, PageMetric
from app.models.project import Project
from app.models.site import Site
from app.models.user import User, UserRole


def seed() -> None:
    db: Session = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == "admin@demo.local").first()
        if existing:
            print("Seed đã tồn tại")
            return
        admin = User(
            email="admin@demo.local",
            name="Quản trị viên Demo",
            role=UserRole.OWNER,
            password_hash=get_password_hash("Admin123!"),
        )
        db.add(admin)
        db.commit()
        db.refresh(admin)

        project = Project(owner_id=admin.id, name="Dự án Demo", goals="Tăng trưởng Click 20%")
        db.add(project)
        db.commit()
        db.refresh(project)

        site = Site(project_id=project.id, domain="https://demo-site.vn", wp_base_url="https://demo-site.vn/wp-json")
        db.add(site)
        db.commit()
        db.refresh(site)

        page = Page(site_id=site.id, url="https://demo-site.vn/bai-viet-chu-luc", title="Bài viết chủ lực")
        db.add(page)
        db.commit()
        db.refresh(page)

        today = date.today()
        for i in range(28):
            metric = PageMetric(
                page_id=page.id,
                date=today - timedelta(days=i),
                clicks=100 - i,
                impressions=500 - i * 2,
                ctr=0.2,
                position=5 + i * 0.1,
            )
            db.add(metric)
        db.commit()

        print("Seed hoàn tất. Tài khoản demo: admin@demo.local / Admin123!")
    finally:
        db.close()


if __name__ == "__main__":
    seed()
