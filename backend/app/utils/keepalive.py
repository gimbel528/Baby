import httpx
from app.config import get_settings
from datetime import datetime
import logging

settings = get_settings()


async def ping_supabase():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"{settings.SUPABASE_URL}/rest/v1/",
                headers={
                    "apikey": settings.SUPABASE_ANON_KEY,
                    "Authorization": f"Bearer {settings.SUPABASE_ANON_KEY}"
                },
                timeout=10.0
            )
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.info(f"[{timestamp}] Keep-alive ping - Status: {response.status_code}")
            
        except Exception as e:
            logging.error(f"Keep-alive failed: {e}")
