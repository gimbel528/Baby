import logging
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.routers import auth, countdown, letters, checklist, health
from app.utils.supabase_health import check_supabase_connection

load_dotenv()

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    status = await check_supabase_connection()
    if not status["ok"]:
        raise RuntimeError(
            "Supabase connection check failed: " + "; ".join(status["errors"])
        )
    app.state.supabase_status = status
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(countdown.router, prefix="/api/countdown", tags=["countdown"])
app.include_router(letters.router, prefix="/api/letters", tags=["letters"])
app.include_router(checklist.router, prefix="/api/checklist", tags=["checklist"])
app.include_router(health.router, prefix="/api/health", tags=["health"])


@app.get("/health")
async def health():
    status = await check_supabase_connection()
    body = {"status": "ok" if status["ok"] else "degraded", "supabase": status}
    if not status["ok"]:
        return JSONResponse(status_code=503, content=body)
    return body
