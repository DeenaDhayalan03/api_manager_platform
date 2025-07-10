from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from scripts.core.service.auth_service import router as auth_router
from scripts.core.service.plan_service import router as plan_router
from scripts.core.service.service_service import router as service_router
from scripts.core.service.endpoint_credits_service import router as credit_router
from scripts.core.service.summary_service import router as summary_router
from scripts.core.service.proxy_service import router as proxy_router

from scripts.core.utils.mqtt_utils.mqtt_client import connect_mqtt


def create_app() -> FastAPI:
    app = FastAPI(title="API Management System")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router, tags=["Authentication"])
    app.include_router(plan_router, tags=["Plans"])
    app.include_router(service_router, tags=["Services"])
    app.include_router(credit_router, tags=["Endpoint Credits"])
    app.include_router(summary_router, tags=["Invoices"])
    app.include_router(proxy_router, tags=["Proxy Gateway"])

    @app.on_event("startup")
    def startup_event():
        connect_mqtt()

    return app
