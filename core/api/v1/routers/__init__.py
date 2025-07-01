from core.api.v1.routers.auth import router as auth_router
from core.api.v1.routers.organization import router as organization_router
from core.api.v1.routers.employee import router as employee_router
from core.api.v1.routers.project import router as project_router
from core.api.v1.routers.offer import router as offer_router
from core.api.v1.routers.permissions import router as permissions
from core.api.v1.routers.vacancy import router as vacancy_router
from core.api.v1.routers.admin import router as admin_router

routers = [auth_router, organization_router, employee_router, project_router,
           offer_router, vacancy_router, permissions, admin_router, ]
