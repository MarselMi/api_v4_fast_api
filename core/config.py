from pydantic import BaseModel
from pydantic_settings import BaseSettings


class DbSettings(BaseModel):
    url: str = f"mysql+aiomysql://admin:ux5DdPxWIwer@localhost:3307/spaff_db"
    echo: bool = True


class Settings(BaseSettings):
    api_v4_prefix: str = "/api/v4"

    db: DbSettings = DbSettings()


settings = Settings()
