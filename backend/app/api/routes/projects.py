from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.models.project import Project
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectRead
from app.services.auth import get_current_user

router = APIRouter(prefix="/projects", tags=["projects"])


@router.get("/", response_model=List[ProjectRead])
async def list_projects(
    session: AsyncSession = Depends(get_session), current_user: User = Depends(get_current_user)
) -> List[ProjectRead]:
    result = await session.execute(select(Project).where(Project.owner_id == current_user.id))
    projects = result.scalars().unique().all()
    return [
        ProjectRead(
            id=project.id,
            name=project.name,
            goals=project.goals,
            created_at=project.created_at,
        )
        for project in projects
    ]


@router.post("/", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
async def create_project(
    payload: ProjectCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> ProjectRead:
    if payload.owner_id != current_user.id and current_user.role not in {"admin"}:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Không có quyền tạo cho người khác")
    project = Project(owner_id=payload.owner_id, name=payload.name, goals=payload.goals)
    session.add(project)
    await session.commit()
    await session.refresh(project)
    return ProjectRead(
        id=project.id,
        name=project.name,
        goals=project.goals,
        created_at=project.created_at,
    )
