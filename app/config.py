from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    retailcrm_api_url: str
    retailcrm_api_key: str

    class Config:
        env_file = ".env"


settings = Settings()
