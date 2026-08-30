from pathlib import Path
from fastapi import APIRouter, HTTPException
from server.database.db import async_session
from server.database.shema import Users
from sqlalchemy import select
from server.database.model import DownloadProduct
from server.repositories.get_prod import GetProduct
from server.repositories.purchases import Purchase
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/products")
async def get_products():
    async with async_session() as session:
        repository = GetProduct(session)
        products = await repository.get_prod()
        return products


@router.post("/products/{prod_id}/download")
async def product_file(prod_id: int, data: DownloadProduct):
    async with async_session() as session:
        repository = GetProduct(session)
        product = await repository.get_by_id(prod_id)

        user = await session.scalar(
            select(Users).where(Users.telegram_id == data.telegram_id)
        )

        if user is None:
            raise HTTPException(
                status_code=404,
                detail="пользоваетль не найден!"
            )


        if product is None:
            raise HTTPException(
                status_code=404,
                detail="Продукт не найден!"
            )

        file_path = Path("files") / product.file_name

        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Файл не найден!"
            )

        purcahase_repository = Purchase(session)
        purchase = await  purcahase_repository.create_purchase(user.user_id, prod_id)

        return FileResponse(
            file_path,
            filename = product.file_name,
            media_type = "application/pdf"
        )