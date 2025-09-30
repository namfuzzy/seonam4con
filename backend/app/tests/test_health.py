import os
import sys
from pathlib import Path

os.environ.setdefault("APP_SECRET", "test-secret-key-test-secret-key-test")
osp = "postgresql://user:pass@localhost:5432/seo"
os.environ.setdefault("JWT_SECRET", "jwt-secret-key-test-1234567890")
os.environ.setdefault("JWT_REFRESH_SECRET", "jwt-refresh-secret-test-123456789")
os.environ.setdefault("DATABASE_URL", osp)

ROOT_DIR = Path(__file__).resolve().parents[2]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from app.main import app
from fastapi.testclient import TestClient


def test_healthz():
    client = TestClient(app)
    response = client.get("/healthz")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
