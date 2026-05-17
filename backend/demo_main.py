from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, timedelta
from typing import Optional, List
import secrets
import logging
import uuid

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title="Baby Growth Tracker API (Demo)",
    description="宝宝成长记录系统 API - 演示版本",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

users_db = {}
countdown_events_db = {}
letters_db = {}
tokens_db = {}


class UserCreate(BaseModel):
    email: str
    username: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class CountdownEventCreate(BaseModel):
    event_name: str
    target_date: datetime
    event_type: str = "custom"


class LetterCreate(BaseModel):
    title: str
    content: str
    unlock_date: Optional[datetime] = None
    reminder_date: Optional[datetime] = None


def create_access_token(user_id: str):
    token = secrets.token_urlsafe(32)
    tokens_db[token] = user_id
    return token


def get_current_user(token: str):
    if token not in tokens_db:
        raise HTTPException(status_code=401, detail="无效的认证凭证")
    
    user_id = tokens_db[token]
    if user_id not in users_db:
        raise HTTPException(status_code=401, detail="用户不存在")
    
    return users_db[user_id]


@app.get("/")
async def root():
    return {
        "message": "Baby Growth Tracker API (Demo)",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/api/auth/register", response_model=dict)
async def register(user_data: UserCreate):
    for user in users_db.values():
        if user["email"] == user_data.email:
            raise HTTPException(status_code=400, detail="邮箱已被注册")
    
    user_id = str(uuid.uuid4())
    users_db[user_id] = {
        "id": user_id,
        "email": user_data.email,
        "username": user_data.username,
        "password": user_data.password,
        "created_at": datetime.utcnow()
    }
    
    logging.info(f"用户注册成功: {user_data.email}")
    
    return {
        "message": "注册成功，请登录",
        "user_id": user_id
    }


@app.post("/api/auth/login", response_model=Token)
async def login(user_data: UserLogin):
    user = None
    for u in users_db.values():
        if u["email"] == user_data.email and u["password"] == user_data.password:
            user = u
            break
    
    if not user:
        raise HTTPException(status_code=401, detail="邮箱或密码错误")
    
    access_token = create_access_token(user["id"])
    
    logging.info(f"用户登录成功: {user_data.email}")
    
    return Token(
        access_token=access_token,
        token_type="bearer"
    )


@app.get("/api/auth/me")
async def get_current_user_info(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未提供认证凭证")
    
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token)
    
    return {
        "id": user["id"],
        "email": user["email"],
        "username": user["username"]
    }


@app.post("/api/auth/logout")
async def logout():
    return {"message": "登出成功"}


@app.post("/api/countdown/")
async def create_countdown_event(
    event_data: CountdownEventCreate,
    authorization: Optional[str] = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未提供认证凭证")
    
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token)
    
    event_id = str(uuid.uuid4())
    countdown_events_db[event_id] = {
        "id": event_id,
        "user_id": user["id"],
        "event_name": event_data.event_name,
        "target_date": event_data.target_date.isoformat(),
        "event_type": event_data.event_type,
        "is_active": True,
        "created_at": datetime.utcnow().isoformat()
    }
    
    return {
        "message": "倒计时事件创建成功",
        "data": countdown_events_db[event_id]
    }


@app.get("/api/countdown/")
async def get_countdown_events(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未提供认证凭证")
    
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token)
    
    events = []
    for event in countdown_events_db.values():
        if event["user_id"] == user["id"] and event["is_active"]:
            target_date = datetime.fromisoformat(event["target_date"])
            now = datetime.utcnow()
            days_remaining = (target_date - now).days
            
            events.append({
                **event,
                "days_remaining": days_remaining,
                "is_expired": days_remaining < 0
            })
    
    return events


@app.post("/api/letters/")
async def create_letter(
    letter_data: LetterCreate,
    authorization: Optional[str] = Header(None)
):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未提供认证凭证")
    
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token)
    
    letter_id = str(uuid.uuid4())
    letters_db[letter_id] = {
        "id": letter_id,
        "user_id": user["id"],
        "title": letter_data.title,
        "content": letter_data.content,
        "unlock_date": letter_data.unlock_date.isoformat() if letter_data.unlock_date else None,
        "reminder_date": letter_data.reminder_date.isoformat() if letter_data.reminder_date else None,
        "is_unlocked": True,
        "is_reminded": False,
        "created_at": datetime.utcnow().isoformat()
    }
    
    return {
        "message": "信件创建成功",
        "data": letters_db[letter_id]
    }


@app.get("/api/letters/")
async def get_letters(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未提供认证凭证")
    
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token)
    
    letters = []
    for letter in letters_db.values():
        if letter["user_id"] == user["id"]:
            letters.append(letter)
    
    return sorted(letters, key=lambda x: x["created_at"], reverse=True)


@app.get("/api/letters/{letter_id}")
async def get_letter(letter_id: str, authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未提供认证凭证")
    
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token)
    
    if letter_id not in letters_db:
        raise HTTPException(status_code=404, detail="信件不存在")
    
    letter = letters_db[letter_id]
    
    if letter["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="信件不存在")
    
    return letter


@app.delete("/api/letters/{letter_id}")
async def delete_letter(letter_id: str, authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未提供认证凭证")
    
    token = authorization.replace("Bearer ", "")
    user = get_current_user(token)
    
    if letter_id not in letters_db:
        raise HTTPException(status_code=404, detail="信件不存在")
    
    letter = letters_db[letter_id]
    
    if letter["user_id"] != user["id"]:
        raise HTTPException(status_code=404, detail="信件不存在")
    
    del letters_db[letter_id]
    
    return {"message": "删除成功"}
