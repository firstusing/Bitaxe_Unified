from __future__ import annotations

import async_timeout
from aiohttp import ClientError, ClientSession


class BitaxeApiError(Exception):
    """Raised when Bitaxe API communication fails."""


class BitaxeApi:
    def __init__(self, session: ClientSession, host: str) -> None:
        self._session = session
        self.host = host.strip().removeprefix("http://").removeprefix("https://").rstrip("/")
        self.base_url = f"http://{self.host}"

    async def _request(self, method: str, path: str, **kwargs):
        url = f"{self.base_url}{path}"
        try:
            async with async_timeout.timeout(8):
                response = await self._session.request(method, url, **kwargs)
                if response.status >= 400:
                    text = await response.text()
                    raise BitaxeApiError(f"{method} {path} failed: HTTP {response.status}: {text}")
                if response.content_type and "json" in response.content_type:
                    return await response.json()
                text = await response.text()
                return text or None
        except (ClientError, TimeoutError) as err:
            raise BitaxeApiError(f"{method} {path} failed: {err}") from err

    async def get(self, path: str) -> dict:
        return await self._request("GET", path)

    async def info(self) -> dict:
        return await self.get("/api/system/info")

    async def asic(self) -> dict:
        return await self.get("/api/system/asic")

    async def system(self) -> dict:
        return await self.get("/api/system")

    async def pool(self) -> dict:
        return await self.get("/api/pool")

    async def network(self) -> dict:
        return await self.get("/api/network")

    async def statistics(self) -> dict:
        return await self.get("/api/system/statistics")

    async def statistics_dashboard(self) -> dict:
        return await self.get("/api/system/statistics/dashboard")

    async def pause(self) -> None:
        await self._request("POST", "/api/system/pause")

    async def resume(self) -> None:
        await self._request("POST", "/api/system/resume")

    async def restart(self) -> None:
        await self._request("POST", "/api/system/restart")

    async def identify(self) -> None:
        await self._request("POST", "/api/system/identify")

    async def patch_system(self, payload: dict) -> None:
        await self._request("PATCH", "/api/system", json=payload)
