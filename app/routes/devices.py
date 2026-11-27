from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_repository
from app.models import AlertResponse, DeviceCreate, DeviceResponse, StatusUpdate
from app.services.device_service import (
    DeviceAlreadyExistsError,
    DeviceNotFoundError,
    DeviceService,
)

router = APIRouter(tags=["devices"])


def service(repository=Depends(get_repository)) -> DeviceService:
    return DeviceService(repository)


@router.post("/devices", response_model=DeviceResponse, status_code=status.HTTP_201_CREATED,
            responses={409: {"description": "Device ID already exists"}})
def register_device(payload: DeviceCreate, device_service: DeviceService = Depends(service)):
    try:
        return device_service.register(payload.model_dump())
    except DeviceAlreadyExistsError as exc:
        raise HTTPException(status_code=409, detail=f"Device {exc.args[0]} already exists") from exc


@router.get("/devices", response_model=list[DeviceResponse])
def list_devices(device_service: DeviceService = Depends(service)):
    return device_service.list()


@router.get("/devices/{device_id}", response_model=DeviceResponse,
           responses={404: {"description": "Device not found"}})
def get_device(device_id: str, device_service: DeviceService = Depends(service)):
    try:
        return device_service.get(device_id)
    except DeviceNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"Device {exc.args[0]} not found") from exc


@router.patch("/devices/{device_id}/status", response_model=DeviceResponse,
             responses={404: {"description": "Device not found"}})
def update_status(device_id: str, payload: StatusUpdate,
                  device_service: DeviceService = Depends(service)):
    try:
        return device_service.update_status(device_id, payload.status)
    except DeviceNotFoundError as exc:
        raise HTTPException(status_code=404, detail=f"Device {exc.args[0]} not found") from exc


@router.get("/alerts", response_model=list[AlertResponse])
def list_alerts(device_service: DeviceService = Depends(service)):
    return device_service.repository.list_alerts()


@router.get("/health")
def health():
    return {"status": "ok"}
