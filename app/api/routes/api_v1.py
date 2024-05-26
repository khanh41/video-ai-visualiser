"""API Routes."""
from fastapi import APIRouter

from app.api.routes import visualizer_route

app = APIRouter(prefix="/v1")

app.include_router(visualizer_route.router, tags=["Visualizer"], prefix="/visualizer")
