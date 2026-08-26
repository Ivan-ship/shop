from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, relationship
from sqlalchemy import String, BigInteger, Integer, Boolean, ForeignKey

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"

    user_id: Mapped[int]=mapped_column(primary_key=True)
    username: Mapped[str]=mapped_column(String(50))
    first_name: Mapped[str]=mapped_column(String(50))
    last_name: Mapped[str]=mapped_column(String(50))
    telegram_id: Mapped[int]=mapped_column(BigInteger)

    purchases = Mapped[list["Purchases"]]=relationship(
        "Purchases", back_populates="user", 
        cascade="all, delete-orphan")


class Products(Base):
    __tablename__ = "products"

    prod_id: Mapped[int]=mapped_column(primary_key=True)
    name: Mapped[str]=mapped_column(String(50))
    price: Mapped[int]=mapped_column(Integer)
    file_name: Mapped[str]=mapped_column(String(100))
    is_active: Mapped[bool]=mapped_column(Boolean, default=False)

    purchases = Mapped[list["Purchases"]]=relationship(
        "Purchases", back_populates="product", 
        cascade="all, delete-orphan")
    

class Purchases(Base):
    __tablename__ ="purchases"

    purchases_id: Mapped[int]=mapped_column(primary_key=True)
    user_id: Mapped[int]=mapped_column(ForeignKey("users.user_id"))
    prod_id: Mapped[int]=mapped_column(ForeignKey("products.prod_id"))

    user = Mapped["Users"]=relationship(
        "Users",
        back_populates="purchases"
    )

    product = Mapped["Products"]=relationship(
        "Products",
        back_populates="purchases"
    )