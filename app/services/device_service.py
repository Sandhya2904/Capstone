from app.events import create_offline_alert


class DeviceAlreadyExistsError(Exception):
    pass


class DeviceNotFoundError(Exception):
    pass


class DeviceService:
    def __init__(self, repository) -> None:
        self.repository = repository

    def register(self, device: dict) -> dict:
        if self.repository.get_device(device["device_id"]):
            raise DeviceAlreadyExistsError(device["device_id"])
        return self.repository.add_device(device)

    def list(self) -> list[dict]:
        return self.repository.list_devices()

    def get(self, device_id: str) -> dict:
        device = self.repository.get_device(device_id)
        if device is None:
            raise DeviceNotFoundError(device_id)
        return device

    def update_status(self, device_id: str, status: str) -> dict:
        previous = self.repository.get_device(device_id)
        if previous is None:
            raise DeviceNotFoundError(device_id)

        if previous["status"] == "online" and status == "offline":
            updated = self.repository.update_status(device_id, status)
            create_offline_alert(self.repository, device_id)
            return updated

        return self.repository.update_status(device_id, status)
