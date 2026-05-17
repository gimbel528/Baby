from fastapi import APIRouter, HTTPException, Depends
from app.models.countdown import CountdownEventCreate, CountdownEventUpdate, CountdownEvent
from app.routers.auth import get_current_user
from app.database import get_supabase_client
from datetime import datetime
import logging

router = APIRouter()


@router.post("/", response_model=dict)
async def create_countdown_event(
    event_data: CountdownEventCreate,
    user = Depends(get_current_user)
):
    supabase = get_supabase_client()
    
    try:
        response = supabase.table("countdown_events").insert({
            "user_id": user["sub"],
            "event_name": event_data.event_name,
            "target_date": event_data.target_date.isoformat(),
            "event_type": event_data.event_type,
            "is_active": True
        }).execute()
        
        return {
            "message": "倒计时事件创建成功",
            "data": response.data[0]
        }
    except Exception as e:
        logging.error(f"创建倒计时事件失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="创建倒计时事件失败"
        )


@router.get("/", response_model=list)
async def get_countdown_events(user = Depends(get_current_user)):
    supabase = get_supabase_client()
    
    try:
        response = supabase.table("countdown_events").select("*").eq("user_id", user["sub"]).eq("is_active", True).execute()
        
        events = []
        for event in response.data:
            target_date = datetime.fromisoformat(event["target_date"].replace("Z", "+00:00"))
            now = datetime.now(target_date.tzinfo)
            days_remaining = (target_date - now).days
            
            events.append({
                **event,
                "days_remaining": days_remaining,
                "is_expired": days_remaining < 0
            })
        
        return events
    except Exception as e:
        logging.error(f"获取倒计时事件失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取倒计时事件失败"
        )


@router.get("/{event_id}", response_model=dict)
async def get_countdown_event(
    event_id: str,
    user = Depends(get_current_user)
):
    supabase = get_supabase_client()
    
    try:
        response = supabase.table("countdown_events").select("*").eq("id", event_id).eq("user_id", user["sub"]).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="倒计时事件不存在")
        
        event = response.data[0]
        target_date = datetime.fromisoformat(event["target_date"].replace("Z", "+00:00"))
        now = datetime.now(target_date.tzinfo)
        days_remaining = (target_date - now).days
        
        return {
            **event,
            "days_remaining": days_remaining,
            "is_expired": days_remaining < 0
        }
    except Exception as e:
        logging.error(f"获取倒计时事件失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取倒计时事件失败"
        )


@router.put("/{event_id}", response_model=dict)
async def update_countdown_event(
    event_id: str,
    event_data: CountdownEventUpdate,
    user = Depends(get_current_user)
):
    supabase = get_supabase_client()
    
    try:
        update_data = event_data.dict(exclude_unset=True)
        
        if "target_date" in update_data:
            update_data["target_date"] = update_data["target_date"].isoformat()
        
        response = supabase.table("countdown_events").update(update_data).eq("id", event_id).eq("user_id", user["sub"]).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="倒计时事件不存在")
        
        return {
            "message": "更新成功",
            "data": response.data[0]
        }
    except Exception as e:
        logging.error(f"更新倒计时事件失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="更新倒计时事件失败"
        )


@router.delete("/{event_id}")
async def delete_countdown_event(
    event_id: str,
    user = Depends(get_current_user)
):
    supabase = get_supabase_client()
    
    try:
        response = supabase.table("countdown_events").delete().eq("id", event_id).eq("user_id", user["sub"]).execute()
        
        if not response.data:
            raise HTTPException(status_code=404, detail="倒计时事件不存在")
        
        return {"message": "删除成功"}
    except Exception as e:
        logging.error(f"删除倒计时事件失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="删除倒计时事件失败"
        )
