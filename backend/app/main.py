from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, countdown, letters
from dotenv import load_dotenv
import os

# 加载环境变量（必须！否则连不上数据库）
load_dotenv()

app = FastAPI()

# 跨域（必须！否则前端连不上）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 加载所有接口
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(countdown.router, prefix="/api/countdown", tags=["countdown"])
app.include_router(letters.router, prefix="/api/letters", tags=["letters"])

# 健康检查
@app.get("/health")
async def health():
    return {"status": "ok"}