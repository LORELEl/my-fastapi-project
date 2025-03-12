import time

import httpx
from config import settings


class TokenManager:
    def __init__(self):
        self._access_token = None
        self._expires_at = 0

    async def get_token(self) -> str:
        if time.time() < (self._expires_at - settings.token_expire_buffer):
            return self._access_token

        print("get_token again~")
        async with httpx.AsyncClient() as client:
            params = {
                "corpid": settings.wecom_corpid,
                "corpsecret": settings.wecom_secret
            }
            resp = await client.get(settings.token_api_url, params=params)
            resp.raise_for_status()

            data = resp.json()
            if data["errcode"] != 0:
                raise ValueError(f"Token获取失败: {data}")

            self._access_token = data["access_token"]
            self._expires_at = time.time() + data["expires_in"]
            return self._access_token


token_manager = TokenManager()  # 全局单例
