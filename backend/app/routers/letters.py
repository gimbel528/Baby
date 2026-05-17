from fastapi import APIRouter, HTTPException, Depends
from app.models.letter import LetterCreate, LetterUpdate
from app.routers.auth import get_current_user
from app.database import get_supabase_client, SupabaseClient
from datetime import datetime
import logging

router = APIRouter()


@router.post("/", response_model=dict)
async def create_letter(
    letter_data: LetterCreate,
    user = Depends(get_current_user)
):
    supabase = get_supabase_client()
    
    try:
        insert_data = {
            "user_id": user["sub"],
            "title": letter_data.title,
            "content": letter_data.content,
            "is_unlocked": False,
            "is_reminded": False
        }
        
        if letter_data.unlock_date:
            insert_data["unlock_date"] = letter_data.unlock_date.isoformat()
        
        if letter_data.reminder_date:
            insert_data["reminder_date"] = letter_data.reminder_date.isoformat()
        
        inserted = await supabase.insert("letters", insert_data)
        
        return {
            "message": "信件创建成功",
            "data": inserted
        }
    except Exception as e:
        logging.error(f"创建信件失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="创建信件失败"
        )


@router.get("/", response_model=list)
async def get_letters(user = Depends(get_current_user)):
    supabase = get_supabase_client()
    
    try:
        letters = await supabase.select("letters", "*", {
            "user_id": f"eq.{user['sub']}",
            "order": "created_at.desc"
        })
        
        result = []
        for letter in letters:
            is_unlocked = letter["is_unlocked"]
            
            if letter.get("unlock_date"):
                unlock_date = datetime.fromisoformat(letter["unlock_date"].replace("Z", "+00:00"))
                now = datetime.now(unlock_date.tzinfo)
                if now >= unlock_date:
                    is_unlocked = True
            
            letter_data = {
                **letter,
                "is_unlocked": is_unlocked
            }
            
            if not is_unlocked:
                letter_data["content"] = "🔒 信件尚未解锁"
            
            result.append(letter_data)
        
        return result
    except Exception as e:
        logging.error(f"获取信件列表失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取信件列表失败"
        )


@router.get("/{letter_id}", response_model=dict)
async def get_letter(
    letter_id: str,
    user = Depends(get_current_user)
):
    supabase = get_supabase_client()
    
    try:
        letters = await supabase.select("letters", "*", {
            "id": f"eq.{letter_id}",
            "user_id": f"eq.{user['sub']}"
        })
        
        if not letters:
            raise HTTPException(status_code=404, detail="信件不存在")
        
        letter = letters[0]
        is_unlocked = letter["is_unlocked"]
        
        if letter.get("unlock_date"):
            unlock_date = datetime.fromisoformat(letter["unlock_date"].replace("Z", "+00:00"))
            now = datetime.now(unlock_date.tzinfo)
            if now >= unlock_date:
                is_unlocked = True
        
        if not is_unlocked:
            letter["content"] = "🔒 信件尚未解锁"
        
        return {
            **letter,
            "is_unlocked": is_unlocked
        }
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"获取信件失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="获取信件失败"
        )


@router.put("/{letter_id}", response_model=dict)
async def update_letter(
    letter_id: str,
    letter_data: LetterUpdate,
    user = Depends(get_current_user)
):
    supabase = get_supabase_client()
    
    try:
        update_data = letter_data.model_dump(exclude_unset=True)
        
        if "unlock_date" in update_data:
            update_data["unlock_date"] = update_data["unlock_date"].isoformat()
        
        if "reminder_date" in update_data:
            update_data["reminder_date"] = update_data["reminder_date"].isoformat()
        
        updated = await supabase.update("letters", letter_id, update_data)
        
        if not updated:
            raise HTTPException(status_code=404, detail="信件不存在")
        
        return {
            "message": "更新成功",
            "data": updated
        }
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"更新信件失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="更新信件失败"
        )


@router.delete("/{letter_id}")
async def delete_letter(
    letter_id: str,
    user = Depends(get_current_user)
):
    supabase = get_supabase_client()
    
    try:
        await supabase.delete("letters", letter_id)
        return {"message": "删除成功"}
    except Exception as e:
        logging.error(f"删除信件失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="删除信件失败"
        )
