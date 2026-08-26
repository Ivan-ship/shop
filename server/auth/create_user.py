from fastapi import APIRouter
from server.database.db import async_session
from server.utils.jwt_handler import jwt_handler
from server.repositories.create_user import CreateUser
from server.database.model import UserCreate


router = APIRouter()

@router.post("/user/register")
async def create_user(user_data: UserCreate):

    async with async_session() as session:
        repository = CreateUser(session)
        user = await repository.create_user(user_data)

        token = await jwt_handler.generate_access_token(
            user.telegram_id
        )
        return {
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": user.user_id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        }