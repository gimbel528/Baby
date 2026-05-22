from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Optional
from app.models.checklist import (
    Module, ModuleCreate, ModuleUpdate,
    ItemCategory, ItemCategoryCreate, ItemCategoryUpdate,
    ChecklistItem, ChecklistItemCreate, ChecklistItemUpdate
)
from app.database import SupabaseClient
from app.config import get_settings
import logging
import httpx

router = APIRouter()
logger = logging.getLogger(__name__)
security = HTTPBearer()
settings = get_settings()


async def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    token = credentials.credentials

    try:
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

        return user["id"]
    except Exception as e:
        logger.error(f"Token验证失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证凭证"
        )


# ==================== 功能模块 API ====================

async def ensure_default_modules(user_id: str, db: SupabaseClient):
    """确保用户有三个默认模块"""
    # 检查是否已有模块
    existing = await db._request(
        "GET",
        "/modules",
        params={"user_id": f"eq.{user_id}"}
    )
    
    existing_names = [m["name"] for m in existing] if existing else []
    
    default_modules = [
        {
            "name": "物品明细",
            "icon": "📦",
            "description": "待产包及其他物品清单",
            "sort_order": 1,
            "module_type": "checklist",
            "user_id": user_id
        },
        {
            "name": "疫苗记录",
            "icon": "💉",
            "description": "宝宝疫苗接种记录",
            "sort_order": 2,
            "module_type": "vaccine",
            "user_id": user_id
        },
        {
            "name": "健康档案",
            "icon": "📋",
            "description": "宝宝健康数据记录",
            "sort_order": 3,
            "module_type": "health",
            "user_id": user_id
        }
    ]
    
    for module_data in default_modules:
        if module_data["name"] not in existing_names:
            await db._request(
                "POST",
                "/modules",
                json=module_data
            )


@router.get("/modules", response_model=List[Module])
async def get_modules(user_id: str = Depends(get_current_user_id)):
    try:
        db = SupabaseClient()
        
        # 确保有默认模块
        await ensure_default_modules(user_id, db)
        
        # 获取所有模块
        result = await db._request(
            "GET",
            "/modules",
            params={
                "user_id": f"eq.{user_id}",
                "order": "sort_order.asc,created_at.asc"
            }
        )
        return result
    except Exception as e:
        logger.error(f"获取功能模块失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/modules", response_model=Module)
async def create_module(
    module: ModuleCreate,
    user_id: str = Depends(get_current_user_id)
):
    try:
        db = SupabaseClient()
        data = module.dict()
        data["user_id"] = user_id
        
        result = await db._request(
            "POST",
            "/modules",
            json=data
        )
        
        if result and len(result) > 0:
            return result[0]
        
        raise HTTPException(status_code=500, detail="创建功能模块失败")
    except Exception as e:
        logger.error(f"创建功能模块失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/modules/{module_id}", response_model=Module)
async def update_module(
    module_id: str,
    module: ModuleUpdate,
    user_id: str = Depends(get_current_user_id)
):
    try:
        db = SupabaseClient()
        
        result = await db._request(
            "PATCH",
            "/modules",
            json=module.dict(exclude_unset=True),
            params={
                "id": f"eq.{module_id}",
                "user_id": f"eq.{user_id}"
            }
        )
        
        if result and len(result) > 0:
            return result[0]
        
        raise HTTPException(status_code=404, detail="功能模块不存在")
    except Exception as e:
        logger.error(f"更新功能模块失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/modules/{module_id}")
