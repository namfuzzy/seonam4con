from fastapi import APIRouter

from app.api.routes import auth, health, integrations, projects, sites

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(auth.router)
api_router.include_router(projects.router)
api_router.include_router(sites.router)
api_router.include_router(integrations.router)
