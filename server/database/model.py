from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str | None = None
    first_name: str
    last_name: str | None = None
    telegram_id: int


class GetPurchases(BaseModel):
    user_id: int
    prod_id: int

class DownloadProduct(BaseModel):
    telegram_id: int