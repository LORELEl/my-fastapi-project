from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    api_prefix: str = "/api/v1"
    wecom_corpid: str
    wecom_secret: str
    wecom_agent_id: str
    token_api_url: str
    message_api_url: str
    token_expire_buffer: int = 600

    class Config:
        env_file = ".env"


settings = Settings()
