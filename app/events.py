from datetime import datetime, timezone


def create_offline_alert(repository, device_id: str) -> dict:
    alert = {
        "device_id": device_id,
        "message": f"Device {device_id} changed from online to offline",
        "timestamp": datetime.now(timezone.utc),
    }
    return repository.save_alert(alert)
