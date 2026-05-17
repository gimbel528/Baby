# 必须放在最顶部！
from dotenv import load_dotenv
load_dotenv()  # 加载 .env 文件

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.routers import auth, countdown, letters
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.utils.keepalive import ping_supabase
from app.config import get_settings
import logging
import os

settings = get_settings()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="Baby Growth Tracker API",
    description="宝宝成长记录系统 API",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)

ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["认证"])
app.include_router(countdown.router, prefix="/api/countdown", tags=["倒计时"])
app.include_router(letters.router, prefix="/api/letters", tags=["信件"])

STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "dist")

if os.path.exists(STATIC_DIR):
    app.mount("/assets", StaticFiles(directory=os.path.join(STATIC_DIR, "assets")), name="assets")
    logging.info(f"📦 Static files mounted from {STATIC_DIR}")

scheduler = AsyncIOScheduler()


@app.on_event("startup")
async def startup_event():
    scheduler.add_job(ping_supabase, 'interval', hours=6)
    scheduler.start()
    logging.info("🚀 Supabase Keep-Alive Scheduler Started")


@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if os.path.exists(STATIC_DIR):
    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        file_path = os.path.join(STATIC_DIR, full_path)
        if full_path and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(os.path.join(STATIC_DIR, "index.html"))
