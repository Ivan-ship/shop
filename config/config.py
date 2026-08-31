from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict

class SettingConf(BaseSettings):
    bot_token: SecretStr
    #--JWT--
    JWT_ALGORITHM: str
    SECRET_KEY: str
    JWT_ACCESS_TOKEN_EXPIRE: int

    #--Yoomany--
    YOOKASSA_SHOP_ID: str
    YOOKASSA_SECRET_KEY: str

    RETURN_URL:str

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

configuration = SettingConf()