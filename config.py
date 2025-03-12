from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_prefix: str = "/api/v1"
    wecom_corpid: str = Field(..., env="WECOM_CORPID")  # 必填字段
    wecom_secret: str = Field(..., env="WECOM_SECRET")  # 必填字段
    wecom_agent_id: int = Field(..., env="WECOM_AGENT_ID")  # 类型改为 int
    token_api_url: str = Field(..., env="TOKEN_API_URL")  # 必填字段
    message_api_url: str = Field(..., env="MESSAGE_API_URL")  # 必填字段
    token_expire_buffer: int = 600

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
