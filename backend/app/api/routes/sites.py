from typing import List

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.project import Project
from app.models.site import Site
from app.models.user import User
from app.schemas.site import SiteCreate, SiteRead
from app.services.auth import get_current_user

router = APIRouter(prefix="/sites", tags=["sites"])


@router.get("/", response_model=List[SiteRead])
async def list_sites(
    project_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> List[SiteRead]:
    project = await session.get(Project, project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy dự án")
    result = await session.execute(select(Site).where(Site.project_id == project_id))
    sites = result.scalars().unique().all()
    return [
        SiteRead(
            id=site.id,
            domain=site.domain,
            wp_base_url=site.wp_base_url,
            project_id=site.project_id,  # type: ignore[arg-type]
            created_at=site.created_at,
            integrations=[],
        )
        for site in sites
    ]


@router.post("/", response_model=SiteRead, status_code=status.HTTP_201_CREATED)
async def create_site(
    payload: SiteCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> SiteRead:
    project = await session.get(Project, payload.project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy dự án")
    site = Site(project_id=payload.project_id, domain=payload.domain, wp_base_url=payload.wp_base_url)
    session.add(site)
    await session.commit()
    await session.refresh(site)
    return SiteRead(
        id=site.id,
        domain=site.domain,
        wp_base_url=site.wp_base_url,
        project_id=site.project_id,  # type: ignore[arg-type]
        created_at=site.created_at,
        integrations=[],
    )
