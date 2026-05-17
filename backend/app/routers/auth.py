from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.user import UserCreate, UserLogin, Token
from app.database import get_supabase_client
from app.config import get_settings
import logging
import httpx

router = APIRouter()
security = HTTPBearer()
settings = get_settings()

# ====================== 最终修复版 ======================
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials

    try:
        # 官方接口验证 Token，100% 稳定
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                url=f"{settings.SUPABASE_URL}/auth/v1/user",
                headers={
                    "Authorization": f"Bearer {token}",
                    "apikey": settings.SUPABASE_ANON_KEY
                }
            )
            response.raise_for_status()
            user = response.json()

        if not user or "id" not in user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证凭证"
            )

        return {"sub": user["id"]}
    except Exception as e:
        logging.error(f"Token验证失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证"
        )
# ==========================================================

async def _auth_request(method: str, path: str, data: dict = None, use_form: bool = False) -> dict:
    url = f"{settings.SUPABASE_URL.rstrip('/')}/auth/v1{path}"
    headers = {
        "apikey": settings.SUPABASE_ANON_KEY
    }
    
    logging.info(f"Auth request: {method} {url}")
    logging.info(f"Data: {data}")
    logging.info(f"Use form: {use_form}")
    
    request_kwargs = {}
    if use_form:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        request_kwargs["data"] = data
    else:
        headers["Content-Type"] = "application/json"
        request_kwargs["json"] = data
    
    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.request(
            method=method,
            url=url,
            headers=headers,
            **request_kwargs
        )
        logging.info(f"Response status: {response.status_code}")
        logging.info(f"Response body: {response.text}")
        response.raise_for_status()
        return response.json()


@router.post("/register", response_model=dict)
async def register(user_data: UserCreate):
    try:
        auth_response = await _auth_request("POST", "/signup", {
            "email": user_data.email,
            "password": user_data.password,
            "data": {
                "username": user_data.username
            }
        })
        
        user_id = auth_response.get("user", {}).get("id")
        
        if user_id:
            # 检查 profile 是否已经被触发器创建
            profiles = await get_supabase_client().select("profiles", "*", {"id": f"eq.{user_id}"})
            
            if not profiles:
                # 如果没有，才创建
                await get_supabase_client().insert("profiles", {
                    "id": user_id,
                    "username": user_data.username
                })
            
            return {
                "message": "注册成功，请登录",
                "user_id": user_id
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="注册失败"
            )
    except httpx.HTTPStatusError as e:
        logging.error(f"注册失败: {e.response.text}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"注册失败: {e.response.text}"
        )
    except Exception as e:
        logging.error(f"注册失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    try:
        auth_response = await _auth_request(
            "POST",
            "/token?grant_type=password",
            {
                "email": user_data.email,
                "password": user_data.password
            },
            use_form=False
        )
        
        access_token = auth_response.get("access_token")
        
        if access_token:
            return Token(
                access_token=access_token,
                token_type="bearer"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="邮箱或密码错误"
            )
    except httpx.HTTPStatusError as e:
        logging.error(f"登录失败: {e.response.text}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误"
        )
    except Exception as e:
        logging.error(f"登录失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码错误"
        )


@router.get("/me", response_model=dict)
async def get_current_user_info(user = Depends(get_current_user)):
    supabase = get_supabase_client()
    
    try:
        profiles = await supabase.select("profiles", "*", {"id": f"eq.{user['sub']}"})
        
        if profiles:
            return profiles[0]
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
    except Exception as e:
        logging.error(f"获取用户信息失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取用户信息失败"
        )


@router.post("/logout")
async def logout(user = Depends(get_current_user)):
    return {"message": "登出成功"}