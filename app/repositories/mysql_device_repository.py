from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.models import Alert, Device
from app.services.device_service import DeviceAlreadyExistsError, DeviceNotFoundError


class MySqlDeviceRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add_device(self, device: dict) -> dict:
        row = Device(**device)
        self.session.add(row)
        try:
            self.session.commit()
            self.session.refresh(row)
            return self._device_dict(row)
        except IntegrityError as exc:
            self.session.rollback()
            raise DeviceAlreadyExistsError(device["device_id"]) from exc

    def list_devices(self) -> list[dict]:
        rows = self.session.scalars(select(Device).order_by(Device.id)).all()
        return [self._device_dict(row) for row in rows]

    def get_device(self, device_id: str) -> dict | None:
        row = self.session.scalar(select(Device).where(Device.device_id == device_id))
        return self._device_dict(row) if row else None

    def update_status(self, device_id: str, status: str) -> dict:
        row = self.session.scalar(select(Device).where(Device.device_id == device_id))
        if row is None:
            raise DeviceNotFoundError(device_id)
        row.status = status
        try:
            self.session.commit()
            self.session.refresh(row)
            return self._device_dict(row)
        except Exception:
            self.session.rollback()
            raise

    def save_alert(self, alert: dict) -> dict:
        row = Alert(**alert)
        self.session.add(row)
        try:
            self.session.commit()
            self.session.refresh(row)
            return self._alert_dict(row)
        except Exception:
            self.session.rollback()
            raise

    def list_alerts(self) -> list[dict]:
        rows = self.session.scalars(select(Alert).order_by(Alert.id)).all()
        return [self._alert_dict(row) for row in rows]

    @staticmethod
    def _device_dict(row: Device) -> dict:
        return {
            "device_id": row.device_id,
            "name": row.name,
            "device_type": row.device_type,
            "ip_address": row.ip_address,
            "status": row.status,
            "location": row.location,
        }

    @staticmethod
    def _alert_dict(row: Alert) -> dict:
        return {"device_id": row.device_id, "message": row.message, "timestamp": row.timestamp}
