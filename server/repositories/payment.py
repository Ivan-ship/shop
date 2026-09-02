from sqlalchemy import select
from server.database.shema import Payment
from sqlalchemy.ext.asyncio import AsyncSession

class GetPayment():
    def __init__(self, session: AsyncSession):
        self.session = session


    async def create_payment(
        user_id: int,
        prod_id: int,
        yookassa_payment_id: str,
        status: str = "pending"
    ):
        payment = Payment(
            yookassa_payment_id = yookassa_payment_id,
            user_id = user_id,
            prod_id = prod_id,
            status = status
        )
        self.session.add(payment)

        await self.session.commit()
        return payment

    async def get_by_yookassa_payment_id(self, yookassa_payment_id):
        result = await self.session.execute(
            Payment
            ).where(Payment.yookassa_payment_id == yookassa_payment_id)  
        return result.scalar_one_or_none()
    

    async def update_status(self, status: str, payment: Payment):
        payment.status = status
        await self.session.commit()
        return payment