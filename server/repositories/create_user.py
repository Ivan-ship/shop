from server.database.shema import Users
from sqlalchemy import select

class CreateUser():
    def __init__(self, session):
        self.session = session

    async def create_user(self, user_data):
        result = await self.session.execute(
             select(Users).where(
                    Users.telegram_id == user_data.telegram_id
                )
            )
        user = result.scalar_one_or_none()
        
        if user is not None:
            return user
        
        user = Users(
            username=user_data.username,
            first_name=user_data.first_name,
            last_name=user_data.last_name,
            telegram_id=user_data.telegram_id
            )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user