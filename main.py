from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from core.api.v1.routers import routers as routers_v1
from core.database.connection import engine, Base
from templates import templates
from fastapi import FastAPI
from fastapi.openapi.models import OAuthFlows as OAuthFlowsModel, SecurityScheme as SecuritySchemeModel
from fastapi.openapi.utils import get_openapi

app = FastAPI()

# Разрешённые источники (в разработке можно '*')
origins = [
    "http://localhost:5173",
    "http://192.168.0.2:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # или ["*"] для всех
    allow_credentials=True,
    allow_methods=["*"],  # или ['GET', 'POST', ...]
    allow_headers=["*"],  # или ['Content-Type', 'Authorization']
)

for router in routers_v1:
    app.include_router(router=router, prefix="/api/v1")


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="My API",
        version="1.0.0",
        description="API with OAuth2 Password Flow",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "OAuth2PasswordBearer": {
            "type": "oauth2",
            "flows": {
                "password": {
                    "tokenUrl": "/api/v1/auth/login",
                    "scopes": {}
                }
            }
        }
    }

    # Вешаем security requirement на все пути (если нужно)
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method.setdefault("security", [{"OAuth2PasswordBearer": []}])

    app.openapi_schema = openapi_schema
    return app.openapi_schema


@app.get("/ping", response_class=JSONResponse)
async def ping():
    return JSONResponse(content={"message": "its ok!"})


app.openapi = custom_openapi


# @app.on_event("startup")
# async def on_startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)


@app.get("/", response_class=HTMLResponse)
async def root(
        request: Request,
):
    return templates.TemplateResponse("main.html",
                                      {"request": request})
