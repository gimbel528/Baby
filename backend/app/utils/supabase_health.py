import logging
from datetime import datetime, timezone

import httpx

from app.config import get_settings

logger = logging.getLogger(__name__)


async def check_supabase_connection() -> dict:
    settings = get_settings()
    base = settings.SUPABASE_URL.rstrip("/")

    result = {
        "ok": False,
        "rest": False,
        "auth": False,
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "errors": [],
    }

    rest_headers = {
        "apikey": settings.SUPABASE_SERVICE_ROLE_KEY,
        "Authorization": f"Bearer {settings.SUPABASE_SERVICE_ROLE_KEY}",
    }
    auth_headers = {"apikey": settings.SUPABASE_ANON_KEY}

    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            rest = await client.get(f"{base}/rest/v1/", headers=rest_headers)
            result["rest"] = rest.status_code < 500
            if not result["rest"]:
                result["errors"].append(f"REST API HTTP {rest.status_code}")
        except Exception as e:
            result["errors"].append(f"REST API: {e}")

        try:
            auth = await client.get(f"{base}/auth/v1/health", headers=auth_headers)
            result["auth"] = auth.status_code == 200
            if not result["auth"]:
                result["errors"].append(f"Auth API HTTP {auth.status_code}")
        except Exception as e:
            result["errors"].append(f"Auth API: {e}")

    result["ok"] = result["rest"] and result["auth"]
    if result["ok"]:
        logger.info("Supabase connection OK (REST + Auth)")
    else:
        logger.error("Supabase connection failed: %s", result["errors"])

    return result
