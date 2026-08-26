from fastapi import APIRouter
from server.database.db import async_session
from sqlalchemy import select
from server.repositories.get_prod import GetProduct

router = APIRouter()


@router.get("/products")
async def get_products():
    async with async_session() as session:
        repository = GetProduct(session)
        products = await repository.get_prod()
        return products

@router.post("/get/products")
async def product_file():
    pass