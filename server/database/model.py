from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str | None = None
    first_name: str
    last_name: str | None = None
    telegram_id: int
