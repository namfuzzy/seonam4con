from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import deps
from app.db.session import get_db
from app.models.project import Project
from app.models.site import Site
from app.models.user import User
from app.schemas.site import SiteCreate, SiteRead, SiteUpdate

router = APIRouter(prefix="/sites", tags=["sites"])


@router.get("", response_model=list[SiteRead])
def list_sites(
    project_id: int | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
) -> list[SiteRead]:
    query = db.query(Site).join(Project).filter(Project.owner_id == current_user.id)
    if project_id:
        query = query.filter(Site.project_id == project_id)
    return query.all()


@router.post("", response_model=SiteRead)
def create_site(
    payload: SiteCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
) -> SiteRead:
    project = db.query(Project).filter(Project.id == payload.project_id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Không tìm thấy dự án")
    site = Site(**payload.dict())
    db.add(site)
    db.commit()
    db.refresh(site)
    return site


@router.put("/{site_id}", response_model=SiteRead)
def update_site(
    site_id: int,
    payload: SiteUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
) -> SiteRead:
    site = (
        db.query(Site)
        .join(Project)
        .filter(Site.id == site_id, Project.owner_id == current_user.id)
        .first()
    )
    if not site:
        raise HTTPException(status_code=404, detail="Không tìm thấy site")
    for key, value in payload.dict(exclude_unset=True).items():
        setattr(site, key, value)
    db.commit()
    db.refresh(site)
    return site


@router.delete("/{site_id}")
def delete_site(
    site_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict[str, str]:
    site = (
        db.query(Site)
        .join(Project)
        .filter(Site.id == site_id, Project.owner_id == current_user.id)
        .first()
    )
    if not site:
        raise HTTPException(status_code=404, detail="Không tìm thấy site")
    db.delete(site)
    db.commit()
    return {"message": "Đã xóa site"}
