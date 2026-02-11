from fastapi import FastAPI
from .routers import health, generate, search, agent, chat

app = FastAPI(title="Compliance API", version="0.1.0")

app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(generate.router, prefix="/generate", tags=["generate"])
app.include_router(search.router, prefix="/search", tags=["search"])
app.include_router(agent.router, prefix="/agent", tags=["agent"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(chat.upload_router, prefix="/upload", tags=["upload"])
app.include_router(chat.onboard_router, prefix="/onboard", tags=["onboard"])