import pytest

from app.models.integration import IntegrationType

from .test_projects import login


@pytest.mark.asyncio
async def test_integration_credential_flow(client):
    token = await login(client)

    create_site = await client.post(
        "/api/v1/projects/",
        json={"name": "Dự án credential", "goals": "Test", "owner_id": 1},
        headers={"Authorization": f"Bearer {token}"},
    )
    project_id = create_site.json()["id"]

    site_resp = await client.post(
        "/api/v1/sites/",
        json={"domain": "cred.example.com", "project_id": project_id, "wp_base_url": None},
        headers={"Authorization": f"Bearer {token}"},
    )
    site_id = site_resp.json()["id"]

    integration_resp = await client.post(
        "/api/v1/integrations/",
        json={"site_id": site_id, "type": IntegrationType.GSC.value, "enabled": True},
        headers={"Authorization": f"Bearer {token}"},
    )
    integration_id = integration_resp.json()["id"]

    cred_resp = await client.post(
        f"/api/v1/integrations/{integration_id}/credentials",
        json={"key_name": "client_id", "value": "demo"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert cred_resp.status_code == 201
    credential_id = cred_resp.json()["id"]

    reveal = await client.get(
        f"/api/v1/integrations/{integration_id}/credentials/{credential_id}/reveal",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert reveal.status_code == 200
    data = reveal.json()
    assert data["value"] == "demo"
