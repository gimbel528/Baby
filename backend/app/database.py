import httpx
from typing import Optional
from app.config import get_settings

settings = get_settings()


class SupabaseClient:
    def __init__(self):
        self.base_url = settings.SUPABASE_URL.rstrip('/')
        self.service_role_key = settings.SUPABASE_SERVICE_ROLE_KEY
        self.anon_key = settings.SUPABASE_ANON_KEY
        self.timeout = 30.0

    def _get_headers(self, use_service_role: bool = True) -> dict:
        key = self.service_role_key if use_service_role else self.anon_key
        return {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
            "Prefer": "return=representation"
        }

    async def _request(
        self,
        method: str,
        path: str,
        json: Optional[dict] = None,
        params: Optional[dict] = None,
        use_service_role: bool = True
    ) -> dict:
        url = f"{self.base_url}/rest/v1{path}"
        headers = self._get_headers(use_service_role)

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                json=json,
                params=params
            )
            response.raise_for_status()
            return response.json() if response.content else None

    async def select(
        self,
        table: str,
        columns: str = "*",
        filters: Optional[dict] = None,
        use_service_role: bool = True
    ) -> list:
        params = {"select": columns}
        if filters:
            params.update(filters)
        return await self._request("GET", f"/{table}", params=params, use_service_role=use_service_role)

    async def insert(
        self,
        table: str,
        data: dict,
        use_service_role: bool = True
    ) -> dict:
        result = await self._request("POST", f"/{table}", json=data, use_service_role=use_service_role)
        return result[0] if isinstance(result, list) else result

    async def update(
        self,
        table: str,
        id: str,
        data: dict,
        use_service_role: bool = True
    ) -> dict:
        result = await self._request(
            "PATCH",
            f"/{table}",
            json=data,
            params={"id": f"eq.{id}"},
            use_service_role=use_service_role
        )
        return result[0] if isinstance(result, list) else result

    async def delete(
        self,
        table: str,
        id: str,
        use_service_role: bool = True
    ) -> None:
        await self._request(
            "DELETE",
            f"/{table}",
            params={"id": f"eq.{id}"},
            use_service_role=use_service_role
        )


supabase_client = SupabaseClient()


def get_supabase_client() -> SupabaseClient:
    return supabase_client
