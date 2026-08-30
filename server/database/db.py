from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

BASE_DIR = Path(__file__).resolve().parents[2]

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    model_config = SettingsConfigDict(env_file=BASE_DIR / ".env", extra="ignore")

    def DB_CONNECT(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = Settings()

engine = create_async_engine(
    url=settings.DB_CONNECT(),
    echo=True,
    pool_size=5,
    max_overflow=10
)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False
)