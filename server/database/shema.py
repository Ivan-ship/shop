from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy import String, BigInteger

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int]=mapped_column(primary_key=True)
    username: Mapped[str]=mapped_column(String(50))
    first_name: Mapped[str]=mapped_column(String(50))
    last_name: Mapped[str]=mapped_column(String(50))
    telegram_id: Mapped[int]=mapped_column(BigInteger)