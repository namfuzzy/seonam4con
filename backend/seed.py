import asyncio
from datetime import date

from sqlalchemy import select

from app.core.security import get_password_hash
from app.db.session import async_session
from app.models.content import ContentBrief, ContentDraft
from app.models.integration import Integration, IntegrationType
from app.models.page import Page
from app.models.page_metric import PageMetric
from app.models.project import Project
from app.models.site import Site
from app.models.user import User


async def seed() -> None:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.email == "admin@example.com"))
        user = result.scalar_one_or_none()
        if not user:
            user = User(
                email="admin@example.com",
                name="Admin Demo",
                role="owner",
                password_hash=get_password_hash("Admin123!"),
            )
            session.add(user)
            await session.flush()

        project = Project(owner_id=user.id, name="Dự án Demo", goals="Tăng traffic tự nhiên 20%")
        session.add(project)
        await session.flush()

        site = Site(project_id=project.id, domain="demo.example.com", wp_base_url="https://demo.example.com")
        session.add(site)
        await session.flush()

        integration = Integration(site_id=site.id, type=IntegrationType.GSC.value, enabled=False)
        session.add(integration)

        page = Page(site_id=site.id, url="https://demo.example.com/huong-dan-seo", title="Hướng dẫn SEO", status="published")
        session.add(page)
        await session.flush()

        metric = PageMetric(page_id=page.id, date=date.today(), clicks=120, impressions=1500, ctr=0.08, position=5.2)
        session.add(metric)

        brief = ContentBrief(
            site_id=site.id,
            topic="Chiến lược SEO 2025",
            intent="MOFU",
            stage="MOFU",
            outline_json={"sections": ["Tổng quan", "Checklist"]},
            checklist_json={"items": ["E-E-A-T", "Nguồn uy tín"]},
        )
        session.add(brief)

        draft = ContentDraft(
            site_id=site.id,
            title="Chiến lược SEO 2025",
            slug="chien-luoc-seo-2025",
            html="<h1>Chiến lược SEO 2025</h1><p>Nội dung demo.</p>",
            schema_json={"@type": "Article"},
            status="draft",
        )
        session.add(draft)

        await session.commit()


if __name__ == "__main__":
    asyncio.run(seed())
