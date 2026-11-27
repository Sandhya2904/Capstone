from datetime import datetime
from ipaddress import IPv4Address
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DeviceCreate(BaseModel):
    model_config = ConfigDict(json_schema_extra={"examples": [{
        "device_id": "RTR-101",
        "name": "Branch Router",
        "device_type": "router",
        "ip_address": "192.168.10.1",
        "status": "online",
        "location": None,
    }]})

    device_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    device_type: Literal["router", "switch", "server"]
    ip_address: str
    status: Literal["online", "offline"] = "online"
    location: str | None = None

    @field_validator("ip_address")
    @classmethod
    def validate_ipv4(cls, value: str) -> str:
        IPv4Address(value)
        return value


class DeviceResponse(BaseModel):
    device_id: str
    name: str
    device_type: Literal["router", "switch", "server"]
    ip_address: str
    status: Literal["online", "offline"]
    location: str | None = None


class StatusUpdate(BaseModel):
    model_config = ConfigDict(json_schema_extra={"examples": [{"status": "offline"}]})

    status: Literal["online", "offline"]


class AlertResponse(BaseModel):
    device_id: str
    message: str
    timestamp: datetime
