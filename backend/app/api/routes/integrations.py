from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import decrypt_value, encrypt_value
from app.db.session import get_session
from app.models.credential import Credential
from app.models.integration import Integration
from app.models.project import Project
from app.models.site import Site
from app.models.user import User
from app.schemas.credential import CredentialCreate, CredentialRead
from app.schemas.integration import IntegrationCreate, IntegrationRead
from app.services.auth import get_current_user

router = APIRouter(prefix="/integrations", tags=["integrations"])


@router.get("/", response_model=List[IntegrationRead])
async def list_integrations(
    site_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> List[IntegrationRead]:
    site = await session.get(Site, site_id)
    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy site")
    project = await session.get(Project, site.project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy site")
    result = await session.execute(
        select(Integration).options(selectinload(Integration.credentials)).where(Integration.site_id == site_id)
    )
    integrations = result.scalars().unique().all()
    response: List[IntegrationRead] = []
    for integration in integrations:
        response.append(
            IntegrationRead(
                id=integration.id,
                type=integration.type,
                enabled=integration.enabled,
                created_at=integration.created_at,
            )
        )
    return response


@router.post("/", response_model=IntegrationRead, status_code=status.HTTP_201_CREATED)
async def create_integration(
    payload: IntegrationCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> IntegrationRead:
    site = await session.get(Site, payload.site_id)
    if not site:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy site")
    project = await session.get(Project, site.project_id)
    if not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy site")
    integration = Integration(site_id=payload.site_id, type=payload.type, enabled=payload.enabled)
    session.add(integration)
    await session.commit()
    await session.refresh(integration)
    return IntegrationRead(
        id=integration.id,
        type=integration.type,
        enabled=integration.enabled,
        created_at=integration.created_at,
    )


@router.post("/{integration_id}/credentials", response_model=CredentialRead, status_code=status.HTTP_201_CREATED)
async def upsert_credential(
    integration_id: int,
    payload: CredentialCreate,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> CredentialRead:
    integration = await session.get(Integration, integration_id)
    if not integration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tích hợp")
    site = await session.get(Site, integration.site_id)
    project = await session.get(Project, site.project_id) if site else None
    if not site or not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tích hợp")
    result = await session.execute(
        select(Credential).where(
            Credential.integration_id == integration_id, Credential.key_name == payload.key_name
        )
    )
    credential = result.scalar_one_or_none()
    encrypted_value = encrypt_value(payload.value)
    if credential:
        credential.value_encrypted = encrypted_value
    else:
        credential = Credential(
            integration_id=integration_id,
            key_name=payload.key_name,
            value_encrypted=encrypted_value,
        )
        session.add(credential)
    await session.commit()
    await session.refresh(credential)
    return CredentialRead(id=credential.id, key_name=credential.key_name, created_at=credential.created_at)


@router.get("/{integration_id}/credentials/{credential_id}/reveal")
async def reveal_credential(
    integration_id: int,
    credential_id: int,
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    integration = await session.get(Integration, integration_id)
    if not integration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tích hợp")
    site = await session.get(Site, integration.site_id)
    project = await session.get(Project, site.project_id) if site else None
    if not site or not project or project.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy tích hợp")
    credential = await session.get(Credential, credential_id)
    if not credential or credential.integration_id != integration_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Không tìm thấy credential")
    return {"key": credential.key_name, "value": decrypt_value(credential.value_encrypted)}
