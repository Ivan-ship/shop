from fastapi import APIRouter
from server.database.db import async_session
from server.repositories.create_user import CreateUser
from server.database.model import UserCreate


router = APIRouter()

@router.post("/user/register")
async def create_user(user_data: UserCreate):

    async with async_session() as session:
        repository = CreateUser(session)
        user = await repository.create_user(user_data)

        return {
            "user": {
                "id": user.user_id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        }