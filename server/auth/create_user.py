from fastapi import APIRouter
from database.model import CreateUser
from database.db import async_session
from database.shema import Users
from sqlalchemy import select


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
