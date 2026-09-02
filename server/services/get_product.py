from pathlib import Path
from fastapi import APIRouter, HTTPException
from server.database.db import async_session
from server.database.shema import Users
from sqlalchemy import select
from server.database.model import DownloadProduct
from server.repositories.get_prod import GetProduct
from server.repositories.purchases import Purchase
from server.repositories.payment import GetPayment
from fastapi.responses import FileResponse
from server.services.yookassa import create_payment
from yookassa import Payment as YookassaPayment

router = APIRouter()


@router.get("/products")
async def get_products():
    async with async_session() as session:
        repository = GetProduct(session)
        products = await repository.get_prod()
        return products


@router.post("/products/{prod_id}/payment")
async def create_product_payment(prod_id: int, data: DownloadProduct):
    async with async_session() as session:
        product_repository = GetProduct(session)

        product = await product_repository.get_by_id(prod_id)

        if product is None:
            raise HTTPException(status_code=404, detail="Файл не найден!")
        
        user = await session.scalar(
            select(Users).where(Users.telegram_id == data.telegram_id)
        )

        payment = await create_payment(
            amount = f"{product.price}.00",
            description = f"Покупка{product.name}",
            prod_id=product.prod_id,
            telegram_id=user.telegram_id
        )

        payment_repository = GetPayment(session)

        db_payment = await payment_repository.create_payment(
            yookassa_payment_id = payment.id,
            user_id = user.user_id,
            prod_id = product.prod_id,
            status = payment.status
        )

        return{
            "payment_id": payment.id,
            "payment_url": payment.confirmation.confirmation_url,
            "status": payment.status
        }

@router.post("/payment/{payment_id}/check")
async def check_payment(payment_id: str):

    yookassa_payment = YooKassaPayment.find_one(
        payment_id
    )

    async with async_session() as session:

        payment_repository = GetPayment(session)

        payment = await (
            payment_repository
            .get_payment_by_yookassa_id(payment_id)
        )

        if payment is None:
            raise HTTPException(
                status_code=404,
                detail="Платёж не найден"
            )

        if yookassa_payment.status == "succeeded":

            await payment_repository.update_status(
                payment,
                "succeeded"
            )

            purchase_repository = Purchase(session)

            await purchase_repository.create_purchase(
                payment.user_id,
                payment.prod_id
            )

            if purchase is None:
                await purchase_repository.create_purchase(
                payment.user_id,
                payment.prod_id
            )

            await session.commit()

            return {
                "status": "succeeded",
                "message": "Оплата успешно подтверждена"
            }

        return {
            "status": yookassa_payment.status
        }


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
        
        purchase_repository = Purchase(session)

        purchase = await purchase_repository.get_purchase(user.user_id, prod_id)

        if purchase is None:
            raise HTTPException(
                status_code=403, detail="Необходимо оплатить товар!"
            )

        file_path = Path("files") / product.file_name

        if not file_path.exists():
            raise HTTPException(
                status_code=404,
                detail="Файл не найден!"
            )


        return FileResponse(
            file_path,
            filename = product.file_name,
            media_type = "application/pdf"
        )