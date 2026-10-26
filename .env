from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "SOMX.NET Sovereign Engine"
    environment: str = "development"
    secret_key: str = "super-secret-key"

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
