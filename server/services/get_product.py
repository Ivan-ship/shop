from fastapi import APIRouter
from server.database.db import async_session
from sqlalchemy import select
from server.database.shema import Products

router = APIRouter()


@router.get("/products")
async def get_products():
    async with async_session() as session:
        result = await session.execute(
            select(Products).where(Products.is_active == True)
        )
        products = result.scalars().all()
        return products