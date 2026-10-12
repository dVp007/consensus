from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import get_settings
from app.db import init_db
from app.routers import chat, plans, proposals, ws

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.app_name, lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(plans.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(proposals.router, prefix="/api")
app.include_router(ws.router)


@app.get("/api/health")
def health() -> dict:
    return {"status": "ok", "llm_configured": bool(settings.openrouter_api_key)}
