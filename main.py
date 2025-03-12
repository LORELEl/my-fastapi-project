import time
from typing import Annotated, Union

from fastapi import FastAPI, status, HTTPException, Depends
import httpx
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel

from config import settings
from token_manager import token_manager

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.get("/items/")
async def read_items(token: Annotated[str, Depends(oauth2_scheme)]):
    return {"token": token}


@app.post(settings.api_prefix + "/forward", status_code=status.HTTP_202_ACCEPTED)
async def forward_message(request_data: dict):
    try:
        #  获取token
        access_token = await token_manager.get_token()

        api_url = f"{settings.message_api_url}?access_token={access_token}"

        async with httpx.AsyncClient() as client:
            resp = await client.post(
                api_url,  # 使用动态URL
                json={
                    **request_data
                }
            )
            resp.raise_for_status()

            return {"status": "success", "wecom_response": resp.json()}

    except (httpx.HTTPError, ValueError) as e:
        raise HTTPException(
            status_code=500,
            detail=f"企业微信接口调用失败: {str(e)}"
        )


@app.get("/debug/token")
async def debug_token():
    return {
        "current_time": time.time(),
        "token": await token_manager.get_token(),
        "expires_at": token_manager._expires_at,
        "remaining": token_manager._expires_at - time.time()
    }


@app.get("/")
async def index():
    return "hell, world!"
