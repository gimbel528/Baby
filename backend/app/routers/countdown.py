from fastapi import APIRouter, HTTPException, Depends
from app.models.countdown import CountdownEventCreate, CountdownEventUpdate, CountdownEvent
from app.routers.auth import get_current_user
from app.database import get_supabase_client, SupabaseClient
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
        inserted = await supabase.insert("countdown_events", {
            "user_id": user["sub"],
            "event_name": event_data.event_name,
            "target_date": event_data.target_date.isoformat(),
            "event_type": event_data.event_type,
            "is_active": True
        })
        
        return {
            "message": "倒计时事件创建成功",
            "data": inserted
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
        events = await supabase.select("countdown_events", "*", {
            "user_id": f"eq.{user['sub']}",
            "is_active": "eq.true"
        })
        
        result = []
        for event in events:
            target_date = datetime.fromisoformat(event["target_date"].replace("Z", "+00:00"))
            now = datetime.now(target_date.tzinfo)
            days_remaining = (target_date - now).days
            
            result.append({
                **event,
                "days_remaining": days_remaining,
                "is_expired": days_remaining < 0
            })
        
        return result
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
        events = await supabase.select("countdown_events", "*", {
            "id": f"eq.{event_id}",
            "user_id": f"eq.{user['sub']}"
        })
        
        if not events:
            raise HTTPException(status_code=404, detail="倒计时事件不存在")
        
        event = events[0]
        target_date = datetime.fromisoformat(event["target_date"].replace("Z", "+00:00"))
        now = datetime.now(target_date.tzinfo)
        days_remaining = (target_date - now).days
        
        return {
            **event,
            "days_remaining": days_remaining,
            "is_expired": days_remaining < 0
        }
    except HTTPException:
        raise
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
        update_data = event_data.model_dump(exclude_unset=True)
        
        if "target_date" in update_data:
            update_data["target_date"] = update_data["target_date"].isoformat()
        
        updated = await supabase.update("countdown_events", event_id, update_data)
        
        if not updated:
            raise HTTPException(status_code=404, detail="倒计时事件不存在")
        
        return {
            "message": "更新成功",
            "data": updated
        }
    except HTTPException:
        raise
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
        await supabase.delete("countdown_events", event_id)
        return {"message": "删除成功"}
    except Exception as e:
        logging.error(f"删除倒计时事件失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="删除倒计时事件失败"
        )
