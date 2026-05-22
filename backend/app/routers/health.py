from fastapi import APIRouter, HTTPException, Depends, status
from typing import List
from app.models.health import (
    VaccineRecord, VaccineRecordCreate, VaccineRecordUpdate,
    HealthRecord, HealthRecordCreate, HealthRecordUpdate
)
from app.database import get_supabase_client
from app.routers.auth import get_current_user
import logging

router = APIRouter()


# ================== 疫苗记录 API ==================

@router.get("/vaccines/{module_id}", response_model=List[VaccineRecord])
async def get_vaccine_records(
    module_id: str,
    user = Depends(get_current_user)
):
    """获取模块下的所有疫苗记录"""
    supabase = get_supabase_client()
    
    try:
        records = await supabase.select(
            "vaccine_records",
            "*",
            {"module_id": f"eq.{module_id}", "user_id": f"eq.{user['sub']}"},
            order_by="scheduled_date"
        )
        return records
    except Exception as e:
        logging.error(f"获取疫苗记录失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取疫苗记录失败"
        )


@router.post("/vaccines", response_model=VaccineRecord)
async def create_vaccine_record(
    record: VaccineRecordCreate,
    user = Depends(get_current_user)
):
    """创建疫苗记录"""
    supabase = get_supabase_client()
    
    try:
        data = record.model_dump()
        data["user_id"] = user["sub"]
        
        new_record = await supabase.insert("vaccine_records", data)
        return new_record[0]
    except Exception as e:
        logging.error(f"创建疫苗记录失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建疫苗记录失败"
        )


@router.put("/vaccines/{record_id}", response_model=VaccineRecord)
async def update_vaccine_record(
    record_id: str,
    record: VaccineRecordUpdate,
    user = Depends(get_current_user)
):
    """更新疫苗记录"""
    supabase = get_supabase_client()
    
    try:
        data = record.model_dump(exclude_unset=True)
        data["updated_at"] = "now()"
        
        updated = await supabase.update(
            "vaccine_records",
            data,
            {"id": f"eq.{record_id}", "user_id": f"eq.{user['sub']}"}
        )
        
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="疫苗记录不存在"
            )
        
        return updated[0]
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"更新疫苗记录失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新疫苗记录失败"
        )


@router.delete("/vaccines/{record_id}")
async def delete_vaccine_record(
    record_id: str,
    user = Depends(get_current_user)
):
    """删除疫苗记录"""
    supabase = get_supabase_client()
    
    try:
        await supabase.delete(
            "vaccine_records",
            {"id": f"eq.{record_id}", "user_id": f"eq.{user['sub']}"}
        )
        return {"message": "删除成功"}
    except Exception as e:
        logging.error(f"删除疫苗记录失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除疫苗记录失败"
        )


# ================== 健康档案 API ==================

@router.get("/health/{module_id}", response_model=List[HealthRecord])
async def get_health_records(
    module_id: str,
    user = Depends(get_current_user)
):
    """获取模块下的所有健康档案记录"""
    supabase = get_supabase_client()
    
    try:
        records = await supabase.select(
            "health_records",
            "*",
            {"module_id": f"eq.{module_id}", "user_id": f"eq.{user['sub']}"},
            order_by="date.desc"
        )
        return records
    except Exception as e:
        logging.error(f"获取健康档案失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="获取健康档案失败"
        )


@router.post("/health", response_model=HealthRecord)
async def create_health_record(
    record: HealthRecordCreate,
    user = Depends(get_current_user)
):
    """创建健康档案记录"""
    supabase = get_supabase_client()
    
    try:
        data = record.model_dump()
        data["user_id"] = user["sub"]
        
        new_record = await supabase.insert("health_records", data)
        return new_record[0]
    except Exception as e:
        logging.error(f"创建健康档案失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="创建健康档案失败"
        )


@router.put("/health/{record_id}", response_model=HealthRecord)
async def update_health_record(
    record_id: str,
    record: HealthRecordUpdate,
    user = Depends(get_current_user)
):
    """更新健康档案记录"""
    supabase = get_supabase_client()
    
    try:
        data = record.model_dump(exclude_unset=True)
        data["updated_at"] = "now()"
        
        updated = await supabase.update(
            "health_records",
            data,
            {"id": f"eq.{record_id}", "user_id": f"eq.{user['sub']}"}
        )
        
        if not updated:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="健康档案不存在"
            )
        
        return updated[0]
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"更新健康档案失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="更新健康档案失败"
        )


@router.delete("/health/{record_id}")
async def delete_health_record(
    record_id: str,
    user = Depends(get_current_user)
):
    """删除健康档案记录"""
    supabase = get_supabase_client()
    
    try:
        await supabase.delete(
            "health_records",
            {"id": f"eq.{record_id}", "user_id": f"eq.{user['sub']}"}
        )
        return {"message": "删除成功"}
    except Exception as e:
        logging.error(f"删除健康档案失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="删除健康档案失败"
        )
