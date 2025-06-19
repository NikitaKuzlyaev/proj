from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import HTMLResponse

from core.api.v1.routers import routers as routers_v1
from templates import templates

app = FastAPI()

for router in routers_v1:
    app.include_router(router=router, prefix="/api/v1")


@app.get("/", response_class=HTMLResponse)
async def root(
        request: Request,
):
    return templates.TemplateResponse("main.html",
                                      {"request": request})
