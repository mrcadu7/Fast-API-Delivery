from fastapi import FastAPI
from auth_routes import auth_router
from order_routes import order_router
from async_fastapi_jwt_auth import AuthJWT
from schemas import Settings
import inspect, re
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.openapi.utils import get_openapi

app=FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Delivey",
        version="Version 1.0.0",
        description="Freelance API",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {"bearerAuth": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT"
    }}

    openapi_schema["security"] = [{"bearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@AuthJWT.load_config
def get_config():
    return Settings()

app.include_router(auth_router)
app.include_router(order_router)
