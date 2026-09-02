from server.database.shema import Purchases
from sqlalchemy import select

class Purchase():
    def __init__(self, session):
        self.session = session

    async def create_purchase(self, user_id: int, prod_id: int):
        purchase = Purchases(
            user_id = user_id,
            prod_id = prod_id
        )
        self.session.add(purchase)
        await self.session.commit()
        return purchase
    
    async def get_purchase(self, user_id: int, prod_id: int):
        result = await self.session.execute(
            select(Purchases).where(
                Purchases.user_id == user_id, 
                Purchases.prod_id == prod_id
            )
        )
        return result.scalar_one_or_none()