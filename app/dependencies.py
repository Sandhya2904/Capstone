from app.config import NETPULSE_STORAGE
from app.db.session import SessionLocal
from app.repositories.device_repository import InMemoryDeviceRepository
from app.repositories.mysql_device_repository import MySqlDeviceRepository

_memory_repository = InMemoryDeviceRepository()


def get_repository():
    if NETPULSE_STORAGE == "mysql":
        session = SessionLocal()
        try:
            yield MySqlDeviceRepository(session)
        finally:
            session.close()
    else:
        yield _memory_repository
