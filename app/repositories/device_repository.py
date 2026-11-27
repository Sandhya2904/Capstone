from copy import deepcopy


class InMemoryDeviceRepository:
    def __init__(self) -> None:
        self._devices: dict[str, dict] = {}
        self._alerts: list[dict] = []

    def add_device(self, device: dict) -> dict:
        device_id = device["device_id"]
        if device_id in self._devices:
            raise KeyError(device_id)
        stored = deepcopy(device)
        self._devices[device_id] = stored
        return deepcopy(stored)

    def list_devices(self) -> list[dict]:
        return deepcopy(list(self._devices.values()))

    def get_device(self, device_id: str) -> dict | None:
        device = self._devices.get(device_id)
        return deepcopy(device) if device is not None else None

    def update_status(self, device_id: str, status: str) -> dict:
        if device_id not in self._devices:
            raise KeyError(device_id)
        self._devices[device_id]["status"] = status
        return deepcopy(self._devices[device_id])

    def save_alert(self, alert: dict) -> dict:
        stored = deepcopy(alert)
        self._alerts.append(stored)
        return deepcopy(stored)

    def list_alerts(self) -> list[dict]:
        return deepcopy(self._alerts)
