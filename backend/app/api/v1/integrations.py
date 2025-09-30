from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import deps
from app.core.config import get_settings
from app.db.session import get_db
from app.models.integration import Credential, Integration, IntegrationType
from app.models.project import Project
from app.models.user import User
from app.schemas.integration import (
    CredentialCreate,
    CredentialRead,
    IntegrationCreate,
    IntegrationRead,
)
from app.utils.crypto import decrypt, encrypt, mask_value

router = APIRouter(prefix="/integrations", tags=["integrations"])
settings = get_settings()


def _serialize_integration(integration: Integration) -> IntegrationRead:
    return IntegrationRead(
        id=integration.id,
        project_id=integration.project_id,
        type=integration.type,
        enabled=integration.enabled,
        created_at=integration.created_at,
        credentials=[
            CredentialRead(
                id=credential.id,
                key_name=credential.key_name,
                value_masked=mask_value(
                    decrypt(settings.secret_key, credential.value_encrypted)
                ),
            )
            for credential in integration.credentials
        ],
    )


@router.get("", response_model=list[IntegrationRead])
def list_integrations(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
) -> list[IntegrationRead]:
    project = db.query(Project).filter(Project.id == project_id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Không tìm thấy dự án")
    integrations = db.query(Integration).filter(Integration.project_id == project_id).all()
    return [_serialize_integration(integration) for integration in integrations]


@router.post("", response_model=IntegrationRead)
def create_integration(
    payload: IntegrationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
) -> IntegrationRead:
    project = db.query(Project).filter(Project.id == payload.project_id, Project.owner_id == current_user.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Không tìm thấy dự án")
    integration = Integration(project_id=payload.project_id, type=payload.type, enabled=payload.enabled)
    db.add(integration)
    db.commit()
    db.refresh(integration)
    return _serialize_integration(integration)


@router.post("/{integration_id}/credentials", response_model=IntegrationRead)
def upsert_credentials(
    integration_id: int,
    payloads: list[CredentialCreate],
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
) -> IntegrationRead:
    integration = (
        db.query(Integration)
        .join(Project)
        .filter(Integration.id == integration_id, Project.owner_id == current_user.id)
        .first()
    )
    if not integration:
        raise HTTPException(status_code=404, detail="Không tìm thấy tích hợp")
    existing = {cred.key_name: cred for cred in integration.credentials}
    for payload in payloads:
        encrypted = encrypt(settings.secret_key, payload.value)
        if payload.key_name in existing:
            existing[payload.key_name].value_encrypted = encrypted
        else:
            db.add(Credential(integration_id=integration.id, key_name=payload.key_name, value_encrypted=encrypted))
    db.commit()
    db.refresh(integration)
    return _serialize_integration(integration)


@router.post("/{integration_id}/toggle")
def toggle_integration(
    integration_id: int,
    enabled: bool,
    db: Session = Depends(get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict[str, bool]:
    integration = (
        db.query(Integration)
        .join(Project)
        .filter(Integration.id == integration_id, Project.owner_id == current_user.id)
        .first()
    )
    if not integration:
        raise HTTPException(status_code=404, detail="Không tìm thấy tích hợp")
    integration.enabled = enabled
    db.commit()
    return {"enabled": integration.enabled}


@router.post("/{integration_id}/test")
def test_integration(integration_id: int, db: Session = Depends(get_db), current_user: User = Depends(deps.get_current_user)) -> dict[str, str]:
    integration = (
        db.query(Integration)
        .join(Project)
        .filter(Integration.id == integration_id, Project.owner_id == current_user.id)
        .first()
    )
    if not integration:
        raise HTTPException(status_code=404, detail="Không tìm thấy tích hợp")
    return {"status": "ready", "message": "Kết nối sẽ được kiểm tra khi cron chạy"}
