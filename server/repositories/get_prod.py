from sqlalchemy import select
from server.database.shema import Products

class GetProduct():
    def __init__(self, session):
        self.session = session

    async def get_prod(self):
        result = await self.session.execute(
            select(Products).where(Products.is_active == True)
        )
        return result.scalars().all()