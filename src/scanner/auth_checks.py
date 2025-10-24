# src/scanner/auth_checks.py
from .http_probe import probe_url
import asyncio
import httpx

async def check_auth(endpoint: str, method: str = "GET") -> dict:
    res_no_auth = await probe_url(endpoint, method)
    # simulate invalid token by adding header
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.request(method, endpoint, headers={"Authorization": "Bearer invalidtoken"}, timeout=10)
            code = resp.status_code
        except Exception as e:
            code = None
    result = {
        "endpoint": endpoint,
        "no_auth_status": res_no_auth.get("status"),
        "invalid_token_status": code
    }
    return result
