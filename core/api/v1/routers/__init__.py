from core.api.v1.routers.admin import router as admin_router
from core.api.v1.routers.application import router as application_router
from core.api.v1.routers.auth import router as auth_router
from core.api.v1.routers.offer import router as offer_router
from core.api.v1.routers.organization import router as organization_router
from core.api.v1.routers.permissions import router as permissions
from core.api.v1.routers.project import router as project_router
from core.api.v1.routers.vacancy import router as vacancy_router

routers = [auth_router, organization_router, project_router, vacancy_router, permissions, admin_router,
           offer_router, application_router]