async def delete_module(
    module_id: str,
    user_id: str = Depends(get_current_user_id)
):
    try:
        db = SupabaseClient()
        
        # 先获取模块信息
        module = await db._request(
            "GET",
            "/modules",
            params={
                "id": f"eq.{module_id}",
                "user_id": f"eq.{user_id}"
            }
        )
        
        if not module or len(module) == 0:
            raise HTTPException(status_code=404, detail="模块不存在")
        
        module_data = module[0]
        
        # 检查是否是默认模块
        default_names = ["物品明细", "疫苗记录", "健康档案"]
        if module_data["name"] in default_names:
            raise HTTPException(status_code=400, detail="默认模块不能删除")
        
        # 执行删除
        await db._request(
            "DELETE",
            "/modules",
            params={
                "id": f"eq.{module_id}",
                "user_id": f"eq.{user_id}"
            }
        )
        
        return {"message": "删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"删除功能模块失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 物品分类 API ====================

@router.get("/categories", response_model=List[ItemCategory])
async def get_categories(
    module_id: Optional[str] = None,
    user_id: str = Depends(get_current_user_id)
):
    try:
        db = SupabaseClient()
        
        params = {"user_id": f"eq.{user_id}", "order": "sort_order.asc,created_at.asc"}
        
        if module_id:
            params["module_id"] = f"eq.{module_id}"
        
        result = await db._request(
            "GET",
            "/item_categories",
            params=params
        )
        
        return result
    except Exception as e:
        logger.error(f"获取物品分类失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/categories", response_model=ItemCategory)
async def create_category(
    category: ItemCategoryCreate,
    user_id: str = Depends(get_current_user_id)
):
    try:
        db = SupabaseClient()
        data = category.dict()
        data["user_id"] = user_id
        
        result = await db._request(
            "POST",
            "/item_categories",
            json=data
        )
        
        if result and len(result) > 0:
            return result[0]
        
        raise HTTPException(status_code=500, detail="创建物品分类失败")
    except Exception as e:
        logger.error(f"创建物品分类失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/categories/{category_id}", response_model=ItemCategory)
async def update_category(
    category_id: str,
    category: ItemCategoryUpdate,
    user_id: str = Depends(get_current_user_id)
):
    try:
        db = SupabaseClient()
        
        result = await db._request(
            "PATCH",
            "/item_categories",
            json=category.dict(exclude_unset=True),
            params={
                "id": f"eq.{category_id}",
                "user_id": f"eq.{user_id}"
            }
        )
        
        if result and len(result) > 0:
            return result[0]
        
        raise HTTPException(status_code=404, detail="物品分类不存在")
    except Exception as e:
        logger.error(f"更新物品分类失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/categories/{category_id}")
async def delete_category(
    category_id: str,
    user_id: str = Depends(get_current_user_id)
):
    try:
        db = SupabaseClient()
        
        await db._request(
            "DELETE",
            "/item_categories",
            params={
                "id": f"eq.{category_id}",
                "user_id": f"eq.{user_id}"
            }
        )
        
        return {"message": "删除成功"}
    except Exception as e:
        logger.error(f"删除物品分类失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ==================== 物品清单 API ====================

@router.get("/items", response_model=List[ChecklistItem])
async def get_items(
    module_id: Optional[str] = None,
    category_id: Optional[str] = None,
    status: Optional[str] = None,
    user_id: str = Depends(get_current_user_id)
):
    try:
        db = SupabaseClient()
        
        params = {"user_id": f"eq.{user_id}", "order": "sort_order.asc,created_at.asc"}
        
        if module_id:
            params["module_id"] = f"eq.{module_id}"
        
        if category_id:
            params["category_id"] = f"eq.{category_id}"
        
        if status:
            params["status"] = f"eq.{status}"
        
        result = await db._request(
            "GET",
            "/checklist_items",
            params=params
        )
        
        return result
    except Exception as e:
        logger.error(f"获取物品清单失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/items", response_model=ChecklistItem)
async def create_item(
    item: ChecklistItemCreate,
    user_id: str = Depends(get_current_user_id)
):
    try:
        db = SupabaseClient()
        data = item.dict()
        data["user_id"] = user_id
        
        result = await db._request(
            "POST",
            "/checklist_items",
            json=data
        )
        
        if result and len(result) > 0:
            return result[0]
        
        raise HTTPException(status_code=500, detail="创建物品失败")
    except Exception as e:
        logger.error(f"创建物品失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/items/{item_id}", response_model=ChecklistItem)
async def update_item(
    item_id: str,
    item: ChecklistItemUpdate,
    user_id: str = Depends(get_current_user_id)
):
    try:
        db = SupabaseClient()
        
        result = await db._request(
            "PATCH",
            "/checklist_items",
            json=item.dict(exclude_unset=True),
            params={
                "id": f"eq.{item_id}",
                "user_id": f"eq.{user_id}"
            }
        )
        
        if result and len(result) > 0:
            return result[0]
        
        raise HTTPException(status_code=404, detail="物品不存在")
    except Exception as e:
        logger.error(f"更新物品失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/items/{item_id}")
async def delete_item(
    item_id: str,
    user_id: str = Depends(get_current_user_id)
):
    try:
        db = SupabaseClient()
        
        await db._request(
            "DELETE",
            "/checklist_items",
            params={
                "id": f"eq.{item_id}",
                "user_id": f"eq.{user_id}"
            }
        )
        
        return {"message": "删除成功"}
    except Exception as e:
        logger.error(f"删除物品失败: {e}")
        raise HTTPException(status_code=500, detail=str(e))
