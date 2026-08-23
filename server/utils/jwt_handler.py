import jwt
from datetime import datetime, timedelta, timezone
from config.config import configuration


class JWT_Handler:
    def __init__(self):
        self.algorithm = configuration.JWT_ALGORITHM
        self.secret = configuration.SECRET_KEY
        self.access_token_exp = configuration.JWT_ACCESS_TOKEN_EXPIRE

    async def generate_access_token(self, telegram_user_id: int) -> str:
        payload = {
            "telegram_id": str(telegram_user_id),
        }
        token,_ = await self._create_token(
            payload,
            timedelta(days=self.access_token_exp)
            )
        return token

    async def _create_token(self, data: dict, expires_delta: timedelta) -> tuple[str, datetime]:

        expire = datetime.now(timezone.utc) + expires_delta
        payload = data.copy()
        payload["exp"] = expire
        token = jwt.encode(
            payload, 
            self.secret,
            algorithm=self.algorithm
        )
        return token, expire

    async def decode_token(self, token: str) -> str:
        payload = jwt.decode(
            token,
            self.secret,
            algorithm=[self.algorithm]
        )
        return payload

jwt_handler = JWT_Handler()