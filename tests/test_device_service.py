import pytest

from app.repositories.device_repository import InMemoryDeviceRepository
from app.services.device_service import (
    DeviceAlreadyExistsError,
    DeviceNotFoundError,
    DeviceService,
)


@pytest.fixture
def service():
    return DeviceService(InMemoryDeviceRepository())


def device(status="online"):
    return {
        "device_id": "RTR-101",
        "name": "Branch Router",
        "device_type": "router",
        "ip_address": "192.168.10.1",
        "status": status,
        "location": None,
    }


def test_registration(service):
    assert service.register(device())["device_id"] == "RTR-101"


def test_duplicate_registration(service):
    service.register(device())
    with pytest.raises(DeviceAlreadyExistsError):
        service.register(device())


def test_missing_device(service):
    with pytest.raises(DeviceNotFoundError):
        service.get("MISSING")


def test_initial_offline_registration_creates_no_alert(service):
    service.register(device("offline"))
    assert service.repository.list_alerts() == []


def test_online_to_offline_creates_one_alert(service):
    service.register(device())
    service.update_status("RTR-101", "offline")
    alerts = service.repository.list_alerts()
    assert len(alerts) == 1
    assert alerts[0]["device_id"] == "RTR-101"


def test_repeated_offline_creates_no_second_alert(service):
    service.register(device())
    service.update_status("RTR-101", "offline")
    service.update_status("RTR-101", "offline")
    assert len(service.repository.list_alerts()) == 1
