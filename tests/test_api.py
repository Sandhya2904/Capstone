import pytest
from fastapi.testclient import TestClient

from app.dependencies import get_repository
from app.main import app
from app.repositories.device_repository import InMemoryDeviceRepository


@pytest.fixture
def repository():
    return InMemoryDeviceRepository()


@pytest.fixture
def client(repository):
    app.dependency_overrides[get_repository] = lambda: repository
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


def test_health_and_openapi(client):
    assert client.get("/health").status_code == 200
    assert client.get("/health").json() == {"status": "ok"}

    openapi = client.get("/openapi.json")
    assert openapi.status_code == 200
    paths = openapi.json()["paths"]
    assert len([path for path in paths if path in ("/devices", "/devices/{device_id}", "/devices/{device_id}/status", "/alerts", "/health")]) == 5


def test_registration_validation_and_conflict(client):
    payload = {
        "device_id": "RTR-101", "name": "Branch Router", "device_type": "router",
        "ip_address": "192.168.10.1", "status": "online",
    }
    assert client.post("/devices", json=payload).status_code == 201
    assert client.post("/devices", json=payload).status_code == 409

    bad = {**payload, "device_id": "BAD", "ip_address": "999.1.1.1"}
    assert client.post("/devices", json=bad).status_code == 422


def test_exactly_one_offline_alert_after_two_updates(client):
    payload = {
        "device_id": "RTR-101", "name": "Branch Router", "device_type": "router",
        "ip_address": "192.168.10.1", "status": "online",
    }
    assert client.post("/devices", json=payload).status_code == 201
    assert client.patch("/devices/RTR-101/status", json={"status": "offline"}).status_code == 200
    assert len(client.get("/alerts").json()) == 1
    assert client.patch("/devices/RTR-101/status", json={"status": "offline"}).status_code == 200
    assert len(client.get("/alerts").json()) == 1


def test_missing_device(client):
    assert client.get("/devices/MISSING").status_code == 404
    assert client.patch("/devices/MISSING/status", json={"status": "offline"}).status_code == 404
