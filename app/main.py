from fastapi import FastAPI

from app.routes.devices import router

app = FastAPI(
    title="NetPulse Network Monitoring API",
    description="A layered FastAPI device-monitoring API with an in-memory repository.",
    version="1.0.0",
)
app.include_router(router)
