import jwt
from sqlalchemy import select
from fastapi import Depends, HTTPException
from server.utils.jwt_handler import jwt_handler
from server.database.db import async_session
from server.database.shema import Users
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

security = HTTPBearer()

async def get_access_token(
        credentional: HTTPAuthorizationCredentials = Depends(security),
):
    token = credentional.credentials
    try:

        payload = await jwt_handler.decode_token(token)
        telegram_id = payload["telegram_id"]

        async with async_session() as session:
            result = await session.execute(
                select(Users).where(Users.telegram_id == telegram_id)
            )
            user = result.scalar_one_or_none()

        if user is None:
            raise HTTPException(status_code=404, detail="User not found!")
        return user
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token Invalid")