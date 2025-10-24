# src/scanner/http_probe.py
import asyncio
import httpx
from typing import Dict

async def probe_url(url: str, method: str = "GET", timeout: int = 10) -> Dict:
    async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as client:
        try:
            if method.upper() == "OPTIONS":
                resp = await client.options(url)
            elif method.upper() == "HEAD":
                resp = await client.head(url)
            else:
                resp = await client.get(url)
            return {
                "url": url,
                "status": resp.status_code,
                "headers": dict(resp.headers),
                "elapsed_ms": int(resp.elapsed.total_seconds() * 1000)
            }
        except Exception as e:
            return {"url": url, "error": str(e)}
