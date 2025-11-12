from fastapi import FastAPI
from .routers import health, generate, search

app = FastAPI(title="Compliance API", version="0.1.0")

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(generate.router, prefix="/generate", tags=["generate"])
app.include_router(search.router, prefix="/search", tags=["search"])