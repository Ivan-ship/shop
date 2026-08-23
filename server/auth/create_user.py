from fastapi import APIRouter
from server.database.model import CreateUser
from server.database.db import async_session
from server.database.shema import Users
from sqlalchemy import select
from server.utils.jwt_handler import jwt_handler


router = APIRouter()

@router.post("/user/register")
async def create_user(user_data: CreateUser):

    async with async_session() as session:
        result = await session.execute(
            select(Users).where(
                Users.telegram_id == user_data.telegram_id
            )
        )
        user = result.scalar_one_or_none()

        if user is None:
            user = Users(
                username=user_data.username,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                telegram_id=user_data.telegram_id
            )
            session.add(user)
            await session.commit()
            await session.refresh(user)

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