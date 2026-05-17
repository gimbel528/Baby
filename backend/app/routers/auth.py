from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.models.user import UserCreate, UserLogin, Token
from app.database import get_supabase_client
from app.utils.auth import verify_password, get_password_hash, create_access_token
from jose import jwt, JWTError
from app.config import get_settings
import logging

router = APIRouter()
security = HTTPBearer()
settings = get_settings()


async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, settings.SUPABASE_JWT_SECRET, algorithms=["HS256"])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="无效的认证凭证"
            )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证"
        )


@router.post("/register", response_model=dict)
async def register(user_data: UserCreate):
    supabase = get_supabase_client()
    
    try:
        response = supabase.auth.sign_up({
            "email": user_data.email,
            "password": user_data.password,
            "options": {
                "data": {
                    "username": user_data.username
                }
            }
        })
        
        if response.user:
            from supabase import create_client
            admin_client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_SERVICE_ROLE_KEY
            )
            
            try:
                admin_client.auth.admin.update_user_by_id(
                    response.user.id,
                    {"email_confirm": True}
                )
                logging.info(f"用户 {response.user.id} 已自动确认")
            except Exception as confirm_error:
                logging.warning(f"自动确认失败: {str(confirm_error)}")
            
            supabase.table("profiles").insert({
                "id": response.user.id,
                "username": user_data.username
            }).execute()
            
            return {
                "message": "注册成功，请登录",
                "user_id": response.user.id
            }
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="注册失败"
            )
    except Exception as e:
        logging.error(f"注册失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/login", response_model=Token)
async def login(user_data: UserLogin):
    supabase = get_supabase_client()
    
    try:
        response = supabase.auth.sign_in_with_password({
            "email": user_data.email,
            "password": user_data.password
        })
        
        if response.session:
            return Token(
                access_token=response.session.access_token,
                token_type="bearer"
            )
        else:
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
        response = supabase.table("profiles").select("*").eq("id", user["sub"]).execute()
        
        if response.data:
            return response.data[0]
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
    supabase = get_supabase_client()
    
    try:
        supabase.auth.sign_out()
        return {"message": "登出成功"}
    except Exception as e:
        logging.error(f"登出失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="登出失败"
        )
